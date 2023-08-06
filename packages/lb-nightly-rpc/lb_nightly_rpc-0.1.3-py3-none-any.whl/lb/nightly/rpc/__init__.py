###############################################################################
# (c) Copyright 2020-2021 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
__version__ = "0.1.3"

import logging
import os

from celery import Celery
from celery.signals import celeryd_after_setup, worker_process_init
from celery.utils.log import get_task_logger
from kombu import Queue
from lb.nightly.configuration import service_config

from . import archs, scheduler, tasks

conf = service_config(silent=True)
try:
    broker_url = conf.get("rabbitmq", {}).get("url")
    backend_url = conf.get("mysql", {}).get("url")
except AttributeError:
    logging.warning("Broker and Backend not specified, the results will not be kept")
    broker_url = "amqp://guest:guest@rabbitmq:5672"
    backend_url = "rpc"

app = Celery(
    __name__,
    broker=broker_url,
    backend=backend_url,
)
app.conf.update(
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_track_started=True,
    result_extended=True,
)

queues = [
    Queue("checkout", routing_key="checkout.#"),
    Queue("scheduler", routing_key="scheduler.#"),
]
for arch in archs.archs():
    queues.append(Queue(f"build-{arch}", routing_key=f"build-{arch}.#"))
    queues.append(Queue(f"test-{arch}", routing_key=f"test-{arch}.#"))


# global variable to store the path to worker process directory
# the value is set at worker process initialisation
worker_process_dir = ""


@worker_process_init.connect()
def configure_worker(signal=None, sender=None, **kwargs):
    global worker_process_dir
    worker_process_dir = os.path.join(
        os.path.dirname(os.environ["CELERY_LOG_FILE"]),
        os.path.splitext(os.path.basename(os.environ["_MP_FORK_LOGFILE_"]))[0],
    )
    if worker_process_dir:
        os.makedirs(worker_process_dir, exist_ok=True)


@celeryd_after_setup.connect
def setup_direct_queue(sender, instance, **kwargs):
    # disable default queue named 'celery'
    instance.app.amqp.queues.deselect("celery")
    worker_type = sender.split("@")[0]
    for queue in queues:
        if queue.name.split("-")[0] == worker_type:
            instance.app.amqp.queues.select_add(queue.name)


def route_task(name, args, kwargs, options, task=None, **kw):
    if name == "lb.nightly.rpc.tasks.checkout":
        return {"queue": "checkout"}
    elif name.startswith("lb.nightly.rpc.scheduler."):
        return {"queue": "scheduler"}
    elif name.startswith("lb.nightly.rpc.tasks."):
        # build and test tasks require 'platform' arguments which is args[1]
        arch = archs.required(args[1])
        return {"queue": f"{name.split('.')[-1]}-{arch}"}


app.conf.task_routes = (route_task,)
app.conf.task_default_exchange = "tasks"
app.conf.task_default_exchange_type = "direct"

logger = get_task_logger(__name__)


_checkout = app.task(tasks.checkout)
_build = app.task(tasks.build)
_test = app.task(tasks.test)

checkout = lambda *args, **kwargs: _checkout.delay(*args, **kwargs).get()
build = lambda *args, **kwargs: _build.delay(*args, **kwargs).get()
test = lambda *args, **kwargs: _test.delay(*args, **kwargs).get()

_start_slot = app.task(scheduler.start_slot)
start_slot = lambda *args, **kwargs: _start_slot.delay(*args, **kwargs).forget()

# coding: utf-8
import logging
import os
import random
import threading
import time
from datetime import datetime
from pydantic import BaseModel

import socket

from watchmen_boot.config.config import settings
from watchmen_boot.guid.remoteid import next_id
from watchmen_boot.guid.storage.choise_storage import find_template

logger = logging.getLogger(__name__)


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
        return ip


class InvalidSystemClock(Exception):
    pass


class SnowFlakeIdWorker(object):
    TWEPOCH = 1420041600000
    WORKER_ID_BITS = 10
    DATACENTER_ID_BITS = 2
    SEQUENCE_BITS = 10
    MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 2**10-1 0b1111111111
    MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)
    MAX_SEQUENCE = -1 ^ (-1 << SEQUENCE_BITS)
    WOKER_ID_SHIFT = SEQUENCE_BITS
    DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
    TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

    def __init__(self, datacenter_id=0, sequence=0):
        gen = WorkerIdGen()
        worker_id = gen.generate_worker_id()
        threading.Thread(target=WorkerIdGen.heart_beat, args=(gen,), daemon=True).start()
        # sanity check
        if worker_id > self.MAX_WORKER_ID or worker_id < 0:
            raise ValueError('worker_id max value')

        if datacenter_id > self.MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError('datacenter_id max value')

        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = sequence

        self.last_timestamp = -1  #

    def _gen_timestamp(self):
        """
        generate a timestamp
        :return:int timestamp
        """
        return int(time.time() * 1000)

    def get_id(self):
        """
        get a new id
        :return:
        """
        timestamp = self._gen_timestamp()

        #
        if timestamp < self.last_timestamp:
            raise InvalidSystemClock

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & self.MAX_SEQUENCE
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = ((timestamp - self.TWEPOCH) << self.TIMESTAMP_LEFT_SHIFT) | (
                self.datacenter_id << self.DATACENTER_ID_SHIFT) | \
                 (self.worker_id << self.WOKER_ID_SHIFT) | self.sequence
        return new_id

    def _til_next_millis(self, last_timestamp):
        """
        next timestamp id
        """
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp


class WorkerIdGen:

    def __init__(self):
        self.ip = get_host_ip()
        self.process_id = str(os.getpid())
        self.storage_template = find_template()

    def generate_worker_id(self):
        workers = self.storage_template.list_all(WorkerId)
        result = self.check_worker_status(workers)
        if result:
            return result.workerId
        else:
            new_worker_id = self.random_worker_id(workers)
            return new_worker_id

    def check_worker_status(self, workers):
        result = None
        registered_workers = workers
        for el in registered_workers:
            if (datetime.now().replace(microsecond=0) - el.regDate).days >= 1:
                self.storage_template.delete_by_id(el.ip, el.processId)
                workers.remove(el)
            else:
                if el.ip == self.ip and el.processId == self.process_id:
                    result = el
                    break
        return result

    def random_worker_id(self, workers):
        new_worker_id = random.randrange(0, 1024)
        result = self.check_worker_id(workers, new_worker_id)
        if result:
            self.storage_template.insert_one(
                {"ip": self.ip, "processid": self.process_id, "workerid": new_worker_id,
                 "regdate": datetime.now().replace(microsecond=0)})
            return new_worker_id
        else:
            return self.random_worker_id(workers)

    def check_worker_id(self, workers, new_worker_id):
        registered_workers = workers
        for el in registered_workers:
            if el.workerId == new_worker_id:
                return False
        return True

    def heart_beat(self):
        try:
            while True:
                self.storage_template.update_one(self.ip, self.process_id)
                time.sleep(30)
        finally:
            logger.error("worker id register heart beat stop")


class WorkerId(BaseModel):
    ip: str = None
    processId: str = None
    workerId: int = None
    regDate: datetime = None


worker = SnowFlakeIdWorker(settings.SNOWFLAKE_DATACENTER)


def get_surrogate_key():
    return str(get_int_surrogate_key())


def get_int_surrogate_key():
    if settings.SNOWFLAKE_REMOTE:
        return next_id()
    else:
        return worker.get_id()

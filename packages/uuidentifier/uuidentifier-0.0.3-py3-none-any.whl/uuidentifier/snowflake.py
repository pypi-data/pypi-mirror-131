#!/usr/bin/env python
import operator
import os
import time
import warnings
from datetime import datetime
from functools import reduce


class Worker:
    def __init__(self) -> None:
        self.all_macs = []

    def get_mac(self, ifname: str) -> str:
        """ Get MAC address corresponding to the given interface """
        cmd = "ifconfig | grep -A5 {} | grep ether".format(ifname)
        resp = os.popen(cmd).read().strip()
        if not resp:
            warnings.warn(
                'No MAC address found for interface {}'.format(ifname))
            return self.get_first_valid_mac()
        return resp.split()[1]

    def get_all_macs(self) -> list:
        """ Get all MAC addresses of all interfaces """
        if not self.all_macs:
            self.all_macs = os.popen("ifconfig | awk '/ether/{print $2}'"
                                     ).read().strip().split('\n')
        return self.all_macs

    def get_first_valid_mac(self) -> str:
        """ Get the first valid MAC address of the all interfaces """
        return self.get_all_macs()[0]


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SnowFlake(metaclass=SingletonMeta):
    """Generate a uuid"""
    def __init__(self, interface: str = '') -> None:
        """ A valid interface must be given """
        self._starting_date = '2021-01-01 00:00:00,000'
        self.__interface = interface
        self.__sequence = 0
        self.__worker_id = None

    @property
    def interface(self) -> str:
        return self.__interface

    @interface.setter
    def interface(self, new_interface: str) -> str:
        self.__interface = new_interface
        return self.__interface

    @property
    def timestamp(self) -> int:
        cur_time = time.time() * 1000
        start_time = datetime.strptime(
            self._starting_date, "%Y-%m-%d %H:%M:%S,%f").timestamp() * 1000
        self.__timestamp = int(cur_time - start_time)
        return self.__timestamp

    @property
    def worker_id(self):
        if self.__worker_id is None:
            if self.__interface:
                mac = Worker().get_mac(self.__interface)
            else:
                mac = Worker().get_first_valid_mac()
            acc = reduce(operator.add, [int(x, 16) for x in mac.split(':')])
            self.__worker_id = acc % 1024
        return self.__worker_id

    @property
    def datacenter_id(self) -> int:
        raise NotImplementedError

    @property
    def sequence(self) -> int:
        self.__sequence = (self.__sequence + 1) % 4096
        return self.__sequence

    def uuid(self) -> int:
        timestamp = self.timestamp
        worker_id = self.worker_id
        sequence = self.sequence
        return ((timestamp << 22) | (worker_id << 12) | sequence)


if __name__ == '__main__':
    snowflake = SnowFlake('enp34s0')
    for i in range(10):
        print(snowflake.uuid())

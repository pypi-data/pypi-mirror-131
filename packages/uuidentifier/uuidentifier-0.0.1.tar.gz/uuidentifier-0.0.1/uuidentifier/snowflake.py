#!/usr/bin/env python
import struct
import socket
import fcntl
from datetime import datetime
import operator
import os
import time
from functools import reduce


class Worker:
    def get_mac(self, ifname: str) -> str:
        """ Get MAC address of the given interface """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack(
            '256s', bytes(ifname, 'utf-8')[:15]))
        return ':'.join('%02x' % b for b in info[18:24])

    def get_first_valid_mac(self) -> str:
        """ Get the first valid MAC address of the all interfaces """
        ifnames = [x.strip()
                   for x in os.popen('ls /sys/class/net/').readlines()]
        for ifname in ifnames:
            mac = self.get_mac(ifname)
            if mac != '00:00:00:00:00:00':
                return mac


class SnowFlake:
    """Generate a uuid"""

    def __init__(self, interface: str = '') -> None:
        """ A valid interface must be given """
        self._starting_date = '2021-01-01 00:00:00,000'
        self.interface = interface
        self.__sequence = 0
        self.__worker_id = None

    @property
    def timestamp(self) -> int:
        cur_time = time.time() * 1000
        start_time = datetime.strptime(
            self._starting_date, "%Y-%m-%d %H:%M:%S,%f").timestamp()*1000
        self.__timestamp = int(cur_time - start_time)
        return self.__timestamp

    @property
    def worker_id(self):
        if self.__worker_id is None:
            if self.interface:
                mac = Worker().get_mac(self.interface)
            else:
                mac = Worker().get_first_valid_mac()
            prod = reduce(operator.add, [int(x, 16) for x in mac.split(':')])
            self.__worker_id = prod % 1024
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

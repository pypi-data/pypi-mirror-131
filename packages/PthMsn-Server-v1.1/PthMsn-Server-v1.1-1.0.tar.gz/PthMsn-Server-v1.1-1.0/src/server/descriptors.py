import logging
import sys
from ipaddress import ip_address

sys.path.append('../../')

LOG = logging.getLogger('server')


class Port:
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            LOG.error(f'Port must be in range: 1024 - 65535. Your value: {value}')
            exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class Addr:
    def __set__(self, instance, value):
        try:
            ip_address(value)
            instance.__dict__[self.name] = value
        except ValueError as err:
            LOG.error(f'IP {value} error: {err}')

    def __set_name__(self, owner, name):
        self.name = name



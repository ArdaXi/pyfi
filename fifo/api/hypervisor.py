from .wiggle import Entity
from fifo.helper import *

hypervisor_fmt = {
    'uuid':
    {'title': 'UUID', 'len': 36, 'fmt': "%36s", 'get': lambda e: d(e, ['uuid'])},
    'name':
    {'title': 'Name', 'len': 30, 'fmt': "%30s", 'get': lambda e: d(e, ['alias'])},
    'free':
    {'title': 'Free RAM', 'len': 10, 'fmt': "%10s",
     'get': lambda e: str(d(e, ['resources', 'free-memory'])) + "MB"},
    'used':
    {'title': 'Used RAM', 'len': 10, 'fmt': "%10s",
     'get': lambda e: str(d(e, ['resources', 'provisioned-memory'])) + "MB"},
    'total':
    {'title': 'Total RAM', 'len': 10, 'fmt': "%10s",
     'get': lambda e: str(d(e, ['resources', 'total-memory'])) + "MB"},
    'smartos':
    {'title': 'SmartOS Version', 'len': 20, 'fmt': "%-20s",
     'get': lambda e: d(e, ['sysinfo', 'Live Image'])},
}

class Hypervisor(Entity):
    def __init__(self, wiggle):
        self._wiggle = wiggle
        self._resource = "hypervisors"

    def make_parser(self, subparsers):
        parser_hypervisors = subparsers.add_parser('hypervisors', help='hypervisor related commands')
        parser_hypervisors.set_defaults(endpoint=self)
        subparsers_hypervisors = parser_hypervisors.add_subparsers(help='hypervisor commands')
        parser_hypervisors_list = subparsers_hypervisors.add_parser('list', help='lists hypervisors')
        parser_hypervisors_list.add_argument("--fmt", action=ListAction,
                                             default=['uuid', 'name', 'free', 'used'])
        parser_hypervisors_list.add_argument("-H", action='store_false')
        parser_hypervisors_list.add_argument("-p", action='store_true')
        parser_hypervisors_list.set_defaults(func=show_list,
                                          fmt_def=hypervisor_fmt)
        parser_hypervisors_get = subparsers_hypervisors.add_parser('get', help='gets a hypervisor')
        parser_hypervisors_get.add_argument("uuid")
        parser_hypervisors_get.set_defaults(func=show_get)

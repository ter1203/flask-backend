from libs.quovo.base import QuovoRequest

from .entry import DIEntry, container


def register_all():
    '''Register all DI entries'''

    register_admin_entries()
    register_helpers()


def register_admin_entries():

    pass


def register_helpers():

    def quovo_request_create():
        return QuovoRequest()

    container.add(DIEntry(
        QuovoRequest, quovo_request_create
    ))

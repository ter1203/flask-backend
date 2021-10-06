from apps.user.lib.parser import AuthParser
from apps.user.lib.validator import AuthValidator
from libs.helper.auth import AuthHelper

from .entry import DIEntry, container


def register_all():
    '''Register all DI entries'''

    register_auth_entries()
    register_helpers()


def register_auth_entries():

    def auth_parser_create():
        return AuthParser()
        
    container.add(DIEntry(
        AuthParser, auth_parser_create
    ))


    def auth_validator_create():
        return AuthValidator()

    container.add(DIEntry(
        AuthValidator, auth_validator_create
    ))


def register_helpers():

    def auth_helper_create():
        return AuthHelper()

    container.add(DIEntry(
        AuthHelper, auth_helper_create
    ))
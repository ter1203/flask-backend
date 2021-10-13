from apps.auth.lib.parser import AuthParser
from apps.auth.lib.validator import AuthValidator
from apps.auth.lib.auth.authenticator import Authenticator
from apps.user.lib.parser import UserParser
from apps.model.lib.parser import ModelParser
from apps.account.lib.parser import AccountParser

from .entry import DIEntry, container


def register_all():
    '''Register all DI entries'''

    register_auth_entries()
    register_account_entries()
    register_model_entries()
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

    def authenticator_create():
        return Authenticator()

    container.add(DIEntry(
        Authenticator, authenticator_create
    ))

    def user_parser_create():
        return UserParser()

    container.add(DIEntry(
        UserParser, user_parser_create
    ))


def register_account_entries():

    def account_parser_create():
        return AccountParser()

    container.add(DIEntry(
        AccountParser, account_parser_create
    ))


def register_model_entries():

    def model_parser_create():
        return ModelParser()

    container.add(DIEntry(
        ModelParser, model_parser_create
    ))


def register_helpers():
    pass
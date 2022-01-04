from apps.auth.lib.parser import AuthParser
from apps.auth.lib.validator import AuthValidator
from apps.auth.lib.auth.authenticator import Authenticator
from apps.user.lib.parser import UserParser
from apps.model.lib.parser import ModelParser
from apps.model.lib.validator import ModelValidator
from apps.account.lib.parser import AccountParser
from apps.portfolio.lib.parser import PortfolioParser
from apps.trade.lib.parser import TradeParser
from apps.admin.lib.parser import AdminParser

from .entry import DIEntry, container


def register_all():
    '''Register all DI entries'''

    register_auth_entries()
    register_account_entries()
    register_model_entries()
    register_portfolio_entries()
    register_trade_entries()
    register_admin_entries()
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

    def model_validator_create():
        return ModelValidator()

    container.add(DIEntry(
        ModelValidator, model_validator_create
    ))


def register_portfolio_entries():

    def portfolio_parser_create():
        return PortfolioParser()

    container.add(DIEntry(
        PortfolioParser, portfolio_parser_create
    ))


def register_trade_entries():

    def trade_parser_create():
        return TradeParser()

    container.add(DIEntry(
        TradeParser, trade_parser_create
    ))


def register_admin_entries():

    def admin_parser_create():
        return AdminParser()

    container.add(DIEntry(
        AdminParser, admin_parser_create
    ))


def register_helpers():
    pass
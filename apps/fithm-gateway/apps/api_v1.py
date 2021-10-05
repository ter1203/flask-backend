from flask import Blueprint
from flask_restx import Api

api_blueprint = Blueprint('api', __name__)
api_v1 = Api(api_blueprint, doc='/docs')

from .account import account
api_v1.add_namespace(account)

from .admin import admin
api_v1.add_namespace(admin)

from .model import model
api_v1.add_namespace(model)

from .portfolio import portfolio
api_v1.add_namespace(portfolio)

from .trade import trade
api_v1.add_namespace(trade)

from .user import user
api_v1.add_namespace(user)

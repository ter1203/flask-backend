from functools import wraps
from flask import current_app, g, request
from flask.app import Flask
from libs.database import db_session
from apps.models import Business

def init_middlewares(app: Flask):
    '''Initialize app with middlewares'''

    @app.before_request
    def user_middleware():
        '''User middleware'''

        current_app.logger.debug(f'request params: {request.args}')
        current_app.logger.debug(f'request body: {request.json}')
        if request.method == 'GET' or request.method == 'DELETE':
            user = request.args['user_id'] if 'user_id' in request.args else None
        else:
            user = request.json['user_id'] if 'user_id' in request.json else None

        business: Business = db_session.query(Business).filter(Business.user_id == user).first()
        g.business = business
        if g.business:
            current_app.logger.debug(f'requesting business id: {g.business.id}')

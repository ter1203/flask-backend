from functools import wraps
from flask import current_app, g, abort, request
from flask.app import Flask


def init_middlewares(app: Flask):
    '''Initialize app with middlewares'''

    @app.before_request
    def user_middleware():
        '''User middleware'''

        current_app.logger.debug(f'request params: {request.args}')
        current_app.logger.debug(f'request body: {request.json}')
        if request.method == 'GET' or request.method == 'DELETE':
            g.user = request.args['user_id'] if 'user_id' in request.args else None
        else:
            g.user = request.json['user_id'] if 'user_id' in request.json else None

        if g.user:
            current_app.logger.debug(f'requesting user id: {g.user}')

from functools import wraps
from flask import current_app, g, abort, request
from flask.app import Flask
from libs.depends.entry import container
from libs.roles import RoleValues
from apps.auth.lib.auth.authenticator import Authenticator

def init_middlewares(app: Flask):
    '''Initialize app with middlewares'''

    @app.before_request
    def auth_middleware():
        '''Authentication middleware

        Get Authorization-Bearer token
        '''

        current_app.logger.debug(f'auth-middleware is running ...')
        g.user = None

        authenticator: Authenticator = container.get(Authenticator)
        g.user = authenticator.get_user_from_authorization(request)

        if g.user:
            current_app.logger.debug(f'authenticated user: {g.user.as_dict()}')


def login_required():
    def _decorated_view(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            if g.user is None:
                abort(401, 'Not authorized')

            return view(*args, **kwargs)

        return wrapped_view

    return _decorated_view


def active_required():
    def _decorated_view(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            if not g.user.active:
                abort(401, 'Not activated user')

            return view(*args, **kwargs)

        return wrapped_view

    return _decorated_view


def admin_required():
    def _decorated_view(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            roles = g.user.roles
            for role in roles:
                if role.name == RoleValues.admin.value:
                    return view(*args, **kwargs)

            abort(401, 'Not an admin')

        return wrapped_view

    return _decorated_view


def premium_required():
    def _decorated_view(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            roles = g.user.roles
            for role in roles:
                if role.name == RoleValues.premium.value:
                    return view(*args, **kwargs)

            abort(401, 'Not a premium user')

        return wrapped_view

    return _decorated_view

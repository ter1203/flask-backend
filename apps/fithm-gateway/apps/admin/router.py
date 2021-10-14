from flask_restx import Namespace, Resource
from flask import request
from libs.middleware.auth import login_required, active_required, admin_required
from libs.depends.entry import container
from .lib.parser import AdminParser
from .view import AdminView

admin = Namespace('admin', path='/admin', decorators=[admin_required(), active_required(), login_required()])
view = AdminView()

@admin.route('/users')
class Admin(Resource):

    @admin.doc('get all users')
    def get(self):

        parser: AdminParser = container.get(AdminParser)
        args = parser.parse_get_users(request)

        return view.get_users(args['page'], args['page_size'])

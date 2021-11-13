from flask_restx import Namespace, Resource
from flask import request
from libs.middleware.auth import login_required, active_required, admin_required
from libs.depends.entry import container
from .lib.parser import AdminParser
from .view import AdminView

admin = Namespace('admin', path='/admin', decorators=[admin_required(), active_required(), login_required()])
view = AdminView()

@admin.route('/users')
class AdminUserList(Resource):

    @admin.doc('get all users')
    def get(self):

        parser: AdminParser = container.get(AdminParser)
        args = parser.parse_get_users(request)

        return view.get_users(args['page'], args['page_size'])


@admin.route('/users/<int:user_id>')
class AdminUser(Resource):

    @admin.doc('get user detail')
    def get(self, user_id: int):

        return view.get_user(user_id)


    @admin.doc('update user detail')
    def put(self, user_id: int):

        parser: AdminParser = container.get(AdminParser)
        body = parser.parse_update_user(request)

        return view.update_user(user_id, body)


    @admin.doc('delete a user')
    def delete(self, user_id: int):

        return view.delete_user(user_id)

from flask_restx import Namespace, Resource
from flask import request
from .lib.parser import UserParser
from .view import UserView
from libs.depends.entry import container
from libs.middleware.auth import login_required, active_required


user = Namespace('user', path='/users', decorators=[active_required(), login_required()])
view = UserView()


@user.route('')
class UserResource(Resource):
    '''User update, delete'''

    @user.doc('update user')
    @login_required()
    @active_required()
    def put(self):

        parser: UserParser = container.get(UserParser)
        param = parser.parse_update(request)

        return view.update(param)


    @user.doc('delete user')
    @login_required()
    @active_required()
    def delete(self):

        return view.delete()

from flask_restx import Namespace, Resource

admin = Namespace('admin')


@admin.route('/')
class Admin(Resource):

    @admin.doc('admin healthy')
    def get(self):

        return f'Welcome admin'

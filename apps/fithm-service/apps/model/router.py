from flask_restx import Namespace, Resource

model = Namespace('model', path='/models')


@model.route('/')
class Models(Resource):

    @model.doc('model healthy')
    def get(self):
        '''List all models'''

        return f'Welcome model'

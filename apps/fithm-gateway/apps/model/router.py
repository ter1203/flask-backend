from flask_restx import Namespace, Resource
from flask import request
from libs.helper.forward import forward_request
from libs.middleware.auth import login_required, active_required
from libs.depends.entry import container
from .lib.parser import ModelParser

model = Namespace('model', path='/models', decorators=[active_required(), login_required()])

@model.route('')
class ModelList(Resource):

    @model.doc('get all models')
    def get(self):

        parser: ModelParser = container.get(ModelParser)
        params = parser.parse_create(request)

        return forward_request(params=params)


    @model.doc('create a model')
    def post(self):

        parser: ModelParser = container.get(ModelParser)
        body = parser.parse_create(request)

        return forward_request(body=body)


@model.route('/<int:model_id>')
class Model(Resource):

    @model.doc('get a model')
    def get(self, model_id: int):
        
        return forward_request()


    @model.doc('update a model')
    def put(self, model_id: int):

        parser: ModelParser = container.get(ModelParser)
        body = parser.parse_create(request)

        return forward_request(body=body)


    @model.doc('delete a model')
    def delete(self, model_id: int):

        return forward_request()


@model.route('/<int:model_id>/position')
class ModelPosition(Resource):

    @model.doc('update a model position')
    def put(self, model_id: int):

        parser: ModelParser = container.get(ModelParser)
        body = parser.parse_update_positions(request)

        return forward_request(body=body)

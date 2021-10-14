from flask_restx import Namespace, Resource
from flask import request
from .view import ModelView

model = Namespace('model', path='/models')
view = ModelView()

@model.route('')
class ModelList(Resource):

    @model.doc('get all models')
    def get(self):

        return view.get_models(request.args)


    @model.doc('create a model')
    def post(self):

        return view.create_model(request.json)


@model.route('/<int:model_id>')
class Model(Resource):

    @model.doc('get a model')
    def get(self, model_id: int):

        return view.get_model(model_id)


    @model.doc('update a model')
    def put(self, model_id: int):

        return view.update_model(model_id, request.json)


    @model.doc('delete a model')
    def delete(self, model_id: int):

        return view.delete_model(model_id)


@model.route('/<int:model_id>/position')
class ModelPosition(Resource):

    @model.doc('update a model position')
    def put(self, model_id: int):

        return view.update_model_position(model_id, request.json)

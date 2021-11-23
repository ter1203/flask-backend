from flask import current_app, g, abort
from libs.database import db_session
from apps.models import Model, Business, ModelPosition, Pending
import pandas
from libs.database import helpers

class ModelView:
    
    def __init__(self):
        pass


    def get_models(self, args: dict) -> list:
        '''Get all models for the user'''

        business: Business = g.business
        public = args['public'] == 'true'
        current_app.logger.debug(args['public'])
        models: list[Model] = (
            self.public_models() if public
            else filter(lambda model: not model.is_public, business.models)
        )
        return {
            'models': [model.as_dict() for model in models]
        }


    def create_model(self, body: dict) -> dict:
        '''Create a new model for the user'''

        public = body['public']
        model = Model(
            business_id=g.business.id,
            name=body['name'],
            description=body['description'],
            keywords=body['keywords'],
            is_public=public
        )
        db_session.add(model)
        db_session.commit()

        return model.as_dict()


    def get_model(self, id: int) -> dict:
        '''Get a specific model with id'''

        model = self.__get_model(id)
        return model.as_dict()


    def update_model(self, id: int, body: dict) -> dict:
        '''Update a model with body'''

        model = self.__get_model(id)
        model.name = body['name']
        model.keywords = body['keywords']
        model.is_public = body['public']
        model.description = body['description']

        db_session.commit()

        return model.as_dict()


    def delete_model(self, id: int):
        '''Delete a model'''

        model = self.__get_model(id)
        pendings = model.pendings
        db_session.delete(model)
        db_session.commit()
        helpers.update_trade_for_portfolio_model(pendings)

        return {
            'result': 'success'
        }


    def update_model_position(self, id: int, body: dict) -> dict:

        positions: list[ModelPosition] = []
        for pos in body['positions']:
            positions.append(ModelPosition(
                model_id=id,
                symbol=pos['symbol'],
                weight=pos['weight']
            ))

        model = self.__get_model(id)
        model.allocation = positions
        db_session.commit()

        pendings: list[Pending] = model.pendings
        helpers.update_trade_for_portfolio_model(pendings)

        return model.as_dict()


    def public_models(self) -> list[Model]:

        return db_session.query(Model).filter(Model.is_public == True).all()


    def __get_model(self, id: int) -> Model:

        model = db_session.query(Model).get(id)
        if not model:
            abort(404, 'Model not found')
        if model.business_id != g.business.id:
            abort(403, "You don't have permission to this model.")

        return model

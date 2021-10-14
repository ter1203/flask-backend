from flask import current_app, g

class ModelView:
    
    def __init__(self):
        pass


    def get_models(self, params: dict) -> list:
        '''Get all models for the user'''

        return ['models']


    def create_model(self, params: dict) -> dict:
        '''Create a new model for the user'''

        return {'create': 'model'}


    def get_model(self, id: int) -> dict:
        '''Get a specific model with id'''

        return f'model_{id}'


    def update_model(self, id: int, body: dict) -> dict:
        '''Update a model with body'''

        return f'model_update: {body}'


    def delete_model(self, id: int):
        '''Delete a model'''

        return f'model_delete: {id}'


    def update_model_position(self, id: int, body: dict) -> dict:

        return f'update_model_position: {body}'

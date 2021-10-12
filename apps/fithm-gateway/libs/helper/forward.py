from flask import request, current_app
import requests


def forward_request() -> str:
    req_path = request.path
    base_url = current_app.config['SERVICE_URL']

    url = f'{base_url}{req_path}'
    body = request.json
    params = request.args
    method = request.method

    current_app.logger.debug(f'url = {url}, method = {method}')
    return requests.request(method, url, params=params, json=body).json()

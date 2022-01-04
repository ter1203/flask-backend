from typing import Optional, Dict
from flask import json, request, current_app, g, abort
import requests


def forward_request(body: Optional[Dict] = None, params: Optional[Dict] = None) -> str:
    req_path = request.path
    base_url = current_app.config['SERVICE_URL']

    url = f'{base_url}{req_path}'
    if not body:
        body = request.json or {}
    if not params:
        params = request.args or {}
    method = request.method

    if g.user and hasattr(g.user, 'id'):
        if method == 'PUT' or method == 'POST':
            body['user_id'] = g.user.id
        elif method == 'GET' or method == 'DELETE':
            params['user_id'] = g.user.id

    current_app.logger.debug(f'url = {url}, method = {method}, params = {params}, body = {body}')
    response = requests.request(method, url, params=params, json=body)
    if response.status_code == 200:
        return response.json()
    else:
        abort(response.status_code, response.content.decode('utf8'))

from typing import Optional, Dict
from flask import request, current_app, g
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
    return requests.request(method, url, params=params, json=body).json()

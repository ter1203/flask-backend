from typing import Optional, Dict
from flask import request, current_app
import requests


def forward_request(body: Optional[Dict] = None) -> str:
    req_path = request.path
    base_url = current_app.config['SERVICE_URL']

    url = f'{base_url}{req_path}'
    if not body:
        body = request.json
    params = request.args
    method = request.method

    current_app.logger.debug(f'url = {url}, method = {method}')
    return requests.request(method, url, params=params, json=body).json()

from flask import current_app
import requests as req
from apps.models import User


def delete_quovo_user(quovo_user_id):
    head = {"Authorization": "Bearer " + current_app.config['FITHM_QUOVO_KEY']}
    status = req.delete("https://api.quovo.com/v3/users/" +
                        str(quovo_user_id), headers=head)
    return status


def get_quovo(path):
    base = 'https://api.quovo.com/v3/'
    head = {"Authorization": "Bearer " + current_app.config['FITHM_QUOVO_KEY']}
    url = base + path
    return req.get(url, headers=head).json()


def post_quovo(path, add_json_header=False, body=None):
    base = 'https://api.quovo.com/v3/'
    head = {"Authorization": "Bearer " + current_app.config['FITHM_QUOVO_KEY']}
    if add_json_header:
        head['Content-Type'] = "application/json"
    url = base + path
    if body:
        return req.post(url, headers=head, data=body).json()
    return req.post(url, headers=head).json()


def set_quovo_account_list(user: User, quovo_response, manual=None):
    new_list = [{'broker_name': r['institution_name'],
                 'account_number': 'quovo_' + str(r['id'])} for r in quovo_response]
    if manual:
        new_list.extend(manual)
    return req.post(
        current_app.config['API_BASE_URL'] + '/account/user_accounts/' + user.tradeshop_id,
        json={'account_list': new_list}).json()

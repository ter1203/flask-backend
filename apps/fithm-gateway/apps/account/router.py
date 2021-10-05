from flask import Blueprint
from flask import request, g

account = Blueprint('account', __name__)


@account.route('', methods=['GET', 'POST'])
def accounts():
	return 'account blueprint'
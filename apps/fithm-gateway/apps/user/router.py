from flask import Blueprint, request, g
from libs.database import db_session

user = Blueprint('user', __name__)

@user.route('/', methods=['GET', 'POST'])
def index():
	'''Get users or create a user'''

	if request.method == 'GET':
		return 'No users'
	else:
		return 'Creating user'

from apps.models import Role, RolesUsers, User
from apps.auth.lib.auth.authenticator import Authenticator
from libs.depends.register import container
from libs.roles import RoleValues
from . import db_session
from settings import FITHM_ADMIN_MAIL, FITHM_ADMIN_PASS

def default_values():
    '''Populate default values'''

    admin_count = db_session.query(User).filter(User.username == 'admin').count()
    if admin_count:
        return

    # add roles
    admin_role = Role(
        name=RoleValues.admin.value,
        description='System administrator'
    )
    basic_role = Role(
        name=RoleValues.basic.value,
        description='General user'
    )
    premimu_role = Role(
        name = RoleValues.premium.value,
        description='Premium user with more abilities'
    )
    db_session.add(admin_role)
    db_session.add(basic_role)
    db_session.add(premimu_role)

    # add admin user
    authenticator: Authenticator = container.get(Authenticator)
    admin = User(
        email=FITHM_ADMIN_MAIL,
        username='admin',
        password=authenticator.hash_password(FITHM_ADMIN_PASS),
        active=True
    )
    db_session.add(admin)
    db_session.commit()

    role1 = RolesUsers(user_id=admin.id, role_id=admin_role.id)
    role2 = RolesUsers(user_id=admin.id, role_id=basic_role.id)
    db_session.add(role1)
    db_session.add(role2)

    db_session.commit()

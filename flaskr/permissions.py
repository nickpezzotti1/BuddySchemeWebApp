from flask import current_app
from flask_login import LoginManager, current_user
from functools import wraps

def permissioned_login_required(role="ANY", login_manager=None):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if ((current_user.role != role) and (role != "ANY")):
                return login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

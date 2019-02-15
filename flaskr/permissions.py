from flask import redirect
from flask_login import current_user
from functools import wraps

def permissioned_login_required(role="ANY", redirect_on_fail="/dashboard"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(redirect_on_fail)
            if ((current_user.role != role) and (role != "ANY")):
                return redirect(redirect_on_fail)
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

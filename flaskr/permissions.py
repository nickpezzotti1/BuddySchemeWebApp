from flask import redirect
from flask_login import current_user
from functools import wraps

def permissioned_login_required(role="ANY", redirect_on_fail="/"):
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


def admin_login_required(redirect_on_fail = '/'):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(redirect_on_fail)
            if (current_user.priv != 'admin' and current_user.priv != 'system_admin'):
                print(current_user.priv)
                return redirect(redirect_on_fail)
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

def system_admin_login_required(redirect_on_fail = '/system'):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(redirect_on_fail)
            if (current_user.priv != 'system_admin'):
                print(current_user.priv)
                return redirect(redirect_on_fail)
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

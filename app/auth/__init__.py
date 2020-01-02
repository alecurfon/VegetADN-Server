from flask import request, abort
from app.models import User, WhitelistToken
from functools import wraps
import os, sys

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth_token = None
        if 'Authorization' in request.headers:
            auth_token = request.headers['Authorization'].split(" ")[1]
        if not auth_token:
            abort(401, 'The session token is missing')
        try:
            if not WhitelistToken.check_whitelist(auth_token):
                abort(401, 'The session token is not valid')
            user_id = User.decode_auth_token(auth_token)
            current_user = User.query.filter(User.id == user_id).first()
        except Exception as e:
            abort(401, 'The session token is not valid or has expired')
        return func(*args, **kwargs)
    return decorated

def admin_token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth_token = None
        if 'Authorization' in request.headers:
            auth_token = request.headers['Authorization'].split(" ")[1]
        if not auth_token:
            abort(401, 'The session token is missing')
        try:
            if not WhitelistToken.check_whitelist(auth_token):
                abort(401, 'The session token is not valid')
            user_id = User.decode_auth_token(auth_token)
            current_user = User.query.filter(User.id == user_id).first()
            admin = current_user.admin
            if not admin:
                abort(401, 'The session token does not have administrator permission')
        except Exception as e:
            abort(401, 'The session token is not valid or has expired')
        return func(*args, **kwargs)
    return decorated

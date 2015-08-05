from flask import Blueprint, render_template, redirect, url_for, request, Response, flash, session
from sqlalchemy import desc
from sqlalchemy.sql import collate
from functools import wraps
from flask.ext.security import login_required


from app import db
from .donotpushme import validate_user
    
    
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not validate_user(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})    
from flask import Blueprint, render_template, redirect, url_for, request, Response
from sqlalchemy import desc
from sqlalchemy.sql import collate
from functools import wraps

from app import db



mod_login = Blueprint('login', __name__, url_prefix='/',
                       template_folder='templates')


@mod_login.route('/')
def landing_page():
        return render_template('login.html')

@mod_login.route('auth', methods=['POST', 'GET'])
def auth():
    username = request.form.get("username")
    password = request.form.get("password")
       	return redirect(url_for('.landing_page'))
    return redirect(url_for('.landing_page'))

def check_user(username, password):
	return username == "Admin" and password == "test"    	
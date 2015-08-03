from flask import Blueprint, render_template, redirect, url_for, request, Response, flash, session
from sqlalchemy import desc
from sqlalchemy.sql import collate
from functools import wraps

from app import db

from app.players.routes import display_players


mod_login = Blueprint('login', __name__, url_prefix='/',
                       template_folder='templates')


@mod_login.route('/')
def landing_page():
        return render_template('login.html')

@mod_login.route('auth', methods=['POST', 'GET'])
def auth():
    username = request.form.get("username")
    password = request.form.get("password")
    if validate_user(username, password):
        session['logged_in'] = True
        return display_one_player()
    else:
        flash('Wrong password shithead')
    return redirect(url_for('.landing_page'))

def validate_user(username, password):
	return username == "Admin" and password == "test"    	
    
    
@mod_login.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('.landing_page'))
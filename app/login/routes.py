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

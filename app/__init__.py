# Import flask and template operators
from flask import Flask, render_template, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy

import logging
import chartkick


# Define the WSGI application object
app = Flask(__name__)


# Configurations
app.config.from_object('config')
app.logger.setLevel(logging.DEBUG)

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error=error), 404
    
db = SQLAlchemy(app)
    
# Import Blueprint modules.
from app.sessions.routes import mod_sessions
from app.players.routes import mod_players
from app.missions.routes import mod_missions


ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')

# Register Blueprint(s)
app.register_blueprint(mod_sessions)
app.register_blueprint(mod_players)
app.register_blueprint(mod_missions)
app.register_blueprint(ck, url_prefix='/ck')
app.jinja_env.add_extension("chartkick.ext.charts")


db.create_all(bind=['ark_a2'])
db.create_all(bind=['compass'])
db.create_all(bind=['ark_forums'])


# pass into database, its first run
from app.loader import loader
loader.loader()
# Import flask and template operators
from flask import Flask, render_template, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy

import logging

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
from app.parser.routes import mod_parser
from app.parser.routes import mod_players


# Register Blueprint(s)
app.register_blueprint(mod_parser)
app.register_blueprint(mod_players)



db.create_all(bind=['ark_a2'])
db.create_all(bind=['ast'])
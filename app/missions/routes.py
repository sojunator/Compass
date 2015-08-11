from flask import Blueprint, render_template, redirect, url_for, request, Response
from sqlalchemy import desc
from functools import wraps
from itertools import chain

from app import db

from app.database.database import Mission, Player, AIMovement, PlayerMovement, PlayerDisconnect, func, CmpPlayer
from app.sessions.models import Session, SessionMission
from app.login.routes import requires_auth


mod_missions = Blueprint('missions', __name__, url_prefix='/missions',
                       template_folder='templates')


@mod_missions.route('/')
@requires_auth
def display_missions():
	missions = db.session.query(Mission).all()

	session_missions = [mission for mission in missions if is_session_mission(mission)]

	unique_missions = list(set(missions))

	return render_template('missions.html', missions=unique_missions)

def is_session_mission(mission):
	return ((mission.created.weekday() in [5,6]) and ((mission.created.hour >= 18) or (mission.created.hour <= 5)))
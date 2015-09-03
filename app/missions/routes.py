from flask import Blueprint, render_template, redirect, url_for, request, Response
from sqlalchemy import desc
from functools import wraps
from itertools import chain
from collections import Counter

import os
import re

from werkzeug import secure_filename
from app import db
from app import app

from app.database.database import Mission, Player, AIMovement, PlayerMovement, PlayerDisconnect, func, CmpPlayer
from app.sessions.models import Session, SessionMission
from app.login.routes import requires_auth
from .models import MissionData, PBO


mod_missions = Blueprint('missions', __name__, url_prefix='/missions',
                       template_folder='templates')


@mod_missions.route('/', methods=['GET', 'POST'])
@requires_auth
def display_missions():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			temp_mission = PBO(file)

	session_missions = missions_in_db()
	folder_missions = missions_in_folder()

	counted_missions = Counter(session_missions)
	missions_data = []

	for key, value in counted_missions.items():
		if key.mission_name in folder_missions:
			missions_data.append(MissionData(key.mission_name, value))
		else:
			print(key.mission_name)


	for mission in folder_missions:
		if mission not in missions_data:
			missions_data.append(MissionData(mission, 0))

	print (len(folder_missions), " ", len(session_missions), " ", len(missions_data))

	missions_data.sort(key=lambda x: x.last_datetime, reverse=True)

	return render_template('missions.html', missions=missions_data)

def is_session_mission(mission):
	return ((mission.created.weekday() in [5,6]) and ((mission.created.hour >= 18) or (mission.created.hour <= 5)) and not len(mission.mission_name.split("_")) < 3)

def missions_in_folder():
	folder_missions = []

	for file in os.listdir("C:/dev/python/arma2oa/MPMissions"):
		if file.endswith(".pbo"):
			temp_name = re.sub('(?:[.](.*)|_[vV]([0-9]+(.*))?)', '', file)
			folder_missions.append(temp_name)

	return folder_missions

def missions_in_db():
	missions = db.session.query(Mission).all()
	session_missions = [mission for mission in missions if is_session_mission(mission)]

	for mission in session_missions:
		mission.mission_name = re.sub('(_[vV]([0-9]+)?)$', '', mission.mission_name)

	return session_missions


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['pbo'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
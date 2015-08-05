from flask import Blueprint, render_template, redirect, url_for, request, Response
from sqlalchemy import desc
from sqlalchemy.sql import collate
from functools import wraps

from app import db

from .database import Mission, Player, AIMovement, PlayerMovement, PlayerDisconnect, func, AstPlayer
from .models import Session, SessionMission
from app.login.routes import requires_auth


import time
import collections
import json


mod_sessions = Blueprint('sessions', __name__, url_prefix='/sessions',
                       template_folder='templates')


# Section for handling missions and sessions
@mod_sessions.route('/')
@requires_auth
def get_sessions():
    missions = db.session.query(Mission).all()

    session_missions = []
    for mission in missions:
        # If on a session date (Saturday going on Sunday for A2)
        if ((mission.created.weekday() in [5, 6]) and ((mission.created.hour >= 18) or (mission.created.hour <= 5))):
            session_missions.append(mission)
    
    sessions_unsorted = {}
    for mission in session_missions:
        year, week, __ = mission.created.isocalendar()

        key = (year, week)
        if key not in sessions_unsorted:  # Create a new key/value pair
            sessions_unsorted[key] = Session()

            player_count = (db.session.query(func.count(Player.id))
                            .join(Mission).filter(Mission.id == mission.id, 
                                                  Player.is_jip == False)
                            .first())[0]
            temp_mission = SessionMission(mission, player_count)
            sessions_unsorted[key].add_mission(temp_mission)
        else:  # Use existing key/value pair
            player_count = (db.session.query(func.count(Player.id))
                            .join(Mission).filter(Mission.id == mission.id, 
                                                  Player.is_jip == False)
                            .first())[0]
            temp_mission = SessionMission(mission, player_count)
            sessions_unsorted[key].add_mission(temp_mission)
     
    # Sort the dictionary and only retrieve.
    sorted_sessions = sorted(sessions_unsorted.items(), key=lambda t: t[0])

    return render_template('overview.html', sessions=sorted_sessions)


@mod_sessions.route('/<year>/<week>')
def display_session(year, week):  
    missions = db.session.query(Mission).all()
    week = int(week)
    year = int(year)

    session_missions = []
    for mission in missions:
        if ((mission.created.isocalendar()[1] == week)
            and (mission.created.year == year) 
            and (mission.created.weekday() in [5, 6]) # Missin in a sat or sunday
            and ((mission.created.hour >= 18) or (mission.created.hour <= 5))): # if it was played between 18 and 5
                session_missions.append(mission)

    # Sort mission after played order
    session_missions.sort(key=lambda r: r.created)

    return render_template('session.html', session=session_missions)
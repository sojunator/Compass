from flask import Blueprint

from app import db

from .database import Mission, Player, AIMovement, PlayerMovement, PlayerDisconnect, func
from .models import Session, SessionMission

import collections
import json



mod_parser = Blueprint('parser', __name__, url_prefix='/parser',
                       template_folder='templates')


@mod_parser.route('/')
def get_sessions():
    missions = db.session.query(Mission).all()
    
    session_missions = []
    for mission in missions:
        # If on a session date (Saturday going on Sunday for A2)
        if (mission.created.weekday() in [5, 6]) and ((mission.created.hour >= 18) or (mission.created.hour <= 5)):
            session_missions.append(mission)
            
    sessions = {}
    for mission in session_missions:
        year, week, __ = mission.created.isocalendar() # We only want the week and the year
        
        key = (year, week)
        if key not in sessions: # Create a new key
            sessions[key] = Session()
            player_count = (db.session.query(func.count(Player.id)).join(Mission).filter(Mission.id == mission.id).first())[0]
            temp_mission = SessionMission(mission, player_count)
            sessions[key].add_mission(temp_mission)
        else: # use existing key
            player_count = (db.session.query(func.count(Player.id)).join(Mission).filter(Mission.id == mission.id).first())[0]
            temp_mission = SessionMission(mission, player_count)
            sessions[key].add_mission(temp_mission)
            
    sorted_sessions = sorted(sessions.items(), key=lambda t: t[0]) # sort shit out
      
    return str(sorted_sessions)
from flask import Blueprint
from app import db
from .models import Mission, Player, AIMovement, PlayerMovement, PlayerDisconnect

mod_parser = Blueprint('parser', __name__, url_prefix='/parser',
                       template_folder='templates')


@mod_parser.route('/')
def get_sessions():
    missions = db.session.query(Mission).all()
    
    session_missions = []
    for mission in missions:
        # If on a session date (Saturday going on Sunday for A2)
        if (mission.created.weekday() in [5, 6]) and ((mission.created.hour >= 18) or (mission.created.hour <= 5)):
            session_mission.append(mission)
            
    sessions = {}
    for mission in session_missions:
        year, week, __ = mission.created.isocalendar()
        
        key = (year, week)
        if key not in sessions:
            sessions[key] = [mission]
        else:
            sessions[key].append(mission)
            
    return str(sessions)

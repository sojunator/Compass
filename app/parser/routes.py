from flask import Blueprint, render_template
from sqlalchemy import desc
from sqlalchemy.sql import collate

from app import db

from .database import Mission, Player, AIMovement, PlayerMovement, PlayerDisconnect, func, AstPlayer
from .models import Session, SessionMission

import time
import collections
import json
import requests

mod_parser = Blueprint('parser', __name__, url_prefix='/parser',
                       template_folder='templates')


# Section for handling missions and sessions
@mod_parser.route('/')
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
                            .join(Mission).filter(Mission.id == mission.id, Player.is_jip == False)
                            .first())[0]
            temp_mission = SessionMission(mission, player_count)

            sessions_unsorted[key].add_mission(temp_mission)
        else:  # Use existing key/value pair
            player_count = (db.session.query(func.count(Player.id))
                            .join(Mission).filter(Mission.id == mission.id, Player.is_jip == False)
                            .first())[0]
            temp_mission = SessionMission(mission, player_count)

            sessions_unsorted[key].add_mission(temp_mission)

    # Sort the dictionary and only retrieve.
    sorted_sessions = sorted(sessions_unsorted.items(), key=lambda t: t[0])

    return render_template('parser.html', sessions=sorted_sessions)


mod_players = Blueprint('players', __name__, url_prefix='/players',
                       template_folder='templates')


# Section for getting players from ark_a2 and push them into AstPlayer table
@mod_players.route('/', methods=['GET', 'POST'])
def display_players(): 
    players_in_database = db.session.query(AstPlayer).order_by(collate(AstPlayer.last_played, 'NOCASE')).all()
    return render_template('players.html', players=players_in_database)




# Section for getting players from ark_a2 and push them into AstPlayer table
@mod_players.route('/<username>')
def display_one_player(username): 
    return 'User %s' % username
    
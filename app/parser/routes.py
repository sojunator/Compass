from flask import Blueprint, render_template, redirect, url_for, request, Response
from sqlalchemy import desc
from sqlalchemy.sql import collate
from functools import wraps

from app import db

from .database import Mission, Player, AIMovement, PlayerMovement, PlayerDisconnect, func, AstPlayer
from .models import Session, SessionMission

import time
import collections
import json


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
@mod_players.route('/')
def display_players():
    players_in_database = db.session.query(AstPlayer).order_by(collate(AstPlayer.last_played, 'NOCASE')).all()
    return render_template('players.html', players=players_in_database)

@mod_players.route('/submit/<username>', methods=['POST'])
def submit_notes(username):
    if username is None:
        return redirect(url_for('.display_players'))
    
    notes = request.form['notes']
    print("The username",username,"The notes",notes)

    player = db.session.query(AstPlayer).filter(AstPlayer.player_name == username).first()
    
    player.staff_notes = notes
    
    db.session.commit()
    

    
    return redirect(url_for('.display_players'))
        

# Section for getting players from ark_a2 and push them into AstPlayer table
@mod_players.route('/<username>')
def display_one_player(username): 
    displayed_player = db.session.query(AstPlayer).filter(AstPlayer.player_name == username).first()
    all_players_arma = db.session.query(Player).filter(Player.player_name == username).all() 
    selected_player_arma = [player for player in all_players_arma if ((player.created.weekday() in [5, 6]) and ((player.created.hour >= 18) or (player.created.hour <= 5)) and (player.is_jip == False) and (player.player_name == username))]
    
    player_roles = []
    
    for player in selected_player_arma:
            player_roles.append(player.hull_gear_class)
    
    unique_roles = set(player_roles)
    
    data = dict.fromkeys(unique_roles, 0)
    
    for role in player_roles:
        data[role] = (data[role] + 1)
    
    
    return render_template('profile.html', player=displayed_player, data=data)


mod_login = Blueprint('login', __name__, url_prefix='/',
                       template_folder='templates')



@mod_login.route('/')
def landing_page():
        return render_template('login.html')

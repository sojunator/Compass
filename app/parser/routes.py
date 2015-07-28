from flask import Blueprint, render_template

from app import db

from .database import Mission, Player, AIMovement, PlayerMovement, PlayerDisconnect, func, AstPlayer
from .models import Session, SessionMission

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
                            .join(Mission).filter(Mission.id == mission.id)
                            .first())[0]
            temp_mission = SessionMission(mission, player_count)

            sessions_unsorted[key].add_mission(temp_mission)
        else:  # Use existing key/value pair
            player_count = (db.session.query(func.count(Player.id))
                            .join(Mission).filter(Mission.id == mission.id)
                            .first())[0]
            temp_mission = SessionMission(mission, player_count)

            sessions_unsorted[key].add_mission(temp_mission)

    # Sort the dictionary and only retrieve.
    sorted_sessions = sorted(sessions_unsorted.items(), key=lambda t: t[0])

    return render_template('parser.html', sessions=sorted_sessions)


mod_players = Blueprint('players', __name__, url_prefix='/players',
                       template_folder='templates')


# Section for handling missions and sessions
@mod_players.route('/')
def get_players():    
    # TODO: once the insertion into db works, rewrite initial procedure
    # so that everything from AstPlayer table will be fetched only once and then compared for new entries from session
    # to minimize database calls
    
    players = db.session.query(Player).all() # get all players in ark_a2 db
    
    players_in_session = [] # will contain players objects from sessions
    
    players_in_database = db.session.query(AstPlayer.player_name).all()
    list(players_in_database)
    
    for player in players:
        if ((player.created.weekday() in [5, 6]) and ((player.created.hour >= 18) or (player.created.hour <= 5)) and player.player_name != "HC"):
            players_in_session.append(player)    
            if (players_in_session[-1].player_name not in players_in_database): # 
                temp_player = AstPlayer(player.player_name, player.player_uid) # create new player
                players_in_database.append(player.player_name)
                db.session.add(temp_player)    

                
    db.session.commit()        
    return str(players_in_database)

    
           # if (db.session.query(AstPlayer).filter(player.player_uid==AstPlayer.player_uid).first() is None):
            #    temp_player = AstPlayer(player.player_name, player.player_uid) # create new player
            #    db.session.add(temp_player)    
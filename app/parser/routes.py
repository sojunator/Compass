from flask import Blueprint, render_template
from sqlalchemy import desc
from sqlalchemy.sql import collate

from app import db

from .database import Mission, Player, AIMovement, PlayerMovement, PlayerDisconnect, func, AstPlayer
from .models import Session, SessionMission

import collections
import json
import itertools

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
            
    print (len(session_missions)) 
    
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
def get_players():    
    # TODO: Figure out how many missions the players has played
    #       Show last played session
    #       The database will only load a player once and only once. Either drop Astplayer table and reload all data
    #       Or get a struck of genius
    
    players = db.session.query(Player).all() # get all players in ark_a2 db - tuplet
    
    players_in_session = [] # will contain players objects from sessions - list 
    
    players_in_database = list(itertools.chain(*db.session.query(AstPlayer.player_name).all())) # covert it to a list
    
    
    for player in players:
        if ((player.created.weekday() in [5, 6]) and ((player.created.hour >= 18) or (player.created.hour <= 5)) and (player.player_name not in ["HC", "Error: No unit"])):
            players_in_session.append(player)    
            if (players_in_session[-1].player_name not in players_in_database):  # Since the player was in the session, lets see if he is new or not
                missions_played = (db.session.query(Player)
                    .filter_by(player_name=players_in_session[-1].player_name, is_jip=False).count())
                temp_player = AstPlayer(player.player_name, player.player_uid, missions_played) # create new player
                players_in_database.append(player.player_name)
                db.session.add(temp_player)    
                
        
    db.session.commit()   
    players_in_database = db.session.query(AstPlayer).order_by(collate(AstPlayer.player_name, 'NOCASE')).all()
    return render_template('players.html', players=players_in_database)
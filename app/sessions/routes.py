from flask import Blueprint, render_template, redirect, url_for, request, Response
from sqlalchemy import desc
from sqlalchemy.sql import collate
from functools import wraps

from app import db

from .database import Mission, Player, AIMovement, PlayerMovement, PlayerDisconnect, func, AstPlayer
from .models import Session, SessionMission, GroupsInMission
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
            temp_mission = SessionMission(mission, player_count, None, None)
            sessions_unsorted[key].add_mission(temp_mission)
        else:  # Use existing key/value pair
            player_count = (db.session.query(func.count(Player.id))
                            .join(Mission).filter(Mission.id == mission.id, 
                                                  Player.is_jip == False)
                            .first())[0]
            temp_mission = SessionMission(mission, player_count, None, None)
            sessions_unsorted[key].add_mission(temp_mission)
     
    # Sort the dictionary and only retrieve.
    sorted_sessions = sorted(sessions_unsorted.items(), key=lambda t: t[0], reverse=True)

    return render_template('overview.html', sessions=sorted_sessions)


@mod_sessions.route('/<year>/<week>')
def display_session(year, week):  
    missions = db.session.query(Mission).all()
    week = int(week)
    year = int(year)

    session_missions = []

    for mission in missions:
        if ((mission.created.isocalendar()[1] == week) # Find mission on the date we are looking on
            and (mission.created.year == year) 
            and (mission.created.weekday() in [5, 6]) # Missin in a sat or sunday
            and ((mission.created.hour >= 18) or (mission.created.hour <= 5))): # if it was played between 18 and 5
                players = db.session.query(Player).filter(
                                        Player.mission_id == mission.id, 
                                        Player.player_name is not "HC", 
                                        Player.is_jip == False).all()

                player_count = (db.session.query(func.count(Player.id)) 
                            .join(Mission).filter(Mission.id == mission.id, 
                                                  Player.is_jip == False)
                            .first())[0]

                groups = {}

                for player in players: # Find all groups in missio and place the players in them
                    key = player.group_name

                    if key not in groups: # If the key doesnt exist, create new
                        groups[key] = GroupsInMission()
                        groups[key].add_member(player)
                    else:                 # Use existing key
                        groups[key].add_member(player)

                for key in groups:
                    groups[key].sort_members


                temp_mission = SessionMission(mission, player_count, players, groups)
                session_missions.append(temp_mission)

    # Sort mission after played order
    session_missions.sort(key=lambda r: r.mission.created)

    data = {}

    for index, mission in enumerate(session_missions):
        data[index] = mission.playercount
    


    return render_template('session.html', session=session_missions, data=data)
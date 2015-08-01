from flask import Blueprint, render_template, redirect, url_for, request, Response
from sqlalchemy import desc
from sqlalchemy.sql import collate
from functools import wraps

from app import db

from app.parser.database import Mission, Player, AIMovement, PlayerMovement, PlayerDisconnect, func, AstPlayer
from app.parser.models import Session, SessionMission

import time
import collections
import json

mod_players = Blueprint('players', __name__, url_prefix='/players',
                       template_folder='templates')

@mod_players.route('/')
def display_players():
    players_in_database = db.session.query(AstPlayer).order_by(collate(AstPlayer.last_played, 'NOCASE')).all()
    return render_template('players.html', players=players_in_database)

@mod_players.route('/submit/<username>', methods=['POST'])
def submit_notes(username):
    if username is None:
        return redirect(url_for('.display_players'))
    
    notes = request.form['notes']

    player = db.session.query(AstPlayer).filter(AstPlayer.player_name == username).first()
    
    player.staff_notes = notes
    
    db.session.commit()
    
    return redirect(url_for('.display_players'))
        

@mod_players.route('/<username>')
def display_one_player(username):

    displayed_player = db.session.query(AstPlayer).filter(AstPlayer.player_name == username).first()
    if displayed_player is None:
        return redirect(url_for('.display_players'))
        
    all_players_arma = db.session.query(Player).filter(Player.player_name == username).all() 
    selected_player_arma = [player for player in all_players_arma if ((player.created.weekday() in [5, 6]) # Retrieve the player we are looking for from db
                                                                        and ((player.created.hour >= 18) or (player.created.hour <= 5)) 
                                                                        and (player.is_jip == False) 
                                                                        and (player.player_name == username))]
    
    player_roles = []
    
    for player in selected_player_arma:
            player_roles.append(player.hull_gear_class)
    
    unique_roles = set(player_roles)
    
    data = dict.fromkeys(unique_roles, 0)
    
    for role in player_roles:
        data[role] = (data[role] + 1)
    
    
    return render_template('profile.html', player=displayed_player, data=data)


from app import db

import time
from datetime import date
import datetime

from app.parser.database import Mission, Player, AIMovement, PlayerMovement, PlayerDisconnect, func, AstPlayer
from app.parser.models import Session, SessionMission

def loader():
    start_time = time.time()
    AstPlayer.query.delete()
    insert_players()
    print("--- %s seconds to start server ---" % (time.time() - start_time))
def insert_players():    
    players = db.session.query(Player).all() # get all players in ark_a2 db 
    
    players_in_session = [player for player in players if ((player.created.weekday() in [5, 6]) and ((player.created.hour >= 18) or (player.created.hour <= 5)) and (player.player_name not in ["HC", "Error: No unit", "Flash", "Namuthewhale", "SkinnyTar", "Sakai", "ratcatcher", "Tegyr", "Ricky", "ZeRandomTigre", "Wrathz", "Emaharg", "Pr3sario", "Shalun (2)", "Lucky"]))] # will contain players objects from sessions - list 
    players_in_database = [r[0] for r in db.session.query(AstPlayer.player_name).all()]
   
    for player in players_in_session:
        if (player.player_name not in players_in_database):  # Since the player was in the session, lets see if he is new or not
            players_in_database.append(player.player_name)    
            
            temp_player = AstPlayer(player_name=player.player_name, player_uid=player.player_uid, missions_played=1, last_played=player.created, danger_zone=False) # create new player
            db.session.add(temp_player)
        else:
            db_player = db.session.query(AstPlayer).filter(AstPlayer.player_name == player.player_name).first()
            db_player.missions_played += 1
            
            if db_player.last_played < player.created:
                db_player.last_played = player.created
                if player.created.isocalendar()[1] < (date.today().isocalendar()[1] - 2):
                    db_player.danger_zone = True
                else:
                    db_player.danger_zone = False  
                

        
    db.session.commit()   

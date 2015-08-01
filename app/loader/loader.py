from app import db

import time
from datetime import date
import datetime

from app.parser.database import Mission, Player, AIMovement, PlayerMovement, PlayerDisconnect, func, AstPlayer
from app.parser.models import Session, SessionMission

def loader():
    print("Starting server - This can take up to 10 seconds")
    
    start_time = time.time()
    insert_players()
    
    print("--- %s seconds to start server ---" % (time.time() - start_time))
    
def insert_players(): 
    print("Generating players")
    
    players = db.session.query(Player).all()                        # get all players from ark_a2 db 
    players_in_session = [player for player in players if ((player.created.weekday() in [5, 6]) 
                                                            and ((player.created.hour >= 18) or (player.created.hour <= 5)) 
                                                            and (player.is_jip == False) 
                                                            and (player.player_name not in ["HC", "Error: No unit", "Flash", 
                                                                                           "Namuthewhale", "SkinnyTar", "Sakai", 
                                                                                           "ratcatcher", "Tegyr", "Ricky", "ZeRandomTigre", 
                                                                                           "Wrathz", "Emaharg", "Pr3sario", "Shalun (2)", 
                                                                                           "Lucky"]))] 
                                                                                           
    player_name_in_database = [r[0] for r in db.session.query(AstPlayer.player_name).all()]
    player_object_in_database = db.session.query(AstPlayer).all()
    
    leadership_roles = [
        "CO","SL","FTL","MMGG",
        "MATG","HATG","SN","ENG",
        "VC"]
   
    for player in player_object_in_database:                        # Needs to be reset because we are not throwing the DB anymore
        player.played_leader = 0
        player.missions_played = 0
        player.deaths = 0
    
    db.session.commit()
   
    for player in players_in_session:
        
        if player.player_name not in player_name_in_database:       # Since the player was in the session, check if he is in the database.
            player_name_in_database.append(player.player_name)    
      
            temp_player = AstPlayer(player_name=player.player_name, # Insert him into the database
                                    player_uid=player.player_uid, missions_played=1, 
                                    last_played=player.created, 
                                    danger_zone=False, 
                                    player_rank="Regular", 
                                    deaths=0, 
                                    played_leader=0, 
                                    last_mission=player.mission_id, 
                                    staff_notes="")           
            db.session.add(temp_player)
        else:                                                       # He was in the database, update his values
            db_player = db.session.query(AstPlayer).filter(
                                                    AstPlayer.player_name == player.player_name
                                                    ).first()
                                                    
            db_player.missions_played += 1
            
            if player.hull_gear_class in leadership_roles:
                db_player.played_leader += 1
            
            if player.death is not None:
                db_player.deaths += 1
                
            if db_player.last_played < player.created:
                db_player.last_played = player.created
                db_player.last_mission = player.mission_id
                
                if player.created.isocalendar()[1] < (date.today().isocalendar()[1] - 2):
                    db_player.danger_zone = True
                else:
                    db_player.danger_zone = False  
                

        
    db.session.commit()   

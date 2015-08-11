from app import db, app

import time
from datetime import date
import datetime

from app.database.database import Mission, Player, AIMovement, PlayerMovement, PlayerDisconnect, func, CmpPlayer, ForumUser
from app.sessions.models import Session, SessionMission

LEADERSHIP_ROLES = ["CO", "SL", "FTL", "SN",
                    "MMGG", "MATG", "HATG",
                    "ENG", "VC"]


def loader():
    app.logger.info("[Loader] - Starting server - ETA: 7-10 seconds")

    start_time = time.time()
    insert_players()

    app.logger.info("[Loader] - {0} seconds taken to start server"
                    .format(time.time() - start_time))


def insert_players():
    app.logger.info("[Loader] - Generating AST Database")

    # Query the ARMA DB to get a list of all Player instances,
    # then filter out any Players who weren't in a session.
    session_players = [player for player in db.session.query(Player).all()
                       if in_session(player)]

    # Get a list of the CompassPlayers that already exist in our local DB.
    compass_players = db.session.query(CmpPlayer).all()
    user_ranks = {user.username_clean: user.show_rank() for user in db.session.query(ForumUser).all() if user.user_inactive_reason == 0}


    # Reset our DB.
    for player in compass_players:
        player.played_leader = 0
        player.missions_played = 0
        player.deaths = 0

    # Remove banned players from session gathering session data
    for player in session_players:
      if player.player_name.lower().replace(" ", "") not in user_ranks and player.player_name not in ["Lupin_Yonder", "Mr-Link", "Ivan"]: # These people are the worst of worst
        session_players.remove(player)   

    # Remove banned players from cmp_db
    for player in compass_players:
      if player.player_name.lower().replace(" ", "") not in user_ranks and player.player_name not in ["Lupin_Yonder", "Mr-Link", "Ivan"]: 
        compass_players.remove(player)   

    for player in session_players:
        rank = user_ranks.get(player.player_name.lower().replace(" ", ""), "Regular")
        if player not in compass_players:  # compares player_uid
            compass_players.append(player)

            compass_player = CmpPlayer(player_name=player.player_name,
                                   player_uid=player.player_uid,
                                   missions_played=1,
                                   last_played=player.created,
                                   danger_zone=False,
                                   player_rank=rank,
                                   deaths=0,
                                   played_leader=0,
                                   last_mission=player.mission_id,
                                   staff_notes=""
                                   )
            db.session.add(compass_player)
        else:
            compass_player = (db.session.query(CmpPlayer)
                          .filter(CmpPlayer.player_name == player.player_name)
                          .first())

            compass_player.missions_played += 1

            if player.hull_gear_class in LEADERSHIP_ROLES:
                compass_player.played_leader += 1

            if player.death is not None:
                compass_player.deaths += 1

            if compass_player.last_played < player.created:
                compass_player.last_played = player.created
                compass_player.last_mission = player.mission_id

                compass_player.danger_zone = in_danger_zone(player, rank)

    db.session.commit()


def in_session(player):
    """Checks whether the Player was 'created' during a Saturday session."""
    return ((player.created.weekday() in [5, 6]) and
            ((player.created.hour >= 18) or (player.created.hour <= 5)) and
            (not player.is_jip) and
            (player.player_name not in ["HC", "Error: No unit", "Flash",
                                        "Namuthewhale", "SkinnyTar", "Sakai",
                                        "ratcatcher", "Tegyr", "Ricky",
                                        "ZeRandomTigre", "Wrathz", "Emaharg",
                                        "Pr3sario", "Shalun (2)", "Lucky", "Matt"]))


def in_danger_zone(player, rank):
    """Checks whether the Player was 'created' more than two weeks ago."""
    return (player.created.isocalendar()[1] <
            (date.today().isocalendar()[1] - 2) 
            and rank not in ["Guest", "Staff"])

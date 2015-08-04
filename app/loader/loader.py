from app import db, app

import time
from datetime import date
import datetime

from app.sessions.database import (Mission, Player, AIMovement, PlayerMovement,
                                 PlayerDisconnect, func, AstPlayer)
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

    # Get a list of the AstPlayers that already exist in our local DB.
    ast_players = db.session.query(AstPlayer).all()

    # Reset our DB.
    for player in ast_players:
        player.played_leader = 0
        player.missions_played = 0
        player.deaths = 0

    for player in session_players:
        if player not in ast_players:  # compares player_uid
            ast_players.append(player)

            ast_player = AstPlayer(player_name=player.player_name,
                                   player_uid=player.player_uid,
                                   missions_played=1,
                                   last_played=player.created,
                                   danger_zone=False,
                                   player_rank="Regular",
                                   deaths=0,
                                   played_leader=0,
                                   last_mission=player.mission_id,
                                   staff_notes="")
            db.session.add(ast_player)
        else:
            ast_player = (db.session.query(AstPlayer)
                          .filter(AstPlayer.player_name == player.player_name)
                          .first())

            ast_player.missions_played += 1

            if player.hull_gear_class in LEADERSHIP_ROLES:
                ast_player.played_leader += 1

            if player.death is not None:
                ast_player.deaths += 1

            if ast_player.last_played < player.created:
                ast_player.last_played = player.created
                ast_player.last_mission = player.mission_id

                ast_player.danger_zone = in_danger_zone(player)

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
                                        "Pr3sario", "Shalun (2)", "Lucky"]))


def in_danger_zone(player):
    """Checks whether the Player was 'created' more than two weeks ago."""
    return (player.created.isocalendar()[1] <
            (date.today().isocalendar()[1] - 2))

from app import db
from sqlalchemy import Column, ForeignKey, Integer, String, REAL, DateTime, Boolean, func
from sqlalchemy.orm import relationship


class Mission(db.Model):
    __tablename__ = "mission"
    __bind_key__ = 'ark_a2'
    
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False)
    mission_name = Column(String(100), nullable=False)
    world_name = Column(String(100), nullable=False)
    safety_timer = Column(String(100))
    safety_timer_ingame = Column(REAL)
    end = Column(String(100))
    end_ingame = Column(REAL)

    def __repr__(self):
        return "{0} - {1}".format(self.mission_name, self.world_name)


class Player(db.Model):
    __tablename__ = 'player'
    __bind_key__ = 'ark_a2'
    
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False)
    created_ingame = Column(REAL, nullable=False)
    mission_id = Column(Integer, ForeignKey('mission.id'), nullable=False)
    player_uid = Column(String(100), nullable=False)
    player_name = Column(String(100), nullable=False)
    hull_gear_class = Column(String(20))
    group_name = Column(String(40), nullable=False)
    is_jip = Column(Boolean, nullable=False)
    death = Column(String(100))
    death_ingame = Column(REAL)

    mission = relationship(Mission)

    # Equality comparison is overloaded, as we
    # need to compare Player to AstPlayer later on.
    def __eq__(self, other):
        return self.player_uid == other.player_uid


class AIMovement(db.Model):
    __tablename__ = 'ai_movement'
    __bind_key__ = 'ark_a2'
    
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False)
    created_ingame = Column(REAL, nullable=False)
    mission_id = Column(Integer, ForeignKey('mission.id'), nullable=False)
    position = Column(String(40), nullable=False)
    group_name = Column(String(100), nullable=False)
    alive_count = Column(Integer, nullable=False)
    vehicle = Column(String(100))
    waypoint_position = Column(String(40), nullable=False)
    waypoint_type = Column(String(20), nullable=False)

    mission = relationship(Mission)


class PlayerMovement(db.Model):
    __tablename__ = 'player_movement'
    __bind_key__ = 'ark_a2'
    
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False)
    created_ingame = Column(REAL, nullable=False)
    player_id = Column(Integer, ForeignKey('player.id'), nullable=False)
    position = Column(String(40), nullable=False)
    vehicle = Column(String(100))

    player = relationship(Player)


class PlayerDisconnect(db.Model):
    __tablename__ = 'disconnect'
    __bind_key__ = 'ark_a2'
    
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False)
    created_ingame = Column(REAL, nullable=False)
    mission_id = Column(Integer, ForeignKey('mission.id'), nullable=False)
    player_uid = Column(String(100), nullable=False)
    player_name = Column(String(100), nullable=False)

    mission = relationship(Mission)


class AstPlayer(db.Model):
    __tablename__ = 'astplayer'
    __bind_key__ = 'ast'
    
    id = Column(Integer, primary_key=True)
    #created = Column(DateTime, nullable=False)
    player_uid = Column(String(100), nullable=False)
    player_name = Column(String(100), nullable=False)
    player_rank = Column(String(100), nullable=False)
    played_leader = Column(Integer, nullable=False)
    staff_notes = Column(String, nullable=False)
    missions_played = Column(Integer, nullable=False)
    last_mission = Column(String, nullable=False)
    last_played = Column(DateTime, nullable=False)
    danger_zone = Column(Boolean, nullable=False)
    deaths = Column(Integer, nullable=False)

    # Equality comparison is overloaded, as we
    # need to compare Player to AstPlayer later on.
    def __eq__(self, other):
        return self.player_uid == other.player_uid

    
        
    def __repr__(self):
        return "{0} - id {1}".format(self.player_name, self.player_uid)

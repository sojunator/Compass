from app import db
from sqlalchemy import Column, ForeignKey, Integer, String, REAL, DateTime, Boolean, func
from sqlalchemy.orm import relationship


from app import app

class ForumUser(db.Model):

    _ranktable = {
        1: "Staff",
        3: "Regular",
        5: "Recruit",
        6: "Veteran",
        7: "Captain",
        8: "Guest" 
    }

    __tablename__ = "phpbb_users"
    __bind_key__ = 'ark_forums'

    user_id = Column(Integer, primary_key=True)
    username_clean = Column(String(255), nullable=False)
    user_rank = Column(Integer, nullable=False)
    user_inactive_reason = Column(Integer, nullable=False)

    def show_rank(self):
        if self.user_rank in self._ranktable:
            return "{0}".format(self._ranktable[self.user_rank])
        else:
            return None


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
        return "{0}".format(self.mission_name)

    def __eq__(self, other):
        self_name = self.mission_name.split("_")
        other_name = other.mission_name.split("_")

        self_name.pop()
        other_name.pop()

        self_name = ''.join(self_name)
        other_name = ''.join(other_name)

        return self_name == other_name

    def __hash__(self):
        return (self.mission_name).__hash__()

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
    # need to compare Player to AstPlayer later on
    def __eq__(self, other):
        return self.player_name == other.player_name

    def __repr__(self):
        return "{0}".format(self.player_name)    


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


class CmpPlayer(db.Model):
    __tablename__ = 'CmpPlayer'
    __bind_key__ = 'compass'
    
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
    # need to compare Player to CmpPlayer later on.
    def __eq__(self, other):
        return self.player_name == other.player_name

    def return_danger(self):
        if self.danger_zone:
            return "danger_zone"
        else:
            return ""

    def __repr__(self):
        return "{0} - id {1}".format(self.player_name, self.player_uid)
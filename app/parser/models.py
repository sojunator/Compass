class Session:
    def __init__(self):
        self.missions = []
        self.playerpeak = 0
        
    def add_mission(self, mission): 
        self.missions.append(mission)
        
    def update_player_peak(self):               
        for SessionMission in self.missions:
            if self.playerpeak < SessionMission.playercount:
                self.playerpeak = SessionMission.playercount
    
    def __repr__(self):
        self.update_player_peak()
        return "A peak of {0} - {1}".format(self.playerpeak, self.missions)
 
class SessionMission:
    def __init__(self, mission, playercount):
       self.mission = mission
       self.playercount = playercount
    
    def __repr__(self):
        return "{0} {1}".format(self.mission, self.playercount)
        
class Player:
    def __init(self, name, rank):
        self.name = name
    
class Session:
    def __init__(self):
        self.missions = []
        self.playerpeak = 0
        # self.length = 0
        
    def add_mission(self, mission, playercount):
        self.missions.append(mission)
        print (mission.end_ingame)
        # self.length += mission.end_ingame
        
        if self.playerpeak < playercount:
            self.playerpeak = playercount
            
    def __repr__(self):
        return "{0} {1}".format(self.missions, self.playerpeak)
 
class SessionMission:
    def __init__(self, mission, playercount):
       self.playercount = playercount
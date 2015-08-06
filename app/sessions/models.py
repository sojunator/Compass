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
    def __init__(self, mission, playercount, players, groups):
        self.mission = mission
        self.playercount = playercount
        self.players = players
        self.mission_name = mission.mission_name
        self.groups = groups


    def __repr__(self):
        return "{0} {1}".format(self.mission, self.playercount)

class GroupsInMission:
    def __init__(self):
        self.group = []
        self.member_count = 0

    def add_member(self, player):
        self.group.append(player)
        self.member_count = self.member_count + 1

    def __repr__(self):

        string = ""

        for index, player in enumerate(self.group):
            string = string + " " + player.player_name
            print(player.player_name)


        return string

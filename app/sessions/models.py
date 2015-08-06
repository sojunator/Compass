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
    _rules = { 
        "CO": 1,
        "XO": 2,
        "ASL": 3,
        "A1": 4,
        "A2": 5,
        "A3": 6,
        "BSL": 7,
        "B1": 8,
        "B2": 9,
        "B3": 10,
        "MMG1": 11,
        "MMG2": 12,
        "HMG1": 13,
        "IFV1": 14,
        "IFV2": 15,
        "IFV3": 16,
        "IFV4": 17,
        "TNK1": 18
    }

    def __init__(self, mission, playercount, players, groups):
        self.mission = mission
        self.playercount = playercount
        self.players = players
        self.mission_name = mission.mission_name
        self.groups = self.sort_groups(groups)

    def __repr__(self):
        return "{0} {1}".format(self.mission, self.playercount)

    def sort_groups(self, groups):
        return sorted(groups.items(), key=lambda x: ( x[0].split(" ")[0], self._rules.get(x[0].split(" ")[1], 99)))

    

class GroupsInMission:
    def __init__(self):
        self.players = []
        self.member_count = 0

    def add_member(self, player):
        self.players.append(player)
        self.member_count = self.member_count + 1

    def __repr__(self):
        return " ".join([player.player_name for player in self.players])

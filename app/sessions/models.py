class Session:
    def __init__(self):
        self.missions = []
        self.playerpeak = 0

    def session_lenght(self):
        start = self.missions[0].created
        end = self.missions[-1].end
        return end - start

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
        "CSL": 11,
        "C1": 12,
        "C2": 13,
        "C3": 14,
        "DSL": 15,
        "D1": 16,
        "D2": 17,
        "D3": 18,
        "IFV1": 19,
        "IFV3": 20,
        "IFV4": 21,
        "TNK1": 22,
        "TNK2": 23,
        "TNK3": 24,
        "TNK4": 25,
        "MMG1": 26,
        "MMG2": 27,
        "HAT1": 28,
        "HAT2": 29,
        "TH1":  30,
        "TH2":  31,
        "TH3":  32,
        "TH4":  33,
        "AH1":  34,
        "AH2":  35,
        "CAS1": 36

    }

    def __init__(self, mission, playercount, players, groups):
        self.mission = mission
        self.playercount = playercount
        self.players = players
        self.mission_name = mission.mission_name
        if groups is not None:
            self.groups = self.sort_groups(groups)

    def __repr__(self):
        return "{0} {1}".format(self.mission, self.playercount)

    def sort_groups(self, groups):
        return sorted(groups.items(), key=lambda x: ( x[0].split(" ")[0], self._rules.get(x[0].split(" ")[1], 99)))

    

class GroupsInMission:
    _rules = {
        "CO": 1,
        "XO": 2,
        "SL": 3,
        "Medic": 4,
        "FTL": 5,
        "AR": 6,
        "AAR": 7,
        "RAT": 8,
        "MMGG": 9,
        "MMGAG": 10,
        "MMGAC": 11,
        "HATG": 12,
        "HATGAG": 13,
        "HATGAC": 14,
        "VC": 15,
        "VG": 16,
        "VD": 17,
        "P": 18,
        "PCM": 19
    }
    def __init__(self):
        self.players = []
        self.member_count = 0

    def add_member(self, player):
        self.players.append(player)
        self.member_count = self.member_count + 1

    def sort_members(self):
        self.players = sorted(self.players, key=lambda x: (self._rules[x[0]]))

    def __repr__(self):
        return " ".join([player.player_name for player in self.players])

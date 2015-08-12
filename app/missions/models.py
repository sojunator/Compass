class MissionData:
	def __init__(self, mission_name, played):
		self.mission_name = mission_name
		self.played = played

	def __eq__(self, other):
		return self.mission_name == other
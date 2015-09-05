import time
from datetime import date
import datetime

from app.database.database import Mission
from app import db


class MissionData:
	def __init__(self, mission_name, world_name, played):
		(type, player_count) = self.mission_type_and_player_count(mission_name)
		self.type = type
		self.player_count = player_count
		self.mission_name = mission_name
		self.world_name = world_name
		self.played = played
		if played > 0:
			mission_all = db.session.query(Mission).filter(Mission.mission_name == mission_name).all()
			temp_mission = mission_all[0]
			for mission in mission_all:
				if temp_mission.created < mission.created:
					temp_mission = mission

			self.last_played = temp_mission.created.date()
			self.last_played_delta = datetime.date.today() - temp_mission.created.date()
			self.last_played_delta = self.last_played_delta.days
			self.last_datetime = temp_mission.created.date()
		else:
			self.last_played = "No record"
			self.last_datetime = datetime.date(datetime.MINYEAR, 1, 1)

		self.colour = self.setColour()

	def __eq__(self, other):
		return self.mission_name == other

	def setColour(self):
		value = abs(self.last_datetime.isocalendar()[1] - date.today().isocalendar()[1])
		returnValues = {
			0 : "stage1",
			1 : "stage1",
			2 : "stage2",
			3 : "stage2",
			4 : "stage3",
			5 : "stage3",
			6 : "stage4",
			7 : "stage4",
			8 : "stage5",
		}

		return returnValues.get(value, "stage5")

	def mission_type_and_player_count(self, mission_name):
		mission_name_split = mission_name.split('_')
		if len(mission_name_split) > 1:
			type_and_player_count = mission_name_split[1]
			types = ['cotvt', 'co', 'tvt', 'gtvt']
			for type in types:
				t_len = len(type)
				if type_and_player_count[:t_len] == type:
					return (type, type_and_player_count[t_len:])

		return ('custom', 0)

	def type_html(self):
		return { 'cotvt': 'ct', 'co': 'c', 'tvt': 't', 'gtvt': 'g', 'custom': '?' }[self.type]


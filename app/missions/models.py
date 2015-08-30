import time
from datetime import date
import datetime

from app.database.database import Mission
from app import db


class MissionData:
	def __init__(self, mission_name, played):
		self.mission_name = mission_name
		self.played = played
		self.mission_type = "co"
		if played is not 0:
			mission_all = db.session.query(Mission).filter(Mission.mission_name == mission_name).all()
			temp_mission = mission_all[0]
			for mission in mission_all:
				if temp_mission.created < mission.created:
					temp_mission = mission

			self.last_played = temp_mission.created.date()
			self.last_datetime = temp_mission.created.date()
		else:
			self.last_played = "No record"
			self.last_datetime = datetime.date(datetime.MINYEAR, 1, 1)

		self.colour = self.setColour()

		if self.mission_name != "##Lobby##":
			split_mission_name = self.mission_name.split("_")[1]
			if split_mission_name[:3] in ["gtv", "tvt"]:
				self.mission_type = "tvt"

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


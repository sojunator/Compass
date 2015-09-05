import time
from datetime import date
import datetime
import os
import re

from app.database.database import Mission
from app import db
from app import app


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


class PBO:
	def __init__(self, pbo):
		if pbo is None:
			raise

		self.name = os.path.basename(pbo.filename)

		if self.valid_name(self.name):
			self.mission = MissionData(self.name, 0)
			pbo.save(os.path.join(app.config['UPLOAD_FOLDER'], pbo.filename))
		else:
			raise

	def valid_name(self, name):
		return (True if	re.search('ark+_[a-z]+[0-9]+_.+[.].+[.]pbo', name)
				else False)
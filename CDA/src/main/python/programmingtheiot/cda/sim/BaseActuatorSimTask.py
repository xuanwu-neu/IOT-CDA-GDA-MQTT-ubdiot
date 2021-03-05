#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import random

from src.main.python.programmingtheiot.common import ConfigConst
from src.main.python.programmingtheiot.data.ActuatorData import ActuatorData

class BaseActuatorSimTask():
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, actuatorType: int = ActuatorData.DEFAULT_ACTUATOR_TYPE, simpleName: str = "Actuator", actuatorName = ConfigConst.NOT_SET):
		self.name = actuatorName
		self.actuatorType = actuatorType
		self.simpleName = simpleName
		self.latestActuatorData = ActuatorData()
		self.value = 0.0
		
	def activateActuator(self, val: float) -> bool:
		self.value = val
		sval = str(self.value)
		logging.info("actuator was sent an 'ON' command, and its value is:" + sval)
		self.latestActuatorData.command = ActuatorData.COMMAND_ON
		return True
		
	def deactivateActuator(self) -> bool:
		logging.info("actuator was sent an 'OFF' command.")
		self.latestActuatorData.command = ActuatorData.COMMAND_OFF
		return True
		
	def getLatestActuatorResponse(self) -> ActuatorData:
		return self.latestActuatorData
	
	def getSimpleName(self) -> str:
		return self.simpleName
	
	def updateActuator(self, data: ActuatorData) -> bool:
		if data != None:
			if data.command == ActuatorData.COMMAND_ON:
				self.activateActuator(data.value)
			elif data.command == ActuatorData.COMMAND_OFF:
				self.deactivateActuator()
		data.name = self.name
		self.latestActuatorData.updateData(data)
		self.latestActuatorData.setAsResponse()
		return True
		
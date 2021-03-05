#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from time import sleep

import src.main.python.programmingtheiot.common.ConfigConst as ConfigConst

from src.main.python.programmingtheiot.common.ConfigUtil import ConfigUtil
from src.main.python.programmingtheiot.data.ActuatorData import ActuatorData
from src.main.python.programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

from pisense import SenseHAT


class HeartRateUpEmulatorTask(BaseActuatorSimTask):
	"""
	Shell representation of class for student implementation.

	"""

	def __init__(self):
		super(HeartRateUpEmulatorTask, self).__init__(actuatorType=ActuatorData.HEART_RATE_ACTUATOR_TYPE_UP, simpleName="HEART_RATE_ACTUATOR_TYPE_UP", actuatorName = ConfigConst.HEART_RATE_UP_ACTUATOR_NAME)
		self.sh = SenseHAT(emulate=True)
		configUtil = ConfigUtil()
		flag = configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_SENSE_HAT_KEY)
		if flag:
			self.sh = SenseHAT(emulate=True)
		else:
			self.sh = SenseHAT(emulate=False)

	def _handleActuation(self, cmd: int, val: float = 0.0, stateData: str = None) -> int:
		if cmd == ActuatorData.COMMAND_ON:
			if self.sh.screen:
				# create a message with the value and an 'ON' message, then scroll it across the LED display
				#self.sh.screen.scroll_text(str(val))
				self.sh.screen.scroll_text("Warning ! Heart rate is more than 90.")


			else:
				logging.warning("No SenseHAT LED screen instance to update.")
				return -1
		else:
			if self.sh.screen:
				# create a message with an 'OFF' message, then scroll it across the LED display
				self.sh.screen.scroll_text("")


			else:
				logging.warning("No SenseHAT LED screen instance to clear / close.")
				return -1

	def updateActuator(self, data: ActuatorData) -> bool:
		if data != None:
			if data.command == ActuatorData.COMMAND_ON:
				self.activateActuator(data.value)
			elif data.command == ActuatorData.COMMAND_OFF:
				self.deactivateActuator()
		data.name = self.name
		self._handleActuation(data.command, data.value, data.stateData)
		self.latestActuatorData.updateData(data)
		self.latestActuatorData.setAsResponse()
		print(self.latestActuatorData.actuatorType);
		return True
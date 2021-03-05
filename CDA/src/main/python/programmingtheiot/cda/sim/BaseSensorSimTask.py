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
from src.main.python.programmingtheiot.data.SensorData import SensorData

class BaseSensorSimTask():
	"""
	Shell representation of class for student implementation.
	
	"""

	DEFAULT_MIN_VAL = 0.0
	DEFAULT_MAX_VAL = 1000.0
	
	def __init__(self, sensorType: int = SensorData.DEFAULT_SENSOR_TYPE, dataSet = None, minVal: float = DEFAULT_MIN_VAL, maxVal: float = DEFAULT_MAX_VAL, sensorName = ConfigConst.NOT_SET):
		self.sensorName = sensorName
		self.sensorType = sensorType
		self.dataSet = dataSet
		self.minVal = minVal
		self.maxVal = maxVal
		self.index = 0
		self.lastSensorData = None
		self.useRandomizer = False
		if self.dataSet == None:
			self.useRandomizer = True
	
	def generateTelemetry(self) -> SensorData:
		sensorData = SensorData(sensorType = self.sensorType, name = self.sensorName)
		if self.useRandomizer:
			value = random.uniform(self.minVal, self.maxVal)
			value = round(value, 2)
			sensorData.setValue(value)
		else:
			sensorData = self.dataSet.getDataEntry(self.index)
			self.index = self.index + 1
			if self.index >= self.dataSet.getDataEntryCount():
				self.index = 0
		self.lastSensorData = sensorData
		return self.lastSensorData
	
	def getTelemetryValue(self) -> float:
		if self.lastSensorData:
			return self.lastSensorData.getValue()
		else:
			self.generateTelemetry()
			return self.lastSensorData.getValue()
	
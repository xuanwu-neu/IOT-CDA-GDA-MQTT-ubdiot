#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#
import logging

from src.main.python.programmingtheiot.common import ConfigConst
from src.main.python.programmingtheiot.data.SensorData import SensorData

class BaseSystemUtilTask():
	"""
	Shell representation of class for student implementation.
	
	"""
	
	def __init__(self, sensorName = ConfigConst.NOT_SET):
		###
		# TODO: fill in the details here
		self.latestSensorData = None
		self.sensorName = sensorName
		pass
	
	def generateTelemetry(self) -> SensorData:
		###
		# TODO: fill in the details here
		#
		# NOTE: Use self._getSystemUtil() to retrieve the value from the sub-class
		sensorData = SensorData(name = self.sensorName)
		self.latestSensorData = sensorData
		self.latestSensorData.value = self._getSystemUtil()
		return self.latestSensorData
		
	def getTelemetryValue(self) -> float:
		if self.latestSensorData is None:
			self.generateTelemetry()
		return self.latestSensorData.value
	
	def _getSystemUtil(self) -> float:
		"""
		Template method implemented by sub-class.
		
		Retrieve the system utilization value as a float.
		
		@return float
		"""
		pass
		

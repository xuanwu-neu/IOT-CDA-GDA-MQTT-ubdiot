#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#
from src.main.python.programmingtheiot.common import ConfigConst
from src.main.python.programmingtheiot.data.BaseIotData import BaseIotData

class SensorData(BaseIotData):
	"""
	Shell representation of class for student implementation.
	
	"""
	DEFAULT_VAL = 0.0
	DEFAULT_SENSOR_TYPE = 0
	
	# These are just sensor type samples - these can be changed however
	# you'd like; you can also create an enum representing the values
	HEART_RATE_SENSOR_TYPE = 1
	BLOOD_PRESSURE_SENSOR_TYPE = 2
	BODY_TEMP_SENSOR_TYPE = 3

	def __init__(self, sensorType: int = DEFAULT_SENSOR_TYPE, name=ConfigConst.NOT_SET, d=None):
		"""
		Constructor.

		@param d Defaults to None. The data (dict) to use for setting all parameters.
		It's provided here as a convenience - mostly for testing purposes. The utility
		in DataUtil should be used instead.
		"""
		super(SensorData, self).__init__(name=name, d=d)

		if d:
			self.value = d['value']
			self.sensorType = d['sensorType']
		else:
			self.value = self.DEFAULT_VAL
			self.sensorType = sensorType
	
	def getSensorType(self) -> int:
		"""
		Returns the sensor type to the caller.
		
		@return int
		"""
		return self.sensorType
	
	def getValue(self) -> float:
		return self.value
	
	def setValue(self, newVal: float):
		self.value = newVal
	
	def __str__(self):
		"""
		Returns a string representation of this instance.
		
		@return The string representing this instance.
		"""
		svalue = str(self.getValue())
		ssensorType = str(self.getSensorType())
		customStr = \
			str('name='	+ self.getName() + \
			',value=' + svalue + \
			',sensorType=' + ssensorType)
					
		return customStr	
	def _handleUpdateData(self, data):
		if data != None:
			self.value = data.value

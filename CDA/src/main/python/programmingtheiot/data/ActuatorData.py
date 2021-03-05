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

class ActuatorData(BaseIotData):
	"""
	Shell representation of class for student implementation.
	
	"""
	DEFAULT_COMMAND = 0
	COMMAND_OFF = DEFAULT_COMMAND
	COMMAND_ON = 1

	# for now, actuators will be 1..99
	# and displays will be 100..1999
	DEFAULT_ACTUATOR_TYPE = 0
	
	BODY_TEMP_ACTUATOR_TYPE_UP = 1
	BODY_TEMP_ACTUATOR_TYPE_DOWN = 2
	BLOOD_PRESSURE_ACTUATOR_TYPE_UP = 3
	BLOOD_PRESSURE_ACTUATOR_TYPE_DOWN = 4
	HEART_RATE_ACTUATOR_TYPE_UP = 5
	HEART_RATE_ACTUATOR_TYPE_DOWN = 6

	def __init__(self, actuatorType: int = DEFAULT_ACTUATOR_TYPE, name=ConfigConst.NOT_SET, d=None):
		"""
		Constructor.

		@param d Defaults to None. The data (dict) to use for setting all parameters.
		It's provided here as a convenience - mostly for testing purposes. The utility
		in DataUtil should be used instead.
		"""
		super(ActuatorData, self).__init__(name=name, d=d)

		self.isResponse = False
		self.actuatorType = actuatorType
		self.value = 0

		if d:
			self.command = d['command']
			self.stateData = d['stateData']
			self.curValue = d['curValue']
			self.actuatorType = d['actuatorType']
		else:
			self.command = self.DEFAULT_COMMAND
			self.stateData = None
			self.curValue = self.DEFAULT_VAL
			self.actuatorType = actuatorType

	def __str__(self):
		"""
		Returns a string representation of this instance.
		
		@return The string representing this instance.
		"""
		svalue = str(self.getValue())
		sstateData = str(self.getStateData())
		scommand = str(self.command)
		customStr = \
			str('value='	+ svalue + \
			',stateData=' + sstateData + \
			',name=' + self.getName() + \
			',command=' + scommand)
					
		return customStr	
	
	def getCommand(self) -> int:
		return self.command
	
	def getStateData(self) -> str:
		return self.stateData
	
	def getValue(self) -> float:
		return self.value
	
	def isResponseFlagEnabled(self) -> bool:
		return False
	
	def setCommand(self, command: int):
		self.command = command
	
	def setAsResponse(self):
		self.isResponse = True
		
	def setStateData(self, stateData: str):
		self.stateData = stateData
	
	def setValue(self, val: float):
		self.value = val
		
	def _handleUpdateData(self, data):
		if data != None:
			self.value = data.value 
			self.command = data.command 
			self.stateData = data.stateData
			self.actuatorType = data.actuatorType
		
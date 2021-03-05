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


class SystemPerformanceData(BaseIotData):
	"""
	Shell representation of class for student implementation.
	
	"""
	DEFAULT_VAL = 0.0

	def __init__(self, d=None):
		"""
		Constructor.

		@param d Defaults to None. The data (dict) to use for setting all parameters.
		It's provided here as a convenience - mostly for testing purposes. The utility
		in DataUtil should be used instead.
		"""
		super(SystemPerformanceData, self).__init__(name=ConfigConst.NOT_SET, d=d)

		if d:
			self.cpuUtil = d['cpuUtil']
			self.diskUtil = d['diskUtil']
			self.memUtil = d['memUtil']
		else:
			self.cpuUtil = self.DEFAULT_VAL
			self.diskUtil = self.DEFAULT_VAL
			self.memUtil = self.DEFAULT_VAL

	def __str__(self):
		"""
		Returns a string representation of this instance.

		@return The string representing this instance.
		"""

		customStr = \
			str('CpuUtilization=' + str(self.getCpuUtilization()) + \
				'DiskUtilization=' + str(self.getDiskUtilization()) +
				'MemoryUtilization=' + str(self.getMemoryUtilization()))

		return customStr
	def getCpuUtilization(self):
		return self.cpuUtil
	
	def getDiskUtilization(self):
		return self.diskUtil
	
	def getMemoryUtilization(self):
		return self.memUtil
	
	def setCpuUtilization(self, cpuUtil):
		self.cpuUtil = cpuUtil
	
	def setDiskUtilization(self, diskUtil):
		self.diskUtil = diskUtil
	
	def setMemoryUtilization(self, memUtil):
		self.memUtil = memUtil
	
	def _handleUpdateData(self, data):
		if data != None:
			self.cpuUtil = data.cpuUtil
			self.diskUtil = data.diskUtil
			self.memUtil = data.memUtil

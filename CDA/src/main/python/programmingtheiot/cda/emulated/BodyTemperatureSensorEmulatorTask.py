#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

from src.main.python.programmingtheiot.data.SensorData import SensorData

import src.main.python.programmingtheiot.common.ConfigConst as ConfigConst

from src.main.python.programmingtheiot.common.ConfigUtil import ConfigUtil
from src.main.python.programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from src.main.python.programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator

from pisense import SenseHAT


class BodyTemperatureSensorEmulatorTask(BaseSensorSimTask):
	"""
	Shell representation of class for student implementation.

	"""

	def __init__(self, dataSet=None):
		super(BodyTemperatureSensorEmulatorTask, self).__init__(SensorData.BODY_TEMP_SENSOR_TYPE,
															minVal=SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP,
															maxVal=SensorDataGenerator.HI_NORMAL_INDOOR_TEMP,
															sensorName= ConfigConst.BODY_TEMP_SENSOR_NAME)
		self.sh = SenseHAT(emulate=True)
		configUtil = ConfigUtil()
		flag = configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_SENSE_HAT_KEY)
		if flag:
			self.sh = SenseHAT(emulate=True)
		else:
			self.sh = SenseHAT(emulate=False)

	def generateTelemetry(self) -> SensorData:
		sensorData = SensorData(name = ConfigConst.BODY_TEMP_SENSOR_NAME, sensorType = self.sensorType)
		sensorVal = self.sh.environ.temperature
		sensorData.setValue(sensorVal)
		self.latestSensorData = sensorData
		return sensorData

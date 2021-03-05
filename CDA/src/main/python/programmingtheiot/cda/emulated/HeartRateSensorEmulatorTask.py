#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#
import logging

from src.main.python.programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask
from src.main.python.programmingtheiot.data.SensorData import SensorData
import src.main.python.programmingtheiot.common.ConfigConst as ConfigConst

from src.main.python.programmingtheiot.common.ConfigUtil import ConfigUtil
from src.main.python.programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from src.main.python.programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator

from pisense import SenseHAT


class HeartRateSensorEmulatorTask(BaseSensorSimTask):
    """
	Shell representation of class for student implementation.

	"""

    def __init__(self, dataSet=None):
        super(HeartRateSensorEmulatorTask, self).__init__(SensorData.HEART_RATE_SENSOR_TYPE,
                                                         minVal=SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY,
                                                         maxVal=SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY,
                                                         sensorName=ConfigConst.HEART_RATE_SENSOR_NAME)
        # Create an instance of SenseHAT and set the emulate flag to True if running the emulator, or False if using real hardware
        # This can be read from ConfigUtil using the ConfigConst.CONSTRAINED_DEVICE section and the ConfigConst.ENABLE_SENSE_HAT_KEY
        # If the ConfigConst.ENABLE_SENSE_HAT_KEY is False, set the emulate flag to True, otherwise set to False
        self.sh = SenseHAT(emulate=True)
        configUtil = ConfigUtil()
        flag = configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_SENSE_HAT_KEY)

        if flag:
            self.sh = SenseHAT(emulate=True)
        else:
            self.sh = SenseHAT(emulate=False)

    def generateTelemetry(self) -> SensorData:
        sensorData = SensorData(name = ConfigConst.HEART_RATE_SENSOR_NAME, sensorType = self.sensorType)
        sensorVal = self.sh.environ.humidity
        sensorData.setValue(sensorVal)
        self.latestSensorData = sensorData
        return sensorData

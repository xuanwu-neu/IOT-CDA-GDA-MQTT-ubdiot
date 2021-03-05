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

from src.main.python.programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from src.main.python.programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator
from src.main.python.programmingtheiot.cda.sim.SensorDataGenerator import SensorDataSet
from src.main.python.programmingtheiot.common import ConfigConst

from src.main.python.programmingtheiot.data.SensorData import SensorData


class HeartRateSensorSimTask(BaseSensorSimTask):
    """
	Shell representation of class for student implementation.
	"""

    def __init__(self, dataSet=None):
        super(HeartRateSensorSimTask, self).__init__(SensorData.HEART_RATE_SENSOR_TYPE, dataSet=dataSet,
                                                    minVal=SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY,
                                                    maxVal=SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY,
                                                    sensorName=ConfigConst.HEART_RATE_SENSOR_NAME)

    def generateTelemetry(self) -> SensorData:
        sensorData = SensorData(name = ConfigConst.HEART_RATE_SENSOR_NAME, sensorType = self.sensorType)
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

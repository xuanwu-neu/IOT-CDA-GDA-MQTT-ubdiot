#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from apscheduler.schedulers.background import BackgroundScheduler

from src.main.python.programmingtheiot.common.IDataMessageListener import IDataMessageListener

from src.main.python.programmingtheiot.cda.sim.BloodPressureSensorSimTask import BloodPressureSensorSimTask
from src.main.python.programmingtheiot.cda.sim.BodyTemperatureSensorSimTask import BodyTemperatureSensorSimTask
from src.main.python.programmingtheiot.cda.sim.HeartRateSensorSimTask import HeartRateSensorSimTask
import src.main.python.programmingtheiot.common.ConfigConst as ConfigConst
from src.main.python.programmingtheiot.common.ConfigUtil import ConfigUtil
from src.main.python.programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator


class SensorAdapterManager(object):
	"""
	Shell representation of class for student implementation.

	"""

	def __init__(self, useEmulator: bool = True, pollRate: int = 5, allowConfigOverride: bool = True):
		self.useEmulator = useEmulator
		self.pollRate = pollRate
		self.dataMsgListener = IDataMessageListener()
		self.scheduler = BackgroundScheduler()
		self.scheduler.add_job(self.handleTelemetry, 'interval', seconds=self.pollRate)

		if self.useEmulator:
			logging.info("emulators will be used.")
			# load the Humidity emulator
			heartRateModule = __import__('src.main.python.programmingtheiot.cda.emulated.HeartRateSensorEmulatorTask',
										fromlist=['HeartRateSensorEmulatorTask'])
			heClazz = getattr(heartRateModule, 'HeartRateSensorEmulatorTask')
			self.heartRateEmulator = heClazz()
			# load the Pressure emulator
			bloodPressureModule = __import__('src.main.python.programmingtheiot.cda.emulated.BloodPressureSensorEmulatorTask',
										fromlist=['BloodPressureSensorEmulatorTask'])
			PeClazz = getattr(bloodPressureModule, 'BloodPressureSensorEmulatorTask')
			self.bloodPressureEmulator = PeClazz()
			# load the Temperature emulator
			bodyTemperatureModule = __import__('src.main.python.programmingtheiot.cda.emulated.BodyTemperatureSensorEmulatorTask',
										   fromlist=['BodyTemperatureSensorEmulatorTask'])
			TeClazz = getattr(bodyTemperatureModule, 'BodyTemperatureSensorEmulatorTask')
			self.bodyTemperatureEmulator = TeClazz()
		else:
			logging.info("simulators will be used")
			self.dataGenerator = SensorDataGenerator()
			configUtil = ConfigUtil()

			"""
			gei the Floor and ceiling value for each data
			"""
			heartRateFloor = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.HUMIDITY_SIM_FLOOR_KEY,
												SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE)
			heartRateCeiling = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.HUMIDITY_SIM_CEILING_KEY,
												  SensorDataGenerator.HI_NORMAL_ENV_PRESSURE)

			bloodPressureFloor = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.PRESSURE_SIM_FLOOR_KEY,
												SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE)
			bloodPressureCeiling = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.PRESSURE_SIM_CEILING_KEY,
												  SensorDataGenerator.HI_NORMAL_ENV_PRESSURE)

			bodyTempFloor = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TEMP_SIM_FLOOR_KEY,
											SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP)
			bodyTempCeiling = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TEMP_SIM_CEILING_KEY,
											  SensorDataGenerator.HI_NORMAL_INDOOR_TEMP)
			"""
			create three types Data
			"""
			heartRateData = self.dataGenerator.generateDailyEnvironmentHumidityDataSet(minValue=heartRateFloor,
																					  maxValue=heartRateCeiling,
																					  useSeconds=False)
			bloodPressureData = self.dataGenerator.generateDailyEnvironmentPressureDataSet(minValue=bloodPressureFloor,
																					  maxValue=bloodPressureCeiling,
																					  useSeconds=False)
			bodyTempData = self.dataGenerator.generateDailyIndoorTemperatureDataSet(minValue=bodyTempFloor,
																				maxValue=bodyTempCeiling, useSeconds=False)

			"""
			using the data generate sim Task
			"""
			self.heartRateSensorSimTask = HeartRateSensorSimTask(heartRateData)
			self.bloodPressureSensorSimTask = BloodPressureSensorSimTask(bloodPressureData)
			self.bodyTemperatureSensorSimTask = BodyTemperatureSensorSimTask(bodyTempData)

	def handleTelemetry(self):
		if self.useEmulator == False:
			HeartRateSd = self.heartRateSensorSimTask.generateTelemetry()
			BloodPressureSd = self.bloodPressureSensorSimTask.generateTelemetry()
			BodyTemperatureSd = self.bodyTemperatureSensorSimTask.generateTelemetry()
			"""
			call the dataMasgListener
			"""
			self.dataMsgListener.handleSensorMessage(HeartRateSd)
			self.dataMsgListener.handleSensorMessage(BloodPressureSd)
			self.dataMsgListener.handleSensorMessage(BodyTemperatureSd)
		else:
			HeartRateyEd = self.heartRateEmulator.generateTelemetry()
			BloodPressureEd = self.bloodPressureEmulator.generateTelemetry()
			BodyTemperatureEd = self.bodyTemperatureEmulator.generateTelemetry()
			"""
			call the dataMasgListener
			"""
			self.dataMsgListener.handleSensorMessage(HeartRateyEd)
			self.dataMsgListener.handleSensorMessage(BloodPressureEd)
			self.dataMsgListener.handleSensorMessage(BodyTemperatureEd)

	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		if listener:
			self.dataMsgListener = listener
			return True
		else:
			return False

	def startManager(self):
		self.scheduler.start()

	def stopManager(self):
		self.scheduler.shutdown()

#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from src.main.python.programmingtheiot.common.IDataMessageListener import IDataMessageListener
from src.main.python.programmingtheiot.cda.sim.PatientActuatorSimTask import PatientActuatorSimTask
from src.main.python.programmingtheiot.cda.sim.DoctorActuatorSimTask import DoctorActuatorSimTask
from src.main.python.programmingtheiot.data.ActuatorData import ActuatorData


class ActuatorAdapterManager(object):
	"""
	Shell representation of class for student implementation,
	update the blooedpressure, heartRate and bodyTemperature actuator

	"""

	def __init__(self, useEmulator: bool = True):
		self.useEmulator = useEmulator
		self.dataMsgListener = IDataMessageListener()
		if self.useEmulator:
			logging.info("emulators will be used.")
			# load the BloodPressureUp actuation emulator
			BloodPressureUpModule = __import__('src.main.python.programmingtheiot.cda.emulated.BloodPressureUpEmulatorTask',
										  fromlist=['BloodPressureUpEmulatorTask'])
			bpueClazz = getattr(BloodPressureUpModule, 'BloodPressureUpEmulatorTask')
			self.BloodPressureUpEmulator = bpueClazz()
			# load the BloodPressureDown actuation emulator
			BloodPressureDownModule = __import__('src.main.python.programmingtheiot.cda.emulated.BloodPressureDownEmulatorTask',
											fromlist=['BloodPressureDownEmulatorTask'])
			bpdeClazz = getattr(BloodPressureDownModule, 'BloodPressureDownEmulatorTask')
			self.BloodPressureDownEmulator = bpdeClazz()
			# load the BodyTempUp actuation emulator
			BodyTemperatureUpModule = __import__('src.main.python.programmingtheiot.cda.emulated.BodyTemperatureUpEmulatorTask',
										  fromlist=['BodyTemperatureUpEmulatorTask'])
			btueClazz = getattr(BodyTemperatureUpModule, 'BodyTemperatureUpEmulatorTask')
			self.BodyTemperatureUpEmulator = btueClazz()
			# load the BodyTempDown actuation emulator
			BodyTemperatureDownModule = __import__(
				'src.main.python.programmingtheiot.cda.emulated.BodyTemperatureDownEmulatorTask',
				fromlist=['BodyTemperatureDownEmulatorTask'])
			btdeClazz = getattr(BodyTemperatureDownModule, 'BodyTemperatureDownEmulatorTask')
			self.BodyTemperatureDownEmulator = btdeClazz()
			# load the HeartRateUp actuation emulator
			HeartRateUpModule = __import__('src.main.python.programmingtheiot.cda.emulated.HeartRateUpEmulatorTask',
										  fromlist=['HeartRateUpEmulatorTask'])
			hrueClazz = getattr(HeartRateUpModule, 'HeartRateUpEmulatorTask')
			self.HeartRateUpEmulator = hrueClazz()
			# load the HeartRateDown actuation emulator
			HeartRateDownModule = __import__('src.main.python.programmingtheiot.cda.emulated.HeartRateDownEmulatorTask',
										  fromlist=['HeartRateDownEmulatorTask'])
			hrdeClazz = getattr(HeartRateDownModule, 'HeartRateDownEmulatorTask')
			self.HeartRateDownEmulator = hrdeClazz()
		else:
			logging.info("simulators will be used.")
			# create the humidifier actuator
			self.patientActuator = PatientActuatorSimTask()

			# create the HVAC actuator
			self.doctorActuator = DoctorActuatorSimTask()

	def sendActuatorCommand(self, data: ActuatorData) -> bool:
		if self.useEmulator:

			if data.actuatorType == 1:
				self.BodyTemperatureUpEmulator.updateActuator(data)
				if self.dataMsgListener is not None:
					self.dataMsgListener.handleActuatorCommandResponse(self.BodyTemperatureUpEmulator.getLatestActuatorResponse())
			if data.actuatorType == 2:
				self.BodyTemperatureDownEmulator.updateActuator(data)
				if self.dataMsgListener is not None:
					self.dataMsgListener.handleActuatorCommandResponse(self.BodyTemperatureDownEmulator.getLatestActuatorResponse())
			if data.actuatorType == 3:
				self.BloodPressureUpEmulator.updateActuator(data)
				if self.dataMsgListener is not None:
					self.dataMsgListener.handleActuatorCommandResponse(self.BloodPressureUpEmulator.getLatestActuatorResponse())
			if data.actuatorType == 4:
				self.BloodPressureDownEmulator.updateActuator(data)
				if self.dataMsgListener is not None:
					self.dataMsgListener.handleActuatorCommandResponse(self.BloodPressureDownEmulator.getLatestActuatorResponse())
			if data.actuatorType == 5:
				self.HeartRateUpEmulator.updateActuator(data)
				if self.dataMsgListener is not None:
					self.dataMsgListener.handleActuatorCommandResponse(self.HeartRateUpEmulator.getLatestActuatorResponse())
			if data.actuatorType == 6:
				self.HeartRateDownEmulator.updateActuator(data)
				if self.dataMsgListener is not None:
					self.dataMsgListener.handleActuatorCommandResponse(self.HeartRateDownEmulator.getLatestActuatorResponse())
		else:
			"""
			update the humidifierActuator and hvacActuator
			"""
			if data.isResponseFlagEnabled():

				if data.actuatorType == 1:
					self.patientActuator.updateActuator(data)
					if self.dataMsgListener is not None:
						self.dataMsgListener.handleActuatorCommandResponse(self.patientActuator.getLatestActuatorResponse())
				elif data.actuatorType == 2:
					self.doctorActuator.updateActuator(data)
					if self.dataMsgListener is not None:
						self.dataMsgListener.handleActuatorCommandResponse(self.doctorActuator.getLatestActuatorResponse())
				return True
			else:
				return False

		return False

	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		if listener != None:
			self.dataMsgListener = listener
			return True
		else:
			return False

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

from src.main.python.programmingtheiot.cda.system.SystemCpuUtilTask import SystemCpuUtilTask
from src.main.python.programmingtheiot.cda.system.SystemMemUtilTask import SystemMemUtilTask

class SystemPerformanceManager(object):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, pollRate: int = 30):
		self.dataMsgListener = IDataMessageListener()
		"""
		Create a class-scoped instance of SystemCpuUtilTask
		"""
		self.cpuUtilTask = SystemCpuUtilTask()
		"""
		Create a class-scoped instance of SystemMemUtilTask
		"""
		self.memUtilTask = SystemMemUtilTask()
		"""
		Create a class-scoped instance of BackgroundScheduler 
		"""
		self.scheduler = BackgroundScheduler()
		"""
		Add a job to the scheduler
		"""
		self.scheduler.add_job(self.handleTelemetry, 'interval', seconds = pollRate)
		

	def handleTelemetry(self):
		"""
		Set the value of cpuUtil and memUtil
		"""
		self.cpuUtilPct = self.cpuUtilTask.getTelemetryValue()
		self.memUtilPct = self.memUtilTask.getTelemetryValue()
		logging.info('CPU utilization is %s percent, and memory utilization is %s percent.', str(self.cpuUtilPct), str(self.memUtilPct))
		
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		self.dataMsgListener = listener
	
	def startManager(self):
		"""
		Start the Manager.
		
		"""
		logging.info("SystemPerformanceManager started.")
		self.scheduler.start()
		
	def stopManager(self):
		"""
		Stop the Manager.
		
		"""
		logging.info("SystemPerformanceManager stopped.")
		self.scheduler.shutdown()
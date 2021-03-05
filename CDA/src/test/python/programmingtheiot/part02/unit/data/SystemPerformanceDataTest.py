#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 

import logging
import unittest

import src.main.python.programmingtheiot.common.ConfigConst as ConfigConst

from src.main.python.programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class SystemPerformanceDataTest(unittest.TestCase):
	"""
	This test case class contains very basic unit tests for
	SystemPerformanceData. It should not be considered complete,
	but serve as a starting point for the student implementing
	additional functionality within their Programming the IoT
	environment.
	"""
	
	DEFAULT_NAME = "SystemPerformanceDataFooBar"
	DEFAULT_CPU_UTIL_DATA = 10.0
	DEFAULT_DISK_UTIL_DATA = 10.0
	DEFAULT_MEM_UTIL_DATA = 10.0
	
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing SystemPerformanceData class...")
		
	def setUp(self):
		pass

	def tearDown(self):
		pass
	
	def testDefaultValues(self):
		spd = SystemPerformanceData()
		print(spd.getName())
		self.assertEqual(spd.getName(), ConfigConst.NOT_SET)
		self.assertEqual(spd.getStatusCode(), SystemPerformanceData.DEFAULT_STATUS)
		
		self.assertEqual(spd.getCpuUtilization(), SystemPerformanceData.DEFAULT_VAL)
		self.assertEqual(spd.getDiskUtilization(), SystemPerformanceData.DEFAULT_VAL)
		self.assertEqual(spd.getMemoryUtilization(), SystemPerformanceData.DEFAULT_VAL)

	def testParameterUpdates(self):
		spd = self._createTestSystemPerformanceData()
		
		self.assertEqual(spd.getName(), self.DEFAULT_NAME)
		
		self.assertEqual(spd.getCpuUtilization(), self.DEFAULT_CPU_UTIL_DATA)
		self.assertEqual(spd.getDiskUtilization(), self.DEFAULT_DISK_UTIL_DATA)
		self.assertEqual(spd.getMemoryUtilization(), self.DEFAULT_MEM_UTIL_DATA)

	def testFullUpdate(self):
		spd = SystemPerformanceData()
		spd2 = self._createTestSystemPerformanceData()
		
		self.assertEqual(spd.getName(), ConfigConst.NOT_SET)
		
		self.assertEqual(spd.getCpuUtilization(), SystemPerformanceData.DEFAULT_VAL)
		self.assertEqual(spd.getDiskUtilization(), SystemPerformanceData.DEFAULT_VAL)
		self.assertEqual(spd.getMemoryUtilization(), SystemPerformanceData.DEFAULT_VAL)
		
		spd.updateData(spd2)
		
		self.assertEqual(spd.getName(), self.DEFAULT_NAME)
		
		self.assertEqual(spd.getCpuUtilization(), self.DEFAULT_CPU_UTIL_DATA)
		self.assertEqual(spd.getDiskUtilization(), self.DEFAULT_DISK_UTIL_DATA)
		self.assertEqual(spd.getMemoryUtilization(), self.DEFAULT_MEM_UTIL_DATA)
	
	def _createTestSystemPerformanceData(self):
		spd = SystemPerformanceData()
		spd.setName(self.DEFAULT_NAME)
		
		spd.setCpuUtilization(self.DEFAULT_CPU_UTIL_DATA)
		spd.setDiskUtilization(self.DEFAULT_DISK_UTIL_DATA)
		spd.setMemoryUtilization(self.DEFAULT_MEM_UTIL_DATA)
		
		return spd

if __name__ == "__main__":
	unittest.main()
	
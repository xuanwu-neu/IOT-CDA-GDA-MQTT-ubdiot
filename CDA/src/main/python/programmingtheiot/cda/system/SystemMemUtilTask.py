#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import psutil

from src.main.python.programmingtheiot.cda.system.BaseSystemUtilTask import BaseSystemUtilTask
from src.main.python.programmingtheiot.common import ConfigConst


class SystemMemUtilTask(BaseSystemUtilTask):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		super(SystemMemUtilTask, self).__init__(sensorName = ConfigConst.MEM_UTIL_NAME)
	
	def _getSystemUtil(self) -> float:
		return psutil.virtual_memory().percent
		
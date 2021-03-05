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

from src.main.python.programmingtheiot.common import ConfigConst
from src.main.python.programmingtheiot.data.ActuatorData import ActuatorData
from src.main.python.programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

class DoctorActuatorSimTask(BaseActuatorSimTask):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		super(DoctorActuatorSimTask, self).__init__(actuatorType = ActuatorData.DOCTOR_ACTUATOR_TYPE, simpleName = "DOCTOR", actuatorName = ConfigConst.DOCTOR_ACTUATOR_NAME)
		
	

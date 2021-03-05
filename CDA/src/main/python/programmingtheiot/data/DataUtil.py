#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#
import json
import logging
from json import JSONEncoder



from src.main.python.programmingtheiot.data.ActuatorData import ActuatorData
from src.main.python.programmingtheiot.data.SensorData import SensorData
from src.main.python.programmingtheiot.data.SystemPerformanceData import SystemPerformanceData




class DataUtil():
    """
	Shell representation of class for student implementation.

	"""

    def __init__(self, encodeToUtf8=False):
        pass

    def actuatorDataToJson(self, data: ActuatorData):
        logging.info(str(data))
        jsonData = json.dumps(data, indent=4, cls=JsonDataEncoder, ensure_ascii=True)
        logging.info((jsonData))
        return jsonData

    def sensorDataToJson(self, data: SensorData):
        jsonData = json.dumps(data, indent=4, cls=JsonDataEncoder, ensure_ascii=True)
        return jsonData

    def systemPerformanceDataToJson(self, data: SystemPerformanceData):
        jsonData = json.dumps(data, indent=4, cls=JsonDataEncoder, ensure_ascii=True)
        return jsonData

    def jsonToActuatorData(self, jsonData):
        jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
        adDict = json.loads(jsonData)
        ad = ActuatorData()
        mvDict = vars(ad)

        for key in adDict:
            if key in mvDict:
                setattr(ad, key, adDict[key])

        return ad

    def jsonToSensorData(self, jsonData):
        jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
        adDict = json.loads(jsonData)
        ad = SensorData()
        mvDict = vars(ad)

        for key in adDict:
            if key in mvDict:
                setattr(ad, key, adDict[key])

        return ad

    def jsonToSystemPerformanceData(self, jsonData):
        jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
        adDict = json.loads(jsonData)
        ad = SystemPerformanceData()
        mvDict = vars(ad)

        for key in adDict:
            if key in mvDict:
                setattr(ad, key, adDict[key])

        return ad


class JsonDataEncoder(JSONEncoder):
    """
	Convenience class to facilitate JSON encoding of an object that
	can be converted to a dict.

	"""

    def default(self, o):
        return o.__dict__

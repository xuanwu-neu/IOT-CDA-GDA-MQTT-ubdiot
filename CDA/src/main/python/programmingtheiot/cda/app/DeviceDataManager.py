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

from src.main.python.programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from src.main.python.programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector

from src.main.python.programmingtheiot.cda.system.ActuatorAdapterManager import ActuatorAdapterManager
from src.main.python.programmingtheiot.cda.system.SensorAdapterManager import SensorAdapterManager
from src.main.python.programmingtheiot.cda.system.SystemPerformanceManager import SystemPerformanceManager

import src.main.python.programmingtheiot.common.ConfigConst as ConfigConst

from src.main.python.programmingtheiot.common.ConfigUtil import ConfigUtil
from src.main.python.programmingtheiot.common.IDataMessageListener import IDataMessageListener
from src.main.python.programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from src.main.python.programmingtheiot.data.DataUtil import DataUtil
from src.main.python.programmingtheiot.data.ActuatorData import ActuatorData
from src.main.python.programmingtheiot.data.SensorData import SensorData
from src.main.python.programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
from src.main.python.programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector


class DeviceDataManager(IDataMessageListener):
    """
    Shell representation of class for student implementation.

    """

    def __init__(self, enableMqtt: bool = True, enableCoap: bool = False):
        self.dataUtil = DataUtil()

        self.enableMqttClient = enableMqtt

        self.sysPerfManager = SystemPerformanceManager()
        self.sysPerfManager.setDataMessageListener(self)

        self.sensorAdapterManager = SensorAdapterManager()
        self.sensorAdapterManager.setDataMessageListener(self)

        self.actuatorAdapterManager = ActuatorAdapterManager()
        self.actuatorAdapterManager.setDataMessageListener(self)

        self.configUtil = ConfigUtil()
        self.enableHandleTempChangeOnDevice = self.configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE,
                                                                         ConfigConst.ENABLE_HANDLE_TEMP_CHANGE_ON_DEVICE_KEY)

        self.triggerHvacTempFloor = self.configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE,
                                                             ConfigConst.TRIGGER_HVAC_TEMP_FLOOR_KEY);

        self.triggerHvacTempCeiling = self.configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE,
                                                               ConfigConst.TRIGGER_HVAC_TEMP_CEILING_KEY);
        self.triggerHvacTempFloor = 10.0
        self.triggerHvacTempCeiling = 30.0

        if self.enableMqttClient:
            self.mqttClient = MqttClientConnector()
            self.mqttClient.setDataMessageListener(self)

    def handleActuatorCommandResponse(self, data: ActuatorData) -> bool:

        d = self.dataUtil.actuatorDataToJson(data)
        logging.info("Incoming actuator response received" + d)
        #self.mqttClient.publishMessage(ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE, d, 1)
        self._handleUpstreamTransmission(ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE, d)


    def handleIncomingMessage(self, resourceEnum: ResourceNameEnum, msg: str) -> bool:
        logging.info("called handleIncomingMessage function")
        actuatorData = self.dataUtil.jsonToActuatorData(msg)
        if not actuatorData:
            logging.warning("not legal JSON data")
        else:
            self._handleIncomingDataAnalysis(msg)

    def handleSensorMessage(self, data: SensorData) -> bool:
        logging.info("CDA Handling sensor message...")

        d = self.dataUtil.sensorDataToJson(data)
        #self._handleUpstreamTransmission(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, d)

        '''
        just for test : CDA analysis temperature data
        '''

        if data.sensorType is SensorData.HEART_RATE_SENSOR_TYPE:
            self._handleSensorDataAnalysis(data)


        if self.enableMqttClient:
            self.mqttClient.publishMessage(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, d, 0)

        return True;


    def handleSystemPerformanceMessage(self, data: SystemPerformanceData) -> bool:
        logging.info("Handle system performance message...")

        d = self.dataUtil.systemPerformanceDataToJson(data)

        if self.enableMqttClient:
            self.mqttClient.publishMessage(ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE, d)


    def startManager(self):
        logging.info('DeviceDataManager was started')
        self.sysPerfManager.startManager()
        self.sensorAdapterManager.startManager()
        if self.enableMqttClient:
            self.mqttClient.connectClient()

    def stopManager(self):
        logging.info('DeviceDataManager was stopped')
        self.sysPerfManager.stopManager()
        self.sensorAdapterManager.stopManager()
        if self.enableMqttClient:
            self.mqttClient.disconnectClient()

    def _handleIncomingDataAnalysis(self, msg: str):
        """
		Call this from handleIncomeMessage() to determine if there's
		any action to take on the message. Steps to take:
		1) Validate msg: Most will be ActuatorData, but you may pass other info as well.
		2) Convert msg: Use DataUtil to convert if appropriate.
		3) Act on msg: Determine what - if any - action is required, and execute.
		"""
        logging.info('called _handleIncomingDataAnalysis function')

        actuatorData = self.dataUtil.jsonToActuatorData(msg)
        if not actuatorData:
            logging.warning("not legal JSON data")
        else:
            self.actuatorAdapterManager.sendActuatorCommand(actuatorData)

    def _handleSensorDataAnalysis(self, data: SensorData):
        """
        Call this from handleSensorMessage() to determine if there's
        any action to take on the message. Steps to take:
        1) Check config: Is there a rule or flag that requires immediate processing of data?
        2) Act on data: If # 1 is true, determine what - if any - action is required, and execute.
        """

        logging.info("_handleSensorDataAnalysis is called." + str(data))
        #actuatorData = ActuatorData(ActuatorData.PATIENT_ACTUATOR_TYPE)
        if data.getValue() > 90:
            actuatorData = ActuatorData(ActuatorData.HEART_RATE_ACTUATOR_TYPE_UP)
            actuatorData.setCommand(ActuatorData.COMMAND_ON)
            self.actuatorAdapterManager.sendActuatorCommand(actuatorData)


    def _handleUpstreamTransmission(self, resourceName: ResourceNameEnum, msg: str):
        """
        Call this from handleActuatorCommandResponse(), handlesensorMessage(), and handleSystemPerformanceMessage()
        to determine if the message should be sent upstream. Steps to take:
        1) Check connection: Is there a client connection configured (and valid) to a remote MQTT or CoAP server?
        2) Act on msg: If # 1 is true, send message upstream using one (or both) client connections.
        """
        logging.info("_handleUpstreamTransmission is called.")
        if self.enableMqttClient:
            logging.info("mqtt handle publish")
            self.mqttClient.publishMessage(resourceName, msg, 0)

    def handleActuatorCommandMessage(self, data: ActuatorData) -> bool:
        if data:
            logging.info("Processing actuator command message.")

            # TODO: add further validation before sending the command
            self.actuatorAdapterManager.sendActuatorCommand(data)
            return True
        else:
            logging.warning("Received invalid ActuatorData command message. Ignoring.")
            return False

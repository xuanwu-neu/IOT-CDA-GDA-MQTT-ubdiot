#####
#
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
#
# Copyright (c) 2020 by Andrew D. King
#

import logging
import time
import unittest

from time import sleep

import src.main.python.programmingtheiot.common.ConfigConst as ConfigConst

from src.main.python.programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from src.main.python.programmingtheiot.common.ConfigUtil import ConfigUtil
from src.main.python.programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from src.main.python.programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener
from src.main.python.programmingtheiot.data.DataUtil import DataUtil
from src.main.python.programmingtheiot.data.SensorData import SensorData


class MqttClientPerformanceTest(unittest.TestCase):
    NS_IN_MILLIS = 1000000

    # NOTE: We'll use only 10,000 requests for MQTT
    MAX_TEST_RUNS = 10000

    @classmethod
    def setUpClass(self):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level=logging.DEBUG)

    def setUp(self):
        self.mqttClient = MqttClientConnector(clientID='CDAMqttClientPerformanceTest001')
        self.cfg = ConfigUtil()
        pass

    def tearDown(self):
        pass

    # @unittest.skip("Ignore for now.")
    def testConnectAndDisconnect(self):
        startTime = time.time_ns()
        delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY,
                                    ConfigConst.DEFAULT_KEEP_ALIVE)
        self.assertTrue(self.mqttClient.connectClient())
        sleep(delay + 5)
        self.assertTrue(self.mqttClient.disconnectClient())

        endTime = time.time_ns()
        elapsedMillis = (endTime - startTime) / self.NS_IN_MILLIS

        logging.info("Connect and Disconnect: " + str(elapsedMillis) + " ms")

    # @unittest.skip("Ignore for now.")
    def testPublishQoS0(self):
        self._execTestPublish(self.MAX_TEST_RUNS, 0)

    # @unittest.skip("Ignore for now.")
    def testPublishQoS1(self):
        self._execTestPublish(self.MAX_TEST_RUNS, 1)

    # @unittest.skip("Ignore for now.")
    def testPublishQoS2(self):
        self._execTestPublish(self.MAX_TEST_RUNS, 2)

    def _execTestPublish(self, maxTestRuns: int, qos: int):
        self.assertTrue(self.mqttClient.connectClient())

        sensorData = SensorData()
        payload = DataUtil().sensorDataToJson(sensorData)

        startTime = time.time_ns()

        for seqNo in range(0, maxTestRuns):
            self.mqttClient.publishMessage(resource=ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, msg=payload, qos=qos)

        endTime = time.time_ns()
        elapsedMillis = (endTime - startTime) / self.NS_IN_MILLIS

        self.assertTrue(self.mqttClient.disconnectClient())

        logging.info("Publish message - QoS " + str(qos) + " [" + str(maxTestRuns) + "]: " + str(elapsedMillis) + " ms")


if __name__ == "__main__":
    unittest.main()

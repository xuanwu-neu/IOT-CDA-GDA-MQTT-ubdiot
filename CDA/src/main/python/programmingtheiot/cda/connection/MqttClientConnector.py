#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import paho.mqtt.client as mqttClient

from src.main.python.programmingtheiot.common import ConfigUtil
from src.main.python.programmingtheiot.common import ConfigConst

from src.main.python.programmingtheiot.common.IDataMessageListener import IDataMessageListener
from src.main.python.programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from src.main.python.programmingtheiot.cda.connection.IPubSubClient import IPubSubClient
from src.main.python.programmingtheiot.data.DataUtil import DataUtil

DEFAULT_QOS = 0


class MqttClientConnector(IPubSubClient):
    """
    Retrieve the host, port, and keep alive values from the configuration file using ConfigUtil.
    """

    def __init__(self, clientID: str = None):
        """
        Default constructor. This will set remote broker information and client connection
        information based on the default configuration file contents.

        @param clientID Defaults to None. Can be set by caller. If this is used, it's
        critically important that a unique, non-conflicting name be used so to avoid
        causing the MQTT broker to disconnect any client using the same name. With
        auto-reconnect enabled, this can cause a race condition where each client with
        the same clientID continuously attempts to re-connect, causing the broker to
        disconnect the previous instance.
        """
        self.clientID = None;
        self.mc = None;
        self.config = ConfigUtil.ConfigUtil()

        self.host = self.config.getProperty(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.HOST_KEY,
                                            ConfigConst.DEFAULT_HOST)

        self.port = self.config.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.PORT_KEY,
                                           ConfigConst.DEFAULT_MQTT_PORT)

        self.keepAlive = self.config.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY,
                                                ConfigConst.DEFAULT_KEEP_ALIVE)
        self.dataMsgListener = None

        logging.info('\tMQTT Broker Host: ' + self.host)
        logging.info('\tMQTT Broker Port: ' + str(self.port))
        logging.info('\tMQTT Keep Alive:  ' + str(self.keepAlive))

    '''
    initialize MQTT client when it absent
    assign callback functions to MQTT client
    start loop
    @return false if client already connected, true if successed
    '''

    def connectClient(self) -> bool:

        if not self.mc:
            self.mc = mqttClient.Client(client_id=self.clientID, clean_session=True)
            self.mc.on_connect = self.onConnect
            self.mc.on_disconnect = self.onDisconnect
            self.mc.on_message = self.onMessage
            self.mc.on_publish = self.onPublish
            self.mc.on_subscribe = self.onSubscribe

        if not self.mc.is_connected():
            self.mc.connect(self.host, self.port, self.keepAlive)
            self.mc.loop_start()
            logging.info("Attempting to connect to MQTT broker: localhost")
            return True
        else:
            logging.warn('MQTT client is already connected. Ignoring connect request.')
            return False

    '''
    disconnect from the broker if currently connected
    then stop the network loop
    @return false if client already disconnected, true if successed
    '''

    def disconnectClient(self) -> bool:
        if self.mc.is_connected():
            self.mc.disconnect()
            logging.info("Disconnecting from MQTT broker: localhost")
            self.mc.loop_stop()

        return True

    '''
    when connect to client, subscribe to actuator topic
    '''

    def onConnect(self, client, userdata, flags, rc):
        logging.info('[Callback] Connected to MQTT broker. Result code: ' + str(rc))

        # NOTE: Use the QoS of your choice - '1' is only an example
        self.mc.subscribe(topic=ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE.value, qos=0)
        self.mc.message_callback_add(sub=ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE.value,
                                     callback=self.onActuatorCommandMessage)

    '''
    will be called when disconnected
    '''

    def onDisconnect(self, client, userdata, rc):
        logging.info("[Callback] Disconnected from MQTT broker. Result code: " + str(rc))
        pass

    '''
    will be called when got message
    '''

    def onMessage(self, client, userdata, msg):
        logging.info("[Callback] MQTT onMessage")

    '''
    will be called when publish message
    '''

    def onPublish(self, client, userdata, mid):
        # logging.info("[Callback] MQTT onPublish, mid = " + str(mid))
        pass

    '''
    will be called when subscribe to a specific topic
    '''

    def onSubscribe(self, client, userdata, mid, granted_qos):
        logging.info("[Callback] MQTT onSubscribe, mid = " + str(mid))
        pass

    '''
    Create a new callback method to handle incoming subscription messages for actuator command messages
    '''

    def onActuatorCommandMessage(self, client, userdata, msg):
        logging.info('[Callback] Actuator command message received. Topic: %s.', msg.topic)
        if self.dataMsgListener:
            try:
                actuatorData = DataUtil().jsonToActuatorData(msg.payload.decode())
                self.dataMsgListener.handleActuatorCommandMessage(actuatorData)
            except:
                logging.exception("Failed to convert incoming actuation command payload to ActuatorData: ")

    '''
    check topic name and qos, make sure both of them are legal.
    call publish function of MQTT client.
    @return false when topicName illegal or encounter publish exceptions
    @return true if successfully published

    '''

    def publishMessage(self, resource: ResourceNameEnum, msg, qos: int = IPubSubClient.DEFAULT_QOS):
        # logging.info("MQTT publishing message: " + str(resource))
        # If the topic is invalid, return False
        if not (resource):
            return False
        if qos < 0 or qos > 2:
            qos = IPubSubClient.DEFAULT_QOS
        try:
            # self.mc.publish(str(resource), qos)
            # logging.info("mqttClient publishing...")
            msgInfo = self.mc.publish(topic=resource.value, payload=msg, qos=qos)
        # msgInfo.wait_for_publish()
        # logging.info("mqttClient pub success...")
        except:
            logging.info("mqttClient pub error...")
            return False
        # If the publish is valid and the call to the MQTT client is successful, return True.
        return True;

    '''
    check topic name and QoS, make sure both of them are legal.
    call subscribe function of MQTT client.
    @return false when topicName illegal or encounter subscribe exceptions
    @return true if successfully subscribed
    '''

    def subscribeToTopic(self, resource: ResourceNameEnum, qos: int = IPubSubClient.DEFAULT_QOS):
        logging.info("MQTT subscribe to topic")
        # If the topic is invalid, return False

        if not (resource):
            return False
        if qos < 0 or qos > 2:
            qos = IPubSubClient.DEFAULT_QOS

        try:
            self.mc.subscribe(str(resource), qos)
        except:
            return False
        # If the publish is valid and the call to the MQTT client is successful, return True.
        return True;

    def unsubscribeFromTopic(self, resource: ResourceNameEnum):
        logging.info("MQTT unsubscribe from topic")

    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        logging.info("MQTT set data message listener")
        if listener:
            self.dataMsgListener = listener
            return True

        return False

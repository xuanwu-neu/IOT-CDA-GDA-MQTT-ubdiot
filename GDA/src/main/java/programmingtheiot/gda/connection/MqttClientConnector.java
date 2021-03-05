/**
 * This class is part of the Programming the Internet of Things project.
 *
 * It is provided as a simple shell to guide the student and assist with
 * implementation for the Programming the Internet of Things exercises,
 * and designed to be modified by the student as needed.
 */

package programmingtheiot.gda.connection;

import java.io.File;
import java.util.Properties;
import java.util.concurrent.Semaphore;
import java.util.logging.Level;
import java.util.logging.Logger;
import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import javax.net.ssl.SSLSocketFactory;
import programmingtheiot.common.SimpleCertManagementUtil;
import programmingtheiot.data.ActuatorData;
import programmingtheiot.data.DataUtil;
import programmingtheiot.data.SensorData;
import programmingtheiot.data.SystemPerformanceData;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttMessageListener;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.MqttPersistenceException;
import org.eclipse.paho.client.mqttv3.MqttSecurityException;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

import programmingtheiot.common.ConfigConst;
import programmingtheiot.common.ConfigUtil;
import programmingtheiot.common.IDataMessageListener;
import programmingtheiot.common.ResourceNameEnum;

/**
 * Shell representation of class for student implementation.
 *
 */
public class MqttClientConnector implements IPubSubClient, MqttCallbackExtended {
	// static

	private static final Logger _Logger =
			Logger.getLogger(MqttClientConnector.class.getName());
	private String host;
	private int port;
	private int brokerKeepAlive;
	private String clientID;
	private MemoryPersistence persistence;
	private MqttConnectOptions connOpts;
	private String brokerAddr;
	private String protocol = ConfigConst.DEFAULT_MQTT_PROTOCOL;
	private MqttClient mqttClient = null;
	private boolean useCloudGatewayConfig = false;

	// params
	private int DEFAULT_QOS = 0;
	private String pemFileName;
	private boolean enableEncryption;
	private boolean useCleanSession;
	private boolean enableAutoReconnect;
	private IDataMessageListener dataMsgListener = null;
	private boolean reconnect = false;

	// constructors

	/**
	 * Default.
	 */
	public MqttClientConnector()
	{
		this(false);
	}

	public MqttClientConnector(boolean useCloudGatewayConfig)
	{
		super();

		this.useCloudGatewayConfig = useCloudGatewayConfig;

		if (useCloudGatewayConfig) {
			initClientParameters(ConfigConst.CLOUD_GATEWAY_SERVICE);
		} else {
			initClientParameters(ConfigConst.MQTT_GATEWAY_SERVICE);
		}
	}


	// public methods
	/**
	 * mqttconnector connect
	 */
	@Override
	public boolean connectClient() {
		try {
			if (this.mqttClient == null) {
				this.mqttClient = new MqttClient(this.brokerAddr, this.clientID, this.persistence);
				this.mqttClient.setCallback(this);
				//this.connectComplete()
			}

			if (! this.mqttClient.isConnected()) {
				this.mqttClient.connect(this.connOpts);
			}else {
				return false;
			}

		}catch (Exception e) {
			_Logger.info("MQTT connect FAILED: " + e.getMessage());
			e.printStackTrace();
			return false;
		}

		return true;
	}
	/**
	 * mqttconnector disconnect
	 */
	@Override
	public boolean disconnectClient() {
		try {
			if (this.mqttClient != null && this.mqttClient.isConnected()) {
				this.mqttClient.disconnect();
			}else {
				return false;
			}

		}catch (Exception e) {
			_Logger.info(e.getStackTrace().toString());
			return false;
		}
		_Logger.info("MQTT disconnect client");
		return true;

	}
	/**
	 * mqttconnector publish
	 */
	@Override
	public boolean publishMessage(ResourceNameEnum topicName, String msg, int qos) {

		_Logger.info("MQTT publishing message: " + topicName.getResourceName());
		if(topicName == null) {
			return false;
		}
		if(qos < 0 || qos > 2) {
			qos = DEFAULT_QOS;
		}
		try {
			mqttClient.publish(topicName.getResourceName(), msg.getBytes(), qos, false);
		} catch (MqttPersistenceException e) {
			e.printStackTrace();
			_Logger.info("MQTT publish message failed");
		} catch (MqttException e) {
			_Logger.info("MQTT publish message failed");
			e.printStackTrace();
		}

		return true;

	}
	/**
	 * mqttconnector  check sconnect
	 */
	public boolean isConnected() {
		return mqttClient.isConnected();
	}



	/**
	 * mqttconnector subscribeToTopic
	 */
	@Override
	public boolean subscribeToTopic(ResourceNameEnum topicName, int qos) {
		_Logger.info("MQTT subscribing to topic");
		if(topicName == null) {
			return false;
		}
		if(qos < 0 || qos > 2) {
			qos = DEFAULT_QOS;
		}
		try {
			mqttClient.subscribe(topicName.toString(), qos);
			_Logger.info("MQTT subscribe message successed");
		} catch (MqttPersistenceException e) {
			e.printStackTrace();
			_Logger.info("MQTT subscribe message failed");
		} catch (MqttException e) {
			_Logger.info("MQTT subscribe message failed");
			e.printStackTrace();
		}
		return true;
	}
	/**
	 * mqttconnector unsubscribeToTopic
	 */
	@Override
	public boolean unsubscribeFromTopic(ResourceNameEnum topicName) {
		_Logger.info("MQTT unsubscribe from topic");
		return true;
	}
	/**
	 * mqttconnector setDataMessageListener
	 */
	@Override
	public boolean setDataMessageListener(IDataMessageListener listener) {
		_Logger.info("setDataMessageListener is called");
		if (listener != null) {
			this.dataMsgListener = listener;
			return true;
		}

		return false;
	}

	// callbacks
	/**
	 * mqttconnector callback to manage connectComplete
	 */
	@Override
	public void connectComplete(boolean reconnect, String serverURI) {
		_Logger.info("MQTT connection successful (is reconnect = " + reconnect + "). Broker: " + serverURI);

		int qos = 1;

		// Option 2
		try {
			this.mqttClient.subscribe(
					ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE.getResourceName(),
					qos,
					new SensorResponseMessageListener(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, this.dataMsgListener));
			_Logger.info("subscribe to CDA sensor msg topic successfully.");
		} catch (MqttException e) {
			_Logger.warning("Failed to subscribe to CDA sensor msg topic.");
		}

		try {
			this.mqttClient.subscribe(
					ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE.getResourceName(),
					qos,
					new ActuatorResponseMessageListener(ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE, this.dataMsgListener));
			_Logger.info("subscribe to CDA actuator response msg topic successfully.");
		} catch (MqttException e) {
			_Logger.warning("Failed to subscribe to CDA actuator response topic.");
			System.out.println(e.getMessage().toString());
		}

		try {
			this.mqttClient.subscribe(
					ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE.getResourceName(),
					qos,
					new SysPerfResponseMessageListener(ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE, this.dataMsgListener));
			_Logger.info("subscribe to CDA system perf msg topic successfully.");
		} catch (MqttException e) {
			_Logger.warning("Failed to subscribe to CDA system performance response topic.");
		}
	}
	/**
	 * mqttconnector connectionLost
	 */
	@Override
	public void connectionLost(Throwable t) {
		_Logger.info("MQTT connection lost");
	}
	/**
	 * mqttconnector deliveryComplete
	 */
	@Override
	public void deliveryComplete(IMqttDeliveryToken token) {
		_Logger.info("MQTT delivery complete");

	}
	/**
	 * MQTT message arrived (from cloud)
	 */
	@Override
	public void messageArrived(String topic, MqttMessage msg) throws Exception {
		_Logger.info("MQTT message arrived (from cloud) : " + msg);
		String payload = new String(msg.getPayload());


		//JsonElement je = new JsonParser().parse(payload);
		JsonParser jp = new JsonParser();

		JsonObject jo = jp.parse(payload).getAsJsonObject();

		int value = jo.get("value").getAsInt();

		System.out.print(value);
		DataUtil dataUtil = DataUtil.getInstance();
		ActuatorData actuatorData = new ActuatorData();
		if (value == ActuatorData.BLOOD_PRESSURE_ACTUATOR_TYPE_DOWN) {
			actuatorData.setActuatorType(ActuatorData.BLOOD_PRESSURE_ACTUATOR_TYPE_DOWN);
		}else if (value == ActuatorData.BLOOD_PRESSURE_ACTUATOR_TYPE_UP) {
			actuatorData.setActuatorType(ActuatorData.BLOOD_PRESSURE_ACTUATOR_TYPE_UP);
		}else if (value == ActuatorData.BODY_TEMP_ACTUATOR_TYPE_DOWN) {
			actuatorData.setActuatorType(ActuatorData.BODY_TEMP_ACTUATOR_TYPE_DOWN);
		}else if (value == ActuatorData.BODY_TEMP_ACTUATOR_TYPE_UP) {
			actuatorData.setActuatorType(ActuatorData.BODY_TEMP_ACTUATOR_TYPE_UP);
		}
		actuatorData.setCommand(1);
		String jsonActuator = dataUtil.actuatorDataToJson(actuatorData);

		if (this.dataMsgListener != null) {
			this.dataMsgListener.handleIncomingMessage(ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, jsonActuator);
			//this.dataMsgListener.handleActuatorCommandResponse(ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, actuatorData);
		}else {
			_Logger.info("DataMsgListener is null.");
		}
	}


	// private methods

	/**
	 * Called by the constructor to set the MQTT client parameters to be used for the connection.
	 *
	 * @param configSectionName The name of the configuration section to use for
	 *                          the MQTT client configuration parameters.
	 */
	private void initClientParameters(String configSectionName) {
		// TODO: implement this
		ConfigUtil configUtil = ConfigUtil.getInstance();

		this.host =
				configUtil.getProperty(
						configSectionName, ConfigConst.HOST_KEY, ConfigConst.DEFAULT_HOST);
		this.port =
				configUtil.getInteger(
						configSectionName, ConfigConst.PORT_KEY, ConfigConst.DEFAULT_MQTT_PORT);
		this.brokerKeepAlive =
				configUtil.getInteger(
						configSectionName, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE);
		this.enableEncryption =
				configUtil.getBoolean(
						configSectionName, ConfigConst.ENABLE_CRYPT_KEY);
		this.pemFileName =
				configUtil.getProperty(
						configSectionName, ConfigConst.CERT_FILE_KEY);

		// Paho Java client requires a client ID
		this.clientID = MqttClient.generateClientId();

		// these are specific to the MQTT connection which will be used during connect
		this.persistence = new MemoryPersistence();
		this.connOpts    = new MqttConnectOptions();

		this.connOpts.setKeepAliveInterval(this.brokerKeepAlive);
		//this.connOpts.setCleanSession(this.useCleanSession);
		//this.connOpts.setAutomaticReconnect(this.enableAutoReconnect);
		this.connOpts.setCleanSession(false);
		this.connOpts.setAutomaticReconnect(false);

		// if encryption is enabled, try to load and apply the cert(s)
		if (this.enableEncryption) {
			initSecureConnectionParameters(configSectionName);
		}

		// if there's a credential file, try to load and apply them
		if (configUtil.hasProperty(configSectionName, ConfigConst.CRED_FILE_KEY)) {
			initCredentialConnectionParameters(configSectionName);
		}

		// NOTE: URL does not have a protocol handler for "tcp" or "ssl",
		// so construct the URL manually
		this.brokerAddr  = this.protocol + "://" + this.host + ":" + this.port;

		_Logger.info("Using URL for broker conn: " + this.brokerAddr);
	}

	/**
	 * Called by {@link #initClientParameters(String)} to load credentials.
	 *
	 * @param configSectionName The name of the configuration section to use for
	 *                          the MQTT client configuration parameters.
	 */
	private void initCredentialConnectionParameters(String configSectionName) {
		// TODO: implement this
		this.connOpts.setUserName("BBFF-eMMU32LIII45flv6G4qmQvJTx5uafw");
	}

	/**
	 * Called by {@link #initClientParameters(String)} to enable encryption.
	 *
	 * @param configSectionName The name of the configuration section to use for
	 *                          the MQTT client configuration parameters.
	 */
	private void initSecureConnectionParameters(String configSectionName) {
		// TODO: implement this
		ConfigUtil configUtil = ConfigUtil.getInstance();

		try {
			_Logger.info("Configuring TLS...");

			if (this.pemFileName != null) {
				File file = new File(this.pemFileName);

				if (file.exists()) {
					_Logger.info("PEM file valid. Using secure connection: " + this.pemFileName);
				} else {
					this.enableEncryption = false;

					_Logger.log(Level.WARNING, "PEM file invalid. Using insecure connection: " + pemFileName, new Exception());

					return;
				}
			}

			SSLSocketFactory sslFactory =
					SimpleCertManagementUtil.getInstance().loadCertificate(this.pemFileName);

			this.connOpts.setSocketFactory(sslFactory);

			// override current config parameters
			this.port =
					configUtil.getInteger(
							configSectionName, ConfigConst.SECURE_PORT_KEY, ConfigConst.DEFAULT_MQTT_SECURE_PORT);

			this.protocol = ConfigConst.DEFAULT_MQTT_SECURE_PROTOCOL;

			_Logger.info("TLS enabled.");
		} catch (Exception e) {
			_Logger.log(Level.SEVERE, "Failed to initialize secure MQTT connection. Using insecure connection.", e);

			this.enableEncryption = false;
		}
	}
 	/*
 	 listen to handle ActuatorResponseMessage
 	 */
	private class ActuatorResponseMessageListener implements IMqttMessageListener {
		private ResourceNameEnum resource = null;
		private IDataMessageListener dataMsgListener = null;

		ActuatorResponseMessageListener(ResourceNameEnum resource, IDataMessageListener dataMsgListener)
		{
			this.resource = resource;
			this.dataMsgListener = dataMsgListener;
			_Logger.info("actuator listener is created");
		}

		@Override
		public void messageArrived(String topic, MqttMessage message) throws Exception
		{
			_Logger.info("messageArrive is created");
			try {
				ActuatorData actuatorData =
						DataUtil.getInstance().jsonToActuatorData(new String(message.getPayload()));
				_Logger.info("getData is created");
				if (this.dataMsgListener != null) {
					this.dataMsgListener.handleActuatorCommandResponse(resource, actuatorData);
					_Logger.info("handle is created");
				}
			} catch (Exception e) {
				_Logger.warning("Failed to convert message payload to ActuatorData." + "\n" + e.getStackTrace());
			}
		}
	}
	/*
 	 listen to handle SysPerfResponseMessageListener
 	 */
	private class SysPerfResponseMessageListener implements IMqttMessageListener
	{
		private ResourceNameEnum resource = null;
		private IDataMessageListener dataMsgListener = null;

		SysPerfResponseMessageListener(ResourceNameEnum resource, IDataMessageListener dataMsgListener)
		{
			this.resource = resource;
			this.dataMsgListener = dataMsgListener;
		}

		@Override
		public void messageArrived(String topic, MqttMessage message) throws Exception
		{
			try {
				SystemPerformanceData sysData =
						DataUtil.getInstance().jsonToSystemPerformanceData(new String(message.getPayload()));

				if (this.dataMsgListener != null) {
					this.dataMsgListener.handleSystemPerformanceMessage(resource, sysData);
				}
			} catch (Exception e) {
				_Logger.warning("Failed to convert message payload to ActuatorData." + "\n" + e.getStackTrace());
			}
		}

	}
	/*
 	 listen to handle SensorResponseMessageListener
 	 */
	private class SensorResponseMessageListener implements IMqttMessageListener
	{

		private ResourceNameEnum resource = null;
		private IDataMessageListener dataMsgListener = null;

		SensorResponseMessageListener(ResourceNameEnum resource, IDataMessageListener dataMsgListener)
		{
			this.resource = resource;
			this.dataMsgListener = dataMsgListener;
		}

		@Override
		public void messageArrived(String topic, MqttMessage message) throws Exception
		{
			_Logger.info("MQTT Sensor Message Arrived : " + topic);
			try {
				SensorData sensorData =
						DataUtil.getInstance().jsonToSensorData(new String(message.getPayload()));

				if (this.dataMsgListener != null) {
					this.dataMsgListener.handleSensorMessage(resource, sensorData);
				}
			} catch (Exception e) {
				_Logger.warning("Failed to convert message payload to ActuatorData." + "\n" + e.getStackTrace());
			}
		}

	}

	protected boolean publishMessage(String topic, byte[] payload, int qos)
	{
		MqttMessage message = new MqttMessage(payload);

		if (qos < 0 || qos > 2) {
			qos = 0;
		}

		message.setQos(qos);

		// NOTE: you may want to log the exception stack trace if the call fails
		try {
			_Logger.info("Publishing message to topic: " + topic);

			this.mqttClient.publish(topic, message);

			return true;
		} catch (MqttPersistenceException e) {
			_Logger.warning("Persistence exception thrown when publishing to topic: " + topic);
		} catch (MqttException e) {
			_Logger.warning("MQTT exception thrown when publishing to topic: " + topic);
		}

		return false;
	}

	protected boolean subscribeToTopic(String topic, int qos)
	{
		// NOTE: you may want to log the exception stack trace if the call fails
		try {
			this.mqttClient.subscribe(topic, qos);

			return true;
		} catch (MqttException e) {
			_Logger.warning("Failed to subscribe to topic: " + topic);
		}

		return false;
	}

	protected boolean unsubscribeFromTopic(String topic)
	{
		// NOTE: you may want to log the exception stack trace if the call fails
		try {
			this.mqttClient.unsubscribe(topic);

			return true;
		} catch (MqttException e) {
			_Logger.warning("Failed to unsubscribe from topic: " + topic);
		}

		return false;
	}

}
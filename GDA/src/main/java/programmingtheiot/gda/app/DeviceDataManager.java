/**
 * This class is part of the Programming the Internet of Things project.
 *
 * It is provided as a simple shell to guide the student and assist with
 * implementation for the Programming the Internet of Things exercises,
 * and designed to be modified by the student as needed.
 */

package programmingtheiot.gda.app;

import java.util.Set;
import java.util.logging.Level;
import java.util.logging.Logger;

import programmingtheiot.common.ConfigConst;
import programmingtheiot.common.ConfigUtil;
import programmingtheiot.common.DefaultDataMessageListener;
import programmingtheiot.common.IDataMessageListener;
import programmingtheiot.common.ResourceNameEnum;

import programmingtheiot.data.ActuatorData;
import programmingtheiot.data.BaseIotData;
import programmingtheiot.data.DataUtil;
import programmingtheiot.data.SensorData;
import programmingtheiot.data.SystemPerformanceData;
import programmingtheiot.data.SystemStateData;

import programmingtheiot.gda.connection.CloudClientConnector;
import programmingtheiot.gda.connection.CoapServerGateway;
import programmingtheiot.gda.connection.ICloudClient;
import programmingtheiot.gda.connection.IPersistenceClient;
import programmingtheiot.gda.connection.IPubSubClient;
import programmingtheiot.gda.connection.IRequestResponseClient;
import programmingtheiot.gda.connection.MqttClientConnector;
import programmingtheiot.gda.connection.RedisPersistenceAdapter;
import programmingtheiot.gda.connection.SmtpClientConnector;
import programmingtheiot.gda.system.SystemPerformanceManager;


public class DeviceDataManager implements IDataMessageListener
{
	// static
	private static final int thresholdValue = 25;
	private static final Logger _Logger =
			Logger.getLogger(DeviceDataManager.class.getName());

	// private var's

	private boolean enableMqttClient = true;
	private boolean enableCoapServer = false;
	private boolean enableCloudClient = true;
	private boolean enableSmtpClient = false;
	private boolean enablePersistenceClient = true;

	private IPubSubClient mqttClient = null;
	//private ICloudClient cloudClient = null;
	private CloudClientConnector cloudClient = null;
	private IPersistenceClient persistenceClient = null;
	private IRequestResponseClient smtpClient = null;
	private CoapServerGateway coapServer = null;
	private ConfigUtil configUtil;
	private DataUtil dataUtil;
	private SystemPerformanceManager sysPerfManager;


	// constructors
	/**
	 * default constructor
	 * Use ConfigUtil to retrieve communication connection enablement flags from the GatewayDevice section.
	 * initialize connections
	 */
	public DeviceDataManager()
	{
		super();
		configUtil = ConfigUtil.getInstance();
		dataUtil = DataUtil.getInstance();
		sysPerfManager = new SystemPerformanceManager(10);
		sysPerfManager.setDataMessageListener(this);
		this.enableMqttClient  = configUtil.getBoolean(ConfigConst.GATEWAY_DEVICE, ConfigConst.ENABLE_MQTT_CLIENT_KEY);
		this.enableCoapServer  = configUtil.getBoolean(ConfigConst.GATEWAY_DEVICE, ConfigConst.ENABLE_COAP_SERVER_KEY);
		this.enableCloudClient = configUtil.getBoolean(ConfigConst.GATEWAY_DEVICE, ConfigConst.ENABLE_CLOUD_CLIENT_KEY);
		this.enableSmtpClient  = configUtil.getBoolean(ConfigConst.GATEWAY_DEVICE, ConfigConst.ENABLE_SMTP_CLIENT_KEY);
		this.enablePersistenceClient = configUtil.getBoolean(ConfigConst.GATEWAY_DEVICE, ConfigConst.ENABLE_PERSISTENCE_CLIENT_KEY);
		initConnections();
	}

	/**
	 * constructor
	 * set enablement user flag passed in
	 * then initialize connections
	 */
	public DeviceDataManager(
			boolean enableMqttClient,
			boolean enableCoapClient,
			boolean enableCloudClient,
			boolean enableSmtpClient,
			boolean enablePersistenceClient)
	{
		super();

		sysPerfManager = new SystemPerformanceManager(10);
		sysPerfManager.setDataMessageListener(this);

		this.enableCloudClient = enableCloudClient;
		this.enableCoapServer = enableCoapClient;
		this.enableMqttClient = enableMqttClient;
		this.enablePersistenceClient = enablePersistenceClient;
		this.enableSmtpClient = enableSmtpClient;
		initConnections();
	}


	// public methods
	/**
	 * Check if the persistence client is active
	 * if so, do logging and event tracking
	 */
	@Override
	public boolean handleActuatorCommandResponse(ResourceNameEnum resourceName, ActuatorData data)
	{
		_Logger.info("handleActuatorCommandResponse was called");
		if (this.enablePersistenceClient) {
			this.persistenceClient.storeData("", 0, data);
			_Logger.info("write the response to the local datastore");
		}

		if (data.hasError()) {
			_Logger.info("There is an error");
			return false;
		}
		return true;
	}

	/**
	 * use exception handling and the DataUtil class to attempt a conversion to ActuatorData or SystemStateData
	 * then pass data to handleIncomingDataAnalysis function
	 */
	@Override
	public boolean handleIncomingMessage(ResourceNameEnum resourceName, String msg)
	{
		_Logger.info("Handle incoming message..." + msg);
		ActuatorData actuatorData = null;
		SystemStateData sysData = null;
		try {
			actuatorData = dataUtil.jsonToActuatorData(msg);
			_Logger.info("Msg is an ActuatorData instance JSON");
		} catch (Exception e) {
			_Logger.info("Msg is NOT an ActuatorData instance JSON");
		}
		if(actuatorData != null) {
			handleIncomingDataAnalysis(resourceName, actuatorData);
			return true;
		}

		try {
			_Logger.info("Msg is a SystemStateData instance JSON");
			sysData = dataUtil.jsonToSystemStateData(msg);
		} catch (Exception e) {
			_Logger.info("Msg is NOT a SystemStateData instance JSON");
		}
		if(actuatorData == null && sysData == null) {
			_Logger.info("Invalid JSON data, please try again");
			return false;
		}
		handleIncomingDataAnalysis(resourceName, sysData);

		return true;
	}

	/**
	 * Check if the persistence client is active
	 * if so, perform logging and event tracking
	 * then convert the data to JSON
	 * pass JSON String to handleUpstreamTransmission
	 */
	@Override
	public boolean handleSensorMessage(ResourceNameEnum resourceName, SensorData data)
	{

		_Logger.info("Handling sensor message...");

		try {
			handleUpstreamTransmission(resourceName, data);

		}catch (Exception e) {

			return false;

		}
		if(enablePersistenceClient) {
			//TODO write the response to the local datastore (this is mostly for logging and event tracking purposes)
			_Logger.info("writing to the local datastore");
			this.persistenceClient.storeData("", 0, data);
		}


		if("HeartRateSensor".equals(data.getName())) {
			return handleHeartRateSensorData(resourceName, data);
		}




		return true;
	}

	/**
	 * Do humidity sensor data analysis
	 * send actuator command data back to CDA
	 * @param resourceName
	 * @param data
	 * @return
	 */
	public boolean handleHeartRateSensorData(ResourceNameEnum resourceName, SensorData data) {

		float heartRateFloor = 60;
		_Logger.info("Current heart rate is " + data.getValue());

		ActuatorData actuatorData = new ActuatorData();
		if(data.getValue() < heartRateFloor) {

			actuatorData.setActuatorType(ActuatorData.HEART_RATE_ACTUATOR_TYPE_DOWN);
			actuatorData.setCommand(ActuatorData.COMMAND_ON);
		}

		ActuatorData lastResponse = null;
		String lastActData = null;
		if(lastActData!=null) {
			lastResponse = dataUtil.jsonToActuatorData(lastActData);
		}

		String jsonActuator = dataUtil.actuatorDataToJson(actuatorData);
		if((lastResponse == null || lastResponse.getCommand() != actuatorData.getCommand())) {
			mqttClient.publishMessage(ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, jsonActuator, 1);
		}

		return true;
	}

	/**
	 * Do humidity sensor data analysis
	 * send actuator command data back to CDA
	 * @param resourceName
	 * @param data
	 * @return
	 */
	public boolean handleHumiditySensorData(ResourceNameEnum resourceName, SensorData data) {
		/*
		float humidityCeiling = 60;
		float humidityFloor = 40;
		_Logger.info("Current humidity is " + data.getValue());
		ActuatorData actuatorData = new ActuatorData();
		actuatorData.setActuatorType(ActuatorData.HUMIDIFIER_ACTUATOR_TYPE);

		if(data.getValue() < humidityFloor || data.getValue() > humidityCeiling) {
			actuatorData.setCommand(ActuatorData.COMMAND_ON);
		}else {
			actuatorData.setCommand(ActuatorData.COMMAND_OFF);
		}

		ActuatorData lastResponse = null;
		String lastActData = null;
		if(lastActData!=null) {
			lastResponse = dataUtil.jsonToActuatorData(lastActData);
		}

		String jsonActuator = dataUtil.actuatorDataToJson(actuatorData);
		if((lastResponse == null || lastResponse.getCommand() != actuatorData.getCommand()) && (data.getValue() < humidityFloor || data.getValue() > humidityCeiling)) {
			mqttClient.publishMessage(ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, jsonActuator, 1);
		}
		*/
		return true;
	}

	/**
	 * handle actuator data to manage led emulator
	 *
	 * @param resourceName
	 * @param
	 * @return
	 */
	public boolean handleLedActuatorData(ResourceNameEnum resourceName, String actuatorDataJson) {
		mqttClient.publishMessage(ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, actuatorDataJson, 1);
		return true;
	}

	/**
	 * Check if the persistence client is active
	 * if so, perform logging and event tracking
	 * then convert the data to JSON
	 * pass data to handleUpstreamTransmission
	 */
	@Override
	public boolean handleSystemPerformanceMessage(ResourceNameEnum resourceName, SystemPerformanceData data)
	{
		_Logger.info("Handling SystemPerformance Message..." + dataUtil.systemPerformanceDataToJson(data));
		//System.out.print(resourceName.toString());
		//store in local data store
		if(enablePersistenceClient) {
			try {
				_Logger.info("store system performance data : " + data);
				this.persistenceClient.storeData("", 0, data);
			}catch (Exception e) {
				return false;
			}
		}
		//send to cloud
		handleUpstreamTransmission(resourceName, data);

		return true;
	}

	/**
	 * start the manager
	 * Check the flag indicating whether or not the connections created during construction are enabled
	 */
	public void startManager()
	{
		_Logger.info("Started DeviceDataManager");

		if(enableMqttClient) {
			boolean mqttCode = mqttClient.connectClient();
		}
		if(enableCloudClient) {
			boolean cloudCode = cloudClient.connectClient();
			this.cloudClient.setDataMessageListener(this);
			this.cloudClient.mqttClient.setDataMessageListener(this);
			this.cloudClient.subscribeToEdgeEvents(ResourceNameEnum.CDA_UBIDOTS_BPD);
			this.cloudClient.subscribeToEdgeEvents(ResourceNameEnum.CDA_UBIDOTS_BT);

		}

		if(enablePersistenceClient) {
			boolean persisCode = persistenceClient.connectClient();
		}
		if(enableSmtpClient) {
			//TODO
		}
		if(enableCoapServer) {
			boolean coapCode = coapServer.startServer();
		}

		this.sysPerfManager.startManager();
	}

	/**
	 * stop the manager
	 * Check the flag indicating whether or not the connections created during construction are enabled
	 */
	public void stopManager()
	{
		_Logger.info("Stopped DeviceDataManager");

		if(enableMqttClient) {
			boolean mqttCode = mqttClient.disconnectClient();
		}
		if(enableCloudClient) {
			boolean cloudCode = cloudClient.disconnectClient();
		}

		if(enablePersistenceClient) {
			boolean persisCode = persistenceClient.disconnectClient();
		}
		if(enableSmtpClient) {
			//TODO
		}
		if(enableCoapServer) {
			boolean coapCode = coapServer.stopServer();
		}
		this.sysPerfManager.stopManager();

	}


	// private methods

	/**
	 * Initializes the enabled connections. This will NOT start them, but only create the
	 * instances that will be used in the {@link #startManager() and #stopManager()) methods.
	 * create the local class-scoped instances of each connection
	 */

	private void initConnections()
	{
		_Logger.info("init Connections... " );
		if(this.enableMqttClient) {

			mqttClient = new MqttClientConnector();
			mqttClient.setDataMessageListener(this);
		}

		if(this.enableCloudClient) {
			cloudClient = new CloudClientConnector();
			cloudClient.setDataMessageListener(this);

		}


		persistenceClient = new RedisPersistenceAdapter();
		smtpClient = new SmtpClientConnector();
		coapServer = new CoapServerGateway();

	}

	/**
	 * for cloud led action now
	 * @param resourceName
	 * @param data
	 */
	private void handleIncomingDataAnalysis(ResourceNameEnum resourceName, ActuatorData data){
		handleLedActuatorData(resourceName, dataUtil.actuatorDataToJson(data));
	}
	private void handleIncomingDataAnalysis(ResourceNameEnum resourceName, SystemStateData data){
		_Logger.info("HandleIncomingDataAnalysis...");
		/**
		 * Determine if a configured threshold crossing has been met by SensorData that should trigger an ActuatorData command to be published to the MQTT Broker on the CDA's ActuatorMsg topic.
		 * */

	}

	/**
	 * Send system performance data to cloud
	 * @param resourceName
	 * @param
	 */
	private void handleUpstreamTransmission(ResourceNameEnum resourceName, SystemPerformanceData data){
		_Logger.info("HandleUpstreamTransmission...");
		if ( this.enableCloudClient ) {
			this.cloudClient.sendEdgeDataToCloud(ResourceNameEnum.GDA_UBIDOTS_SYS, data);
			this.cloudClient.sendEdgeDataToCloud(ResourceNameEnum.CDA_UBIDOTS_SYS, data);
		}
	}

	private void handleUpstreamTransmission(ResourceNameEnum resourceName, SensorData data){

		_Logger.info("HandleUpstreamTransmission...");

		if ( this.enableCloudClient ) {

			this.cloudClient.sendEdgeDataToCloud(ResourceNameEnum.CDA_UBIDOTS, data);

		}
	}

}

/**
 * This class is part of the Programming the Internet of Things project.
 *
 * It is provided as a simple shell to guide the student and assist with
 * implementation for the Programming the Internet of Things exercises,
 * and designed to be modified by the student as needed.
 */

package programmingtheiot.gda.connection;

import java.util.Properties;
import java.util.logging.Level;
import java.util.logging.Logger;

import programmingtheiot.common.ConfigConst;
import programmingtheiot.common.ConfigUtil;
import programmingtheiot.common.IDataMessageListener;
import programmingtheiot.common.ResourceNameEnum;
import programmingtheiot.data.DataUtil;
import programmingtheiot.data.SensorData;
import programmingtheiot.data.SystemPerformanceData;

/**
 * Shell representation of class for student implementation.
 *
 */
public class CloudClientConnector implements ICloudClient
{
    // static

    private static final Logger _Logger =
            Logger.getLogger(CloudClientConnector.class.getName());

    // private var's

    private String topicPrefix = "";
    public MqttClientConnector mqttClient = null;
    private IDataMessageListener dataMsgListener = null;
    private int qosLevel = 1;
    // constructors

    /**
     * Default.
     *
     */
    public CloudClientConnector()
    {
        ConfigUtil configUtil = ConfigUtil.getInstance();

        this.topicPrefix =
                configUtil.getProperty(ConfigConst.CLOUD_GATEWAY_SERVICE, ConfigConst.BASE_TOPIC_KEY);

        // Depending on the cloud service, the topic names may or may not begin with a "/", so this code
        // should be updated according to the cloud service provider's topic naming conventions
        if (topicPrefix == null) {
            topicPrefix = "/";
        } else {
            if (! topicPrefix.endsWith("/")) {
                topicPrefix += "/";
            }
        }

    }


    // public methods

    @Override
    public boolean connectClient()
    {
        _Logger.info("Cloud Client connecting");
        if (this.mqttClient == null) {
            this.mqttClient = new MqttClientConnector(true);
        }

        return this.mqttClient.connectClient();
    }

    @Override
    public boolean disconnectClient()
    {
        _Logger.info("Cloud Client disconnecting");
        if(this.mqttClient == null)
            return false;

        return mqttClient.disconnectClient();

    }

    /**
     * check mqtt client connected or not
     * @return
     */
    public boolean isConnected()
    {
        return this.mqttClient.isConnected();
    }



    @Override
    public boolean setDataMessageListener(IDataMessageListener listener)
    {
        if(listener != null) {
            this.dataMsgListener = listener;

            return true;
        }
        return false;

    }

    /**
     * Mqtt client send system performance data to cloud
     */
    @Override
    public boolean sendEdgeDataToCloud(ResourceNameEnum resource, SensorData data) {
        // TODO Auto-generated method stub
        _Logger.info("Cloud Client send edge data to cloud");
        if (resource != null && data != null) {
            String payload = DataUtil.getInstance().sensorDataToJson(data);

            return publishMessageToCloud(resource, data.getName(), payload);
        }

        return false;
    }


    /**
     * Mqtt client send system performance data to cloud
     */
    @Override
    public boolean sendEdgeDataToCloud(ResourceNameEnum resource, SystemPerformanceData data) {
        // TODO Auto-generated method stub
        _Logger.info("Cloud Client send edge data to cloud");
        if (resource != null && data != null) {
            SensorData cpuData = new SensorData();
            cpuData.setName(ConfigConst.CPU_UTIL_NAME);
            cpuData.setValue(data.getCpuUtilization());

            boolean cpuDataSuccess = sendEdgeDataToCloud(resource, cpuData);

            if (! cpuDataSuccess) {
                _Logger.warning("Failed to send CPU utilization data to cloud service.");
            }

            SensorData memData = new SensorData();
            memData.setName(ConfigConst.MEM_UTIL_NAME);
            memData.setValue(data.getMemoryUtilization());

            boolean memDataSuccess = sendEdgeDataToCloud(resource, memData);

            if (! memDataSuccess) {
                _Logger.warning("Failed to send memory utilization data to cloud service.");
            }

            return (cpuDataSuccess == memDataSuccess);
        }
        return false;
    }


    /**
     * cloud mqtt client subscribe to a topic
     */
    @Override
    public boolean subscribeToEdgeEvents(ResourceNameEnum resource) {
        // TODO Auto -generated method stub
        _Logger.info("Cloud Client subscribe to edge events");
        boolean success = false;

        String topicName = null;

        if (isConnected()) {
            topicName = createTopicName(resource);
            _Logger.info("cloud subscribe to topic: " + topicName);
            this.mqttClient.subscribeToTopic(topicName, this.qosLevel);

            success = true;
        } else {
            _Logger.warning("Subscription methods only available for MQTT. No MQTT connection to broker. Ignoring. Topic: " + topicName);
        }

        return success;
    }




    /**
     * cloud mqtt client subscribe from a topic
     */
    @Override
    public boolean unsubscribeFromEdgeEvents(ResourceNameEnum resource) {
        // TODO Auto-generated method stub
        _Logger.info("Cloud Client unsubscribe from edge events");
        boolean success = false;

        String topicName = null;

        if (isConnected()) {
            topicName = createTopicName(resource);

            this.mqttClient.unsubscribeFromTopic(topicName);

            success = true;
        } else {
            _Logger.warning("Unsubscribe method only available for MQTT. No MQTT connection to broker. Ignoring. Topic: " + topicName);
        }

        return success;
    }


    // private methods
    private String createTopicName(ResourceNameEnum resource)
    {
        //return "";
        return this.topicPrefix + resource.getDeviceName();
    }

    /**
     * mqtt client publish message to cloud
     * @param resource
     * @param itemName
     * @param payload
     * @return
     */
    private boolean publishMessageToCloud(ResourceNameEnum resource, String itemName, String payload)
    {
        String topicName = createTopicName(resource) + "-" + itemName;

        try {
            _Logger.finest("Publishing payload value(s) to Ubidots: " + topicName);

            this.mqttClient.publishMessage(topicName, payload.getBytes(), this.qosLevel);

            return true;
        } catch (Exception e) {
            _Logger.warning("Failed to publish message to Ubidots: " + topicName);
        }

        return false;
    }

}

package programmingtheiot.part03.integration.connection;
import static org.junit.Assert.*;

import java.util.Set;
import java.util.logging.Logger;

import org.eclipse.californium.core.CoapClient;
import org.eclipse.californium.core.WebLink;
import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

import programmingtheiot.common.ConfigConst;
import programmingtheiot.common.ConfigUtil;
import programmingtheiot.common.DefaultDataMessageListener;
import programmingtheiot.common.IDataMessageListener;
import programmingtheiot.common.ResourceNameEnum;
import programmingtheiot.data.DataUtil;
import programmingtheiot.data.SensorData;
import programmingtheiot.data.SystemStateData;
import programmingtheiot.gda.connection.*;

public class CoapClientPerformanceTest {
    public static final int MAX_TEST_RUNS = 10000;
    private static final int DEFAULT_TIMEOUT = 120000;

    private CoapClientConnector coapClient = null;
    private static final Logger _Logger =
            Logger.getLogger(CoapClientToServerConnectorTest.class.getName());

    @Before
    public void setUp() throws Exception
    {
        this.coapClient = new CoapClientConnector();
    }
    /**
     * Test method for running the con.
     */
    @Test
    public void testPostRequestCon()
    {
        execTestPost(MAX_TEST_RUNS, true);
    }
    /**
     * Test method for running the non.
     */
    @Test
    public void testPostRequestNon()
    {
        execTestPost(MAX_TEST_RUNS, false);
    }

    private void execTestPost(int maxTestRuns, boolean enableCON)
    {
        SensorData sd = new SensorData();
        String payload = DataUtil.getInstance().sensorDataToJson(sd);

        long startMillis = System.currentTimeMillis();

        for (int seqNo = 0; seqNo < maxTestRuns; seqNo++) {
            this.coapClient.sendPostRequest(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, enableCON, payload, DEFAULT_TIMEOUT);
        }

        long endMillis = System.currentTimeMillis();
        long elapsedMillis = endMillis - startMillis;

        _Logger.info("POST message - useCON " + enableCON + " [" + maxTestRuns + "]: " + elapsedMillis + " ms");
    }
}

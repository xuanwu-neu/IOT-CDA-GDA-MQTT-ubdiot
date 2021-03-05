/**
 * 
 * This class is part of the Programming the Internet of Things
 * project, and is available via the MIT License, which can be
 * found in the LICENSE file at the top level of this repository.
 * 
 * Copyright (c) 2020 by Andrew D. King
 */ 

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

/**
 * This test case class contains very basic integration tests for
 * CoapClientToServerConnectorTest. It should not be considered complete,
 * but serve as a starting point for the student implementing
 * additional functionality within their Programming the IoT
 * environment.
 *
 */
public class CoapClientToServerConnectorTest
{
	// static
	public static final int MAX_TEST_RUNS = 10000;
	public static final int DEFAULT_TIMEOUT = 120000;
	public static final boolean USE_DEFAULT_RESOURCES = true;
	
	private static final Logger _Logger =
		Logger.getLogger(CoapClientToServerConnectorTest.class.getName());
	
	private static CoapServerGateway _Csg = null;
	
	// member var's
	private CoapClientConnector coapClient = null;
	
	private CoapClientConnector ccc = null;
	private IDataMessageListener dml = null;
	
	
	// test setup methods
	
	/**
	 * @throws java.lang.Exception
	 */
	@BeforeClass
	public static void setUpBeforeClass() throws Exception
	{
		_Csg = new CoapServerGateway(USE_DEFAULT_RESOURCES);

		assertTrue(_Csg.startServer());
	}
	
	/**
	 * @throws java.lang.Exception
	 */
	@AfterClass
	public static void tearDownAfterClass() throws Exception
	{
		assertTrue(_Csg.stopServer());
	}
	
	/**
	 * @throws java.lang.Exception
	 */
	@Before
	public void setUp() throws Exception
	{
		this.ccc = new CoapClientConnector();
		this.dml = new DefaultDataMessageListener();
		
		this.ccc.setDataMessageListener(this.dml);
		this.coapClient = new CoapClientConnector();
	}
	
	/**
	 * @throws java.lang.Exception
	 */
	@After
	public void tearDown() throws Exception
	{
	}
	
	// test methods
	
	/**
	 *  testGetRequestCon and testGetRequestNon
	 */

	@Test
	public void testGetRequestCon()
	{
		assertTrue(this.ccc.sendGetRequest(ResourceNameEnum.GDA_MGMT_STATUS_MSG_RESOURCE, true, DEFAULT_TIMEOUT));
	}

	@Test
	public void testGetRequestNon()
	{
		assertTrue(this.ccc.sendGetRequest(ResourceNameEnum.GDA_MGMT_STATUS_MSG_RESOURCE, false, DEFAULT_TIMEOUT));
	}
	
	/**
	 * testPostRequestCon
	 */
	@Test
	public void testPostRequestCon()
	{
		int actionCmd = 2;

		SystemStateData ssd = new SystemStateData();
		ssd.setActionCommand(actionCmd);

		String ssdJson = DataUtil.getInstance().systemStateDataToJson(ssd);
		assertTrue(this.ccc.sendPostRequest(ResourceNameEnum.GDA_MGMT_STATUS_MSG_RESOURCE, true, ssdJson, DEFAULT_TIMEOUT));
	}
	/**
	 * testPostRequestNon
	 */
	@Test
	public void testPostRequestNon()
	{
		int actionCmd = 2;

		SystemStateData ssd = new SystemStateData();
		ssd.setActionCommand(actionCmd);

		String ssdJson = DataUtil.getInstance().systemStateDataToJson(ssd);
		assertTrue(this.ccc.sendPostRequest(ResourceNameEnum.GDA_MGMT_STATUS_MSG_RESOURCE, false, ssdJson, DEFAULT_TIMEOUT));
	}
	
	/**
	 * testPutRequestCon
	 */

	@Test
	public void testPutRequestCon()
	{
		int actionCmd = 2;

		SystemStateData ssd = new SystemStateData();
		ssd.setActionCommand(actionCmd);

		String ssdJson = DataUtil.getInstance().systemStateDataToJson(ssd);
		assertTrue(this.ccc.sendPutRequest(ResourceNameEnum.GDA_MGMT_STATUS_MSG_RESOURCE, true, ssdJson, DEFAULT_TIMEOUT));
	}
	/**
	 * testPutRequestCon
	 */
	@Test
	public void testPutRequestNon()
	{
		int actionCmd = 2;

		SystemStateData ssd = new SystemStateData();
		ssd.setActionCommand(actionCmd);

		String ssdJson = DataUtil.getInstance().systemStateDataToJson(ssd);
		assertTrue(this.ccc.sendPutRequest(ResourceNameEnum.GDA_MGMT_STATUS_MSG_RESOURCE, false, ssdJson, DEFAULT_TIMEOUT));
	}
	
	/**
	 * testDeleteRequestCon and testDeleteRequestNon
	 */
	@Test
	public void testDeleteRequestCon()
	{
		assertTrue(this.ccc.sendDeleteRequest(ResourceNameEnum.GDA_MGMT_STATUS_MSG_RESOURCE, true, DEFAULT_TIMEOUT));
	}

	@Test
	public void testDeleteRequestNon()
	{
		assertTrue(this.ccc.sendDeleteRequest(ResourceNameEnum.GDA_MGMT_STATUS_MSG_RESOURCE, false, DEFAULT_TIMEOUT));
	}

	@Test
	public void testConnectAndDiscover()
	{
		assertTrue(this.ccc.sendDiscoveryRequest(DEFAULT_TIMEOUT));

		// NOTE: If you are using a custom asynchronous discovery, include a brief wait here
		try {
			Thread.sleep(2000L);
		} catch (InterruptedException e) {
			// ignore
		}
	}

	@Test
	public void testPostRequestCon1()
	{
		execTestPost(MAX_TEST_RUNS, true);
	}

	@Test
	public void testPostRequestNon1()
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

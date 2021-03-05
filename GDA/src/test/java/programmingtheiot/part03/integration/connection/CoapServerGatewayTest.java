package programmingtheiot.part03.integration.connection;
import static org.junit.Assert.*;

import java.util.Set;
import java.util.logging.Logger;

import org.eclipse.californium.core.CoapClient;
import org.eclipse.californium.core.WebLink;

import org.junit.*;


import programmingtheiot.common.DefaultDataMessageListener;
import programmingtheiot.common.IDataMessageListener;
import programmingtheiot.gda.connection.*;
public class CoapServerGatewayTest {
    public static final int DEFAULT_TIMEOUT = 120000;


    private static final Logger _Logger =
            Logger.getLogger(CoapClientToServerConnectorTest.class.getName());

    private static CoapServerGateway _Csg = null;

    /**
     * testRunSimpleCoapServerGatewayIntegration for the CoapClientConnector
     */
    @Test
    public void testRunSimpleCoapServerGatewayIntegration()
    {
        try {
            String url = "coap://localhost:5683";

            this._Csg = new CoapServerGateway();
            this._Csg.startServer();

            CoapClient clientConn = new CoapClient(url);

            Set<WebLink> wlSet = clientConn.discover();

            if (wlSet != null) {
                for (WebLink wl : wlSet) {
                    _Logger.info(" --> WebLink: " + wl.getURI() + ". Attributes: " + wl.getAttributes());
                }
            }

            Thread.sleep(DEFAULT_TIMEOUT); // DEFAULT_TIMEOUT is in milliseconds - for instance, 120000 (2 minutes)

            this._Csg.stopServer();
        } catch (Exception e) {
            // log a message!
            _Logger.info("There is an error!");
        }
    }
}

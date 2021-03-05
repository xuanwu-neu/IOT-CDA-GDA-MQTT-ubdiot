package programmingtheiot.gda.connection.handlers;

import java.util.logging.Logger;

import org.eclipse.californium.core.CoapHandler;
import org.eclipse.californium.core.CoapResource;
import org.eclipse.californium.core.CoapResponse;
import org.eclipse.californium.core.coap.OptionSet;

import programmingtheiot.common.IDataMessageListener;
import programmingtheiot.common.ResourceNameEnum;


public class GenericCoapResponseHandler implements CoapHandler {
    // static

    private static final Logger _Logger =
            Logger.getLogger(GenericCoapResourceHandler.class.getName());

    // params
    private IDataMessageListener dataMsgListener;

    // constructors

    public GenericCoapResponseHandler(IDataMessageListener listener)
    {
        this.dataMsgListener = listener;
    }





    // public methods
    @Override
    public void onLoad(CoapResponse response)
    {
        if (response != null) {
            OptionSet options = response.getOptions();

            _Logger.info("Processing CoAP response. Options: " + options);
            _Logger.info("Processing CoAP response. MID: " + response.advanced().getMID());
            _Logger.info("Processing CoAP response. Token: " + response.advanced().getTokenString());
            _Logger.info("Processing CoAP response. Code: " + response.getCode());

            // TODO: parse payload and notify listener
            _Logger.info(" --> Payload: " + response.getResponseText());

            if (this.dataMsgListener != null) {
                // TODO: send listener the response
            }
        } else {
            _Logger.warning("No CoAP response to process. Response is null.");
        }
    }

    @Override
    public void onError()
    {
        _Logger.warning("Error processing CoAP response. Ignoring.");
    }
}

/**
 * This class is part of the Programming the Internet of Things project.
 * 
 * It is provided as a simple shell to guide the student and assist with
 * implementation for the Programming the Internet of Things exercises,
 * and designed to be modified by the student as needed.
 */ 

package programmingtheiot.data;

import java.io.Serializable;
import java.text.SimpleDateFormat;
import java.util.Date;

import programmingtheiot.common.ConfigConst;

/**
 * Shell representation of class for student implementation.
 *
 */
public abstract class BaseIotData implements Serializable
{
	// static
	
	public static final float DEFAULT_VAL = 0.0f;
	public static final int DEFAULT_STATUS = 0;
	
	// private var's

    private String  name       = ConfigConst.NOT_SET;
	private String  timeStamp  = null;
    private boolean hasError   = false;
    private int     statusCode = 0;
    
    private long    timeStampMillis = 0L;
	private String stateData = "";
    
	// constructors
	
	/**
	 * Default.
	 * 
	 */
	protected BaseIotData()
	{
		super();
	}
	
	
	// public methods
	
	public String getName()
	{
		return name;
	}
	
	public String getStateData()
	{
		return stateData;
	}
	
	public int getStatusCode()
	{
		return statusCode;
	}
	
	public String getTimeStamp()
	{
		return timeStamp;
	}
	
	public long getTimeStampMillis()
	{
		return timeStampMillis;
	}
	
	public boolean hasError()
	{
		return hasError;
	}
	
	public void setName(String name)
	{
		this.name = name;
	}
	
	public void setStateData(String data)
	{
		this.stateData = data;
	}
	
	public void setStatusCode(int code)
	{
		this.statusCode = code;
	}
	
	public void updateData(BaseIotData data)
	{
		// TODO: update local var's
		this.name = data.getName();
		this.statusCode = data.getStatusCode();
		this.hasError = data.hasError();
		this.timeStamp = data.getTimeStamp();
		this.stateData = data.getStateData();
		handleUpdateData(data);
	}
	
	
	// protected methods
	
	/*
	 * Template method to handle data update for the sub-class.
	 * 
	 * @param BaseIotData While the parameter must implement this method,
	 * the sub-class is expected to cast the base class to its given type.
	 */
	protected abstract void handleUpdateData(BaseIotData data);
	
}

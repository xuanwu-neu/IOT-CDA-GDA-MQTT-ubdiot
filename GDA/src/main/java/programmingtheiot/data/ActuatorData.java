/**
 * This class is part of the Programming the Internet of Things project.
 * 
 * It is provided as a simple shell to guide the student and assist with
 * implementation for the Programming the Internet of Things exercises,
 * and designed to be modified by the student as needed.
 */ 

package programmingtheiot.data;

import java.io.Serializable;

/**
 * Shell representation of class for student implementation.
 *
 */
public class ActuatorData extends BaseIotData implements Serializable
{
	// static
	
	public static final int DEFAULT_COMMAND = 0;
	public static final int COMMAND_OFF = DEFAULT_COMMAND;
	public static final int COMMAND_ON = 1;
	public static final int DEFAULT_ACTUATOR_TYPE = 0;

	public static final int BODY_TEMP_ACTUATOR_TYPE_UP = 1;
	public static final int BODY_TEMP_ACTUATOR_TYPE_DOWN = 2;
	public static final int BLOOD_PRESSURE_ACTUATOR_TYPE_UP = 3;
	public static final int BLOOD_PRESSURE_ACTUATOR_TYPE_DOWN = 4;
	public static final int HEART_RATE_ACTUATOR_TYPE_UP = 5;
	public static final int HEART_RATE_ACTUATOR_TYPE_DOWN = 6;
	
	// private var's
	
    private float value;
    private int command;
    private int actuatorType;

	// constructors
	
	/**
	 * Default.
	 * 
	 */
	public ActuatorData()
	{

		super();
		command = ActuatorData.DEFAULT_COMMAND;
		value = ActuatorData.DEFAULT_VAL;
		actuatorType = ActuatorData.DEFAULT_ACTUATOR_TYPE;
	}


	public void updateData(ActuatorData data)
	{
		// TODO: update local var's
		super.updateData(data);
		this.command = data.command;
		this.value = data.value;
        this.actuatorType = data.actuatorType;
	}



	// public methods
	
	public int getCommand() {
		return command;
	}
	
	public float getValue() {
		return value;
	}
	
	public void setCommand(int command) {
		this.command = command;
	}
	
	public void setValue(float val) {
		value = val;
	}

	public void setActuatorType(int actuatortype) {
		this.actuatorType = actuatortype;
	}
	public int getActuatorType() {
		return this.actuatorType;
	}
	
	// protected methods
	
	/* (non-Javadoc)
	 * @see programmingtheiot.data.BaseIotData#handleUpdateData(programmingtheiot.data.BaseIotData)
	 */
	protected void handleUpdateData(BaseIotData data) {

	}
	
}

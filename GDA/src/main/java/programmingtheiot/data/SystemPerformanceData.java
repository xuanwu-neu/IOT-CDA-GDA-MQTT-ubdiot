/**
 * This class is part of the Programming the Internet of Things project.
 * 
 * It is provided as a simple shell to guide the student and assist with
 * implementation for the Programming the Internet of Things exercises,
 * and designed to be modified by the student as needed.
 */ 

package programmingtheiot.data;

import programmingtheiot.common.ConfigConst;

import java.io.Serializable;

/**
 * Shell representation of class for student implementation.
 *
 */
public class SystemPerformanceData extends BaseIotData implements Serializable
{
	// static
	
	
	// private var's
	private float CpuUtilization = 0;
	private float DiskUtilization = 0;
	private float MemoryUtilization = 0;
    
	// constructors
	
	public SystemPerformanceData()
	{
		super();
		super.setName(ConfigConst.SYS_PERF_DATA);
	}
	
	
	// public methods
	public void updateData(SystemPerformanceData data)
	{
		// TODO: update local var's
		super.updateData(data);
		this.CpuUtilization = data.CpuUtilization;
		this.DiskUtilization = data.DiskUtilization;
		this.MemoryUtilization = data.MemoryUtilization;
	}
	
	public float getCpuUtilization() {

		return CpuUtilization;
	}
	
	public float getDiskUtilization() {

		return DiskUtilization;
	}
	
	public float getMemoryUtilization() {

		return MemoryUtilization;
	}
	
	public void setCpuUtilization(float val) {
		CpuUtilization = val;
	}
	
	public void setDiskUtilization(float val) {
		DiskUtilization = val;
	}
	
	public void setMemoryUtilization(float val) {
		MemoryUtilization = val;
	}
	
	
	// protected methods
	
	/* (non-Javadoc)
	 * @see programmingtheiot.data.BaseIotData#handleToString()
	 */
	protected String handleToString()
	{
		return null;
	}
	
	/* (non-Javadoc)
	 * @see programmingtheiot.data.BaseIotData#handleUpdateData(programmingtheiot.data.BaseIotData)
	 */
	protected void handleUpdateData(BaseIotData data)
	{
	}
	
}

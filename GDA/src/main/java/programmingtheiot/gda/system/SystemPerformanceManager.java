/**
 * This class is part of the Programming the Internet of Things project.
 *
 * It is provided as a simple shell to guide the student and assist with
 * implementation for the Programming the Internet of Things exercises,
 * and designed to be modified by the student as needed.
 */

package programmingtheiot.gda.system;

import java.util.logging.Level;




import java.util.logging.Logger;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;

import programmingtheiot.common.ConfigConst;
import programmingtheiot.common.IDataMessageListener;
import programmingtheiot.common.ResourceNameEnum;
import programmingtheiot.data.SystemPerformanceData;
import programmingtheiot.gda.app.GatewayDeviceApp;

/**
 * Shell representation of class for student implementation.
 *
 */
public class SystemPerformanceManager
{
	// static
	private int pollSecs = 30;
	private static final Logger _Logger =
			Logger.getLogger(SystemPerformanceManager.class.getName());

	private ScheduledExecutorService schedExecSvc = null;
	private SystemCpuUtilTask cpuUtilTask = null;
	private SystemMemUtilTask memUtilTask = null;

	private Runnable taskRunner = null;
	private boolean isStarted = false;
	private IDataMessageListener dataMsgListener = null;

	// constructors

	/**
	 * Default.
	 *
	 */
	public SystemPerformanceManager()
	{
		this(ConfigConst.DEFAULT_POLL_CYCLES);
	}

	/**
	 * Constructor.
	 *
	 * @param pollSecs The number of seconds between each scheduled task poll.
	 */
	public SystemPerformanceManager(int pollSecs)
	{
		if(pollSecs > 1 && pollSecs < Integer.MAX_VALUE) {
			this.pollSecs = pollSecs;
		}
		this.schedExecSvc = Executors.newScheduledThreadPool(2);
		this.cpuUtilTask = new SystemCpuUtilTask();
		this.memUtilTask = new SystemMemUtilTask();


	}


	// public methods

	public void handleTelemetry()
	{
		//float cpuUtilPct = this.cpuUtilTask.getTelemetryValue();
		//float memUtilPct = this.memUtilTask.getTelemetryValue();
		float cpuUtilPct = this.cpuUtilTask.getSystemUtil();
		float memUtilPct = this.memUtilTask.getSystemUtil();
		_Logger.info("cpuUtilPct = "+cpuUtilPct + " memUtilPct = "+memUtilPct);
		SystemPerformanceData sysData = new SystemPerformanceData();
		sysData.setCpuUtilization(cpuUtilPct);
		sysData.setMemoryUtilization(memUtilPct);

		if(this.dataMsgListener != null) {
			dataMsgListener.handleSystemPerformanceMessage(ResourceNameEnum.GDA_UBIDOTS_SYS, sysData);
		}
	}


	public void setDataMessageListener(IDataMessageListener listener)
	{

		this.dataMsgListener = listener;
	}

	public void startManager()
	{
		_Logger.info("Starting system manager...");

		this.taskRunner = () -> {
			this.handleTelemetry();
		};

		if (! this.isStarted) {
			ScheduledFuture<?> futureTask = this.schedExecSvc.scheduleAtFixedRate(this.taskRunner, 0L, this.pollSecs, TimeUnit.SECONDS);

			this.isStarted = true;
		}
	}

	public void stopManager()
	{
		_Logger.info("Stopping system manager...");
		this.schedExecSvc.shutdown();
	}

}
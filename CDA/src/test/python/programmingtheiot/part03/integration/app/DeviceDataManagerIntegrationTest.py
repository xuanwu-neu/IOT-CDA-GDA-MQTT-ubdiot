import logging
import unittest

from time import sleep

from src.main.python.programmingtheiot.cda.app.DeviceDataManager import DeviceDataManager


class DeviceDataManagerIntegrationTest(unittest.TestCase):
    """
    This test case class contains very basic integration tests for
    DeviceDataManager. It should not be considered complete,
    but serve as a starting point for the student implementing
    additional functionality within their Programming the IoT
    environment.

    NOTE: This test MAY require the sense_emu_gui to be running,
    depending on whether or not the 'enableEmulator' flag is
    True within the ConstraineDevice section of PiotConfig.props.
    If so, it must have access to the underlying libraries that
    support the pisense module. On Windows, one way to do
    this is by installing pisense and sense-emu within the
    Bash on Ubuntu on Windows environment and then execute this
    test case from the command line, as it will likely fail
    if run within an IDE in native Windows.

    """

    def testDeviceDataManagerIntegration(self):
        # TODO: set either MQTT or CoAP to True - you'll only need one.
        ddMgr = DeviceDataManager(enableMqtt=True, enableCoap=False)

        ddMgr.startManager()

        # 5 min's should be long enough to run the tests and manually adjust the emulator values
        sleep(300)

        ddMgr.stopManager()


if __name__ == "__main__":
    unittest.main()

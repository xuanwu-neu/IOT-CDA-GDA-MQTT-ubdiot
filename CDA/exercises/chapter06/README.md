# Constrained Device Application (Connected Devices)

## Lab Module 06

Be sure to implement all the PIOT-CDA-* issues (requirements) listed at [PIOT-INF-06-001 - Chapter 06](https://github.com/orgs/programming-the-iot/projects/1#column-10488434).

### Description

NOTE: Include two full paragraphs describing your implementation approach by answering the questions listed below.

What does your implementation do? 

Implemented mqttClientConnector, add functionality to Devicedatamanager implementation.

How does your implementation work?

All test passed as same as example.


### Code Repository and Branch

NOTE: Be sure to include the branch (e.g. https://github.com/programming-the-iot/python-components/tree/alpha001).

URL: https://github.com/NU-CSYE6530-Fall2020/constrained-device-app-xuanwu-neu/tree/chapter06

### UML Design Diagram(s)

NOTE: Include one or more UML designs representing your solution. It's expected each
diagram you provide will look similar to, but not the same as, its counterpart in the
book [Programming the IoT](https://learning.oreilly.com/library/view/programming-the-internet/9781492081401/).

![image](./chapter06.svg)

### Unit Tests Executed

NOTE: TA's will execute your unit tests. You only need to list each test case below
(e.g. ConfigUtilTest, DataUtilTest, etc). Be sure to include all previous tests, too,
since you need to ensure you haven't introduced regressions.

- ./src/test/python/programmingtheiot/part02/unit/data/DataUtilTest
- ./src/test/python/programmingtheiot/part01/unit/system/SystemCpuUtilTaskTest
- ./src/test/python/programmingtheiot/part01/unit/system/SystemMemUtilTaskTest

### Integration Tests Executed

NOTE: TA's will execute most of your integration tests using their own environment, with
some exceptions (such as your cloud connectivity tests). In such cases, they'll review
your code to ensure it's correct. As for the tests you execute, you only need to list each
test case below (e.g. SensorSimAdapterManagerTest, DeviceDataManagerTest, etc.)

- ./src/test/python/programmingtheiot/part03/connection/MqttClientConnectorTest
- 
- 

### 14 different Mqtt Control packet output

![image](./Connect-ACK.png)

![image](./Connect-command.png)

![image](./disconnected.png)

![image](./ping-request.png)

![image](./Ping-Response.png)

![image](./publish-ack.png)

![image](./publish-complete.png)

![image](./publish-message.png)

![image](./publish-received.png)

![image](./publish-release.png)

![image](./subscribe-ack.png)

![image](./unsubscribe-ask.png)

![image](./subscribe-request.png)

![image](./Unsubscribe-request.png)


EOF.

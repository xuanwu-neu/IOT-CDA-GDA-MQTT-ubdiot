# Gateway Device Application (Connected Devices)

## Lab Module 10

Be sure to implement all the PIOT-GDA-* issues (requirements) listed at [PIOT-INF-10-001 - Chapter 10](https://github.com/orgs/programming-the-iot/projects/1#column-10488510).

### Description

NOTE: Include two full paragraphs describing your implementation approach by answering the questions listed below.

What does your implementation do? 

Implemented Coap and Mqtt integration

How does your implementation work?

All test passed as same as example.

### Code Repository and Branch

NOTE: Be sure to include the branch (e.g. https://github.com/programming-the-iot/python-components/tree/alpha001).

URL: https://github.com/NU-CSYE6530-Fall2020/gateway-device-app-xuanwu-neu/tree/chapter10

### UML Design Diagram(s)

NOTE: Include one or more UML designs representing your solution. It's expected each
diagram you provide will look similar to, but not the same as, its counterpart in the
book [Programming the IoT](https://learning.oreilly.com/library/view/programming-the-internet/9781492081401/).

![image](./chapter10.svg)

### Unit Tests Executed

NOTE: TA's will execute your unit tests. You only need to list each test case below
(e.g. ConfigUtilTest, DataUtilTest, etc). Be sure to include all previous tests, too,
since you need to ensure you haven't introduced regressions.

- src/test/java/programmingtheiot/part02/unit/data
-
-

### Integration Tests Executed

NOTE: TA's will execute most of your integration tests using their own environment, with
some exceptions (such as your cloud connectivity tests). In such cases, they'll review
your code to ensure it's correct. As for the tests you execute, you only need to list each
test case below (e.g. SensorSimAdapterManagerTest, DeviceDataManagerTest, etc.)

- src/test/java/programmingtheiot/part03/integration/connection/MqttClientPerformanceTest.java
- src/test/java/programmingtheiot/part03/integration/connection/CoapClientPerformanceTest.java
- src/test/java/programmingtheiot/part02/integration/data

INFO: Publish message - QoS 0 [10000]: 2065 ms
INFO: Publish message - QoS 1 [10000]: 2378 ms
INFO: Publish message - QoS 2 [10000]: 2830 ms
QoS 0 fast and QoS 2 slow

INFO: POST message - useCON true [10000]: 3744 ms
INFO: POST message - useCON false [10000]: 2633 ms
CON slow and NON fast

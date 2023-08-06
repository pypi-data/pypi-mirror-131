To-do's
=========

Functions to add
----------------------

DeviceService
^^^^^^^^^^^^^^
The feature DeviceProvider should be renamed to DeviceServicer()

Node
^^^^^^
The user should be able to define the device node in the DeviceServicer feature. If a new SiLA server is started, the
user can use the SetNode() and GetNode() command to change the node.

Protocol
^^^^^^^^^^
The user should be able to define the used communication protocol. This is either defined on startup or changed during
runtime. A GetCommunicationProtocol() and a SetCommunicationProtocol() function should be added to the DeviceServicer.

Com-Port
^^^^^^^^^^
The user should be able to define the devices serial port. This is either defined on stratup or changed during runtime.
A GetCommunicationPort() and a SetCommunicationPort() function should be added to the  DeviceServicer.


General
---------
- Update all Responses in the FDL-files.
- Implement all simulation responses adequately (With realistic returns)

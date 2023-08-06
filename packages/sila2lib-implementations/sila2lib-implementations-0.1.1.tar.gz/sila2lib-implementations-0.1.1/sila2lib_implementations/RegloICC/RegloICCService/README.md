****This repository contains the SiLA2 driver for the REGLO ICC peristaltic pump. This SiLA2 driver is based on Python 3.7.4+.****


Getting Started
======

>This SiLA2 driver was developed and tested on Beaglebone Green under Debian 9.I5 Stretcher IoT. 

Install required dependencies
-------
The SiLA2 driver in this repository needs the following packages to work correctly if installed under Debian:
*  Cython 0.29.13
*  grpcio 1.23.0
*  grpcio-tools 1.23.0
*  ifaddr 0.1.6
*  lxml 4.3.3
*  pip 9.0.1        (pip versions >9.0.1 were not working properly on Debian 9.5)
*  protobuf 3.9.1
*  pyserial 3.4
*  setuptools 41.2.0
*  sila2lib 0.1.6
*  smart-template 0.1.1
*  wheel 0.33.6
*  zeroconf 0.23.0

SiLA2 Python Library installation
-------
>SiLA Python needs Python 3.6 or greater to run properly.
>See https://gitlab.com/SiLA2/sila_python for more information on this.

Installing the SiLA 2 Python library is now as simple as running
`$ pip3 install sila2lib`
or executing
`$ pip3 install .` from the sila_library folder 

SiLA2 Python code generator installation
--------
In order to build the driver from scratch, you need the SiLA 2 Python code generator (skip this part if you only want to use the driver).
Install the code generator by executing `$ pip3 install sila2codegenerator` or running
`$ pip3 install .` from the sila_tools/sila2codegenerator folder 

Generating the driver
----------
>See https://gitlab.com/SiLA2/sila_python/tree/master/sila_tools/sila2codegenerator for more informatioin

After using the XML template files for feature specification, you can build the driver with the code generator by executing

`$silacodegenerator --build <path/to/project/dir>` with <path/to/project/dir the path to the directory with XML files

Running the pump
======

Available SiLA commands
----------
The RegloICCPumpFeatures.docx file provides an overview of implemented pump commands. Those are grouped into 5 features: 

*   *SystemServicer feature* for commands that define system settings,
*	*DriveControlServicer* for operating the pump drive, such as start/stop commands,
*	*ParameterControlServicer* for setting operational modes and parameters,
*	*CalibrationServicer* for all services related to calibration, and
*	*ConfigurationServicer*, where pump variable configurations, e.g. tubing inside diameter, are set.

Starting the server
----------
>>>
Note:

The pump was connected via USB to the Beaglebone Green with a single USB port. Therefore, automatic port determination executes search to available /dev/ttyUSB**x** designation and accepts it as the currently used port
>>>

The server is started by executing `$ python3 PumpService_server.py` from the *PumpService* folder. 

The server must run during all operations with the pump

Pump integration - Methods
----------

The script *Classes.py* provides established sequences and loops of *Get* and *Set* commands that would enable flexible operation for each of the pump channels. Four methods are defined:
*   *PumpSetVolumeAtFlowRate* : allows dispensing a set volume (input in mL) with a set flow rate (mL/min), rotation direction (J for clockwise, K for counter-clockwise rotation, the letters specified by the pump manufacturer) for specific channel or channels
*   *PumpTimeAtFlowRate* : method to dispense for a set time duration (in seconds) with a set flow rate (mL/min), rotation direction (J or K) for specific channel or channels
*   *PumpStop*: method to stop the channels
*   *PumpStatus* : method to check whether the pump is currently running (+) or not (-)

The pump address is preset to 1, which corresponds to the current address of the used pump, therefore no further input is required. 
The return value of the function is cleared every time the function is called. 
The preset parameters for channels in use and volume/time to pump serve as a demonstration and should be altered according to user requirements.
The rotation direction used for the transfer is preset to counter-clockwise.

All inputs must be made in a list in a string format. The reason for it is the feature definition in XML files, in which the set parameters and pump responses were defined as strings for reasons of uniformity and to avoid multiple format conversions. 
The only exceptions are internal pump state commands *SystemServicer_SetChannelAddressing* and *SystemServicer_SetEventMessages* that are boolean. 
The numeric inputs may have a maximum of two decimal places with an exception of time, which allows only one decimal place. 
The non-compliant input will be formatted automatically. 

If several channels are used, there must be the same number of values in each other parameter, except for pump address and return value that should not be changed. 
If the function is called with no specified input, default values that are set in function in *Classes.py* are used. 
There is no exact preset for flowrale. Tf not set otherwise, the maximum flow rate is used.

Pump integration - *Predispense.py*
----------
*Predispense.py* is an actual application of the [methods](#pump-integration---methods) described above.

Running `$ python3 Predispense.py` from the *PumpService* folder allows pumping of a set volume.

For example,
```
import Classes as classes

p = classes.Pump() 
p.PumpSetVolumeAtFlowRate(channels=['1'], flowrate=['27'], volume=['97.8'], rotation=['K'])
```
executes *PumpSetVolumeAtFlowRate* [method](#pump-integration---methods) for Channel 1 at flowrate of 27 mL/min, pumping 97.8 mL with counter-clockwise rotation direction.


Pump integration - *Robot.py*
----------

Execution of `$ python3 Robot.py` from the *PumpService* folder allows pumping of liquid that is synchronized with the feedback from another device connected via serail connection.

Miltithreading is used for synchronization. The daemon thread, which operates in the background, constantly attempts to receive a message from another device. As soon as the message arrives, it is classified (*"Done"* or *other*) and passed into a corresponding queue
The volume to refill after the message is received is set to 8 mL. If the dispensed volume is changed, the value in the script must be updated. 

The main thread consists of a loop that constantly checks if anything has been added to the queues. As soon as a numeric object is put into volume queue, the volume to pump is increased by that number. The queue is thereby cleared in order to allow the daemon thread further operations with it. 
After the volume parameter has been increased to a number greater than 0, the thread examines whether the pump is currently in motion. If it is not running, then a method to pump set volume is started. The volume parameter is cleared afterwards. 
While the parameters *channels* and *rotation*  are strictly specified in a list for a single input, the input of *volume* is variable, depending on feedback and feedback frequency from the pipetting robot, and time. 
Since the intern parameter used in the queue is of integer format, it is converted into a string, which is required by the defined SiLA~2 command specification for a consistent input format.
As the flow rate is not specified by the user, the maximum calibrated flow rate of the channel will be applied.

When the stop queue has been filled by the daemon thread after receiving a *"Done*" message, two options are possible. 
The first one, when the pump is still execution filling, results in a delay until the queued volume is transmitted and cleared and the refill operation is finished. 
This option can be deleted if the refilled contents are not further used, since the *"Done"* message indicates that the robot has finished the distribution of the liquid into reactors.
The second option occurs when the pump has finished all planned dispensing. Then the channel is stopped (terminal output is generated) and the program is terminated. 

Therminal output
----------

The terminal output of the running server provides information on the serial port, server metadata, and available features. It is also possible to check, whether the desired *real* operation mode (= actual execution instead of *simulation mode* = code functionality tests) is used for all features. Furthermore, the output provides feedback for internal command execution that uses *logging.debug* function.

The terminal output of the executed *Predispense.py* and *Robot.py* summarizes set parameters and executed commands. For further information regarding executed command sequences, the terminal output of the running server can be used.

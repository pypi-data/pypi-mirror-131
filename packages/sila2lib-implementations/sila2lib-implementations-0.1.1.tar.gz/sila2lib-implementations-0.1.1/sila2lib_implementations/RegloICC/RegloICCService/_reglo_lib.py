# Written by Valeryia Sidarava and Lukas Bromig at TU Munich
# Institute of Biochemical Engineering
# Lukas.bromig@tum.de, valeryia.sidarava@tum.de
#
# Technical Support Ismatec Reglo ICC :
# Tel: 09377920344
# E-Mail: http://www.ismatec.de/download/documents/IDX1798-PD-IS_lr.pdf

import RegloICCService_client as testclient
import time


class Pump(testclient.RegloICCServiceClient):
    """Volume at Rate mode and Time at Rate mode"""

    def __init__(self):
        self.client = testclient.RegloICCServiceClient()
        
    #@staticmethod
    def pump_set_volume_at_flow_rate(self, return_val='', pump=1, flowrate=None, channels=[1, 2], volume=[80, 80],
                                     rotation=['K', 'K']):
        """
        Method to dispense a set volume (mL, max 2 decimal places, in a list []) with a set flow rate (mL/min, max 2
        decimal places, in a list []), rotation direction (J=clockwise, K=counter-clockwise, in a list []) for specific
        channel or channels.
        Pump address for Reglo ICC is set on 1, yet can be changed with SetPumpAddress function

        If several channels are used, there must be same number of values in each other parameter, except for pump
        and return_val.
        """

        #client = testclient.RegloICCServiceClient()
        start_time0 = time.time()

        # Channel addressing (ability to "speak" to each separate channel) and event messaging (pump reports on what is
        # going on) are being set to 1 (on). If it is already enabled, then the command is skipped

        if self.client.DeviceServicer_GetChannelAddressing(pump).ChannelAddressing.value is False:
            self.client.DeviceServicer_SetChannelAddressing(pump, True)
        
        # Checks whether the flow rate is set on RPM or mL/min and sets it to mL/min mode if needed:
        for i, channel in enumerate(channels):
            if self.client.ParameterControlServicer_GetFlowRateAtModes(int(channel)).CurrentFlowRate.value is False:
                self.client.ParameterControlServicer_SetFlowRateMode(str(channel)).PumpModeSet.value
        
        #print(flowrate)
        #flowrate=None
        # If flowrate was not defined, max calibrated values are used
        if flowrate is None:
            flowrate = []
            for i, channel in enumerate(channels):
                flowrate.append(self.client.ParameterControlServicer_GetMaximumFlowRateWithCalibration(channel).MaximumFlowRateWithCalibration.value)  # [:6])
            print('Calibrated maximum flow rate used: ', flowrate)
        
        # Iteration: for each channel the following commands will be executed
        for i, channel in enumerate(channels):
            # The channel is set to Volume at Rate mode, which allows to dispense a set volume with a set flow rate
            if self.client.ParameterControlServicer_GetMode(int(channel)).CurrentPumpMode.value != 'O':
                self.client.ParameterControlServicer_SetVolumeRateMode(channel)
            # The volume to dispense is set according to the setting in the head of the function (in mL)
            self.client.ParameterControlServicer_SetVolume(int(channel), float(volume[i]))

            # The flow rate is set according to the setting in the head of the function (in mL/min). Must be LESS or
            # EQUAL to the max. flow rate of the channel
            self.client.ParameterControlServicer_SetFlowRate(int(channel), float(flowrate[i]))

            # Gets the current rotation direction of the channel and compares to the desired setting. If the settings
            # do not match, the sets it to counter-clockwise ...
            if self.client.DriveControlServicer_GetPumpDirection(int(channel)).PumpDirection.value != rotation[i] and \
                    rotation[i] == 'K':
                self.client.DriveControlServicer_SetDirectionCounterClockwise(int(channel))
            # ... or clockwise rotation direction
        
            elif self.client.DriveControlServicer_GetPumpDirection(channel).PumpDirection.value != rotation[i] and \
                    rotation[i] == 'J':
                self.client.DriveControlServicer_SetDirectionClockwise(channel)
        
        start_time = time.time()    # notes the time
        for i, channel in enumerate(channels):
            # Starts pumping. The channel will stop as soon as the volume is dispensed
            self.client.DriveControlServicer_Start(int(channel))
            return_val=return_val+"Volume at Rate mode on channel %s for volume %s mL at rate %s mL/min set \n" % \
                       (channel, volume[i], flowrate[i])
        # print('--- Total execution time: %s seconds ---' %((time.time()-start_time0)))
        # returns the text with set parameters
        
        return return_val

    @staticmethod
    def pump_time_at_flow_rate(return_val='', pump=1, flowrate=None, channels=[1, 2], runtime=['10.5', '5.3'],
                               rotation=['K', 'K']):
        """
        Method to dispense for a set time duration (seconds, max 1 decimal place, in a list []) with a set flow rate
        (mL/min, max 2 decimal places, in a list []), rotation direction (J=clockwise, K=counter-clockwise, in a
        list []) for specific channel or channels.
        Pump address for Reglo ICC is set on 1, yet can be changed with SetPumpAddress function

        If several channels are used, there must be same number of values in each other parameter, except for pump and
        return_val.
        """

        client = testclient.RegloICCServiceClient()

        # Channel addressing (ability to "speak" to each separate channel) and event messaging (pump reports on what is
        # going on) are being set to 1 (on).
        # If it is already enabled, then the command are skipped
        if client.DeviceServicer_GetChannelAddressing(pump).ChannelAddressing.value is False:
            client.DeviceServicer_SetChannelAddressing(pump, 1)

        # checks, whether flowrate is set on RPM or mL/min and sets it to mL/min mode if needed:
        for i, channel in enumerate(channels):
            if client.ParameterControlServicer_GetFlowRateAtModes(int(channel)).CurrentFlowRate.value is False:
                client.ParameterControlServicer_SetFlowRateMode(str(channel)).PumpModeSet.value

        # If flowrate was not defined, max calibrated values are used
        if flowrate is None:
            flowrate = []
            for i, channel in enumerate(channels):
                k = client.ParameterControlServicer_GetMaximumFlowRateWithCalibration(channel).MaximumFlowRateWithCalibration.value
                flowrate.append(client.ParameterControlServicer_GetMaximumFlowRateWithCalibration(channel).MaximumFlowRateWithCalibration.value)
            print('Calibrated maximum flow rate used: ', flowrate)

        # Iteration: for each channel following commands will be executed
        for i, channel in enumerate(channels):
            # The channel is set to Time mode, with allows to dispense for a set time duration with a set flow rate
            if client.ParameterControlServicer_GetMode(channel).CurrentPumpMode.value != 'N':
                client.ParameterControlServicer_SetTimeMode(str(channel))
            # The time duration to dispense is set according to the setting in the head of the function (in seconds with
            # max. 1 decimal place)
            client.ParameterControlServicer_SetCurrentRunTime(channel, runtime[i])
            # The flow rate is set according to the setting in the head of the function (in mL/min). Must be LESS or
            # EQUAL to the max. flow rate of the channel
            client.ParameterControlServicer_SetFlowRate(channel, flowrate[i])

            # Gets the current rotation direction of the channel and compares to the desired setting. If the settings do
            # not match, the sets it to counter-clockwise ...
            if client.DriveControlServicer_GetPumpDirection(channel).PumpDirection.value != rotation[i] and \
                    rotation[i] == 'K':
                client.DriveControlServicer_SetDirectionCounterClockwise(channel)
            # ... or clockwise rotation direction
            elif client.DriveControlServicer_GetPumpDirection(channel).PumpDirection.value != rotation[i] and \
                    rotation[i] == 'J':
                client.DriveControlServicer_SetDirectionClockwise(channel)

        for i, channel in enumerate(channels):
            # Starts pumping. The channel will stop as soon as the volume is dispensed
            client.DriveControlServicer_Start(channel)
            return_val = return_val+"Time mode on channel %s for time %s seconds at rate %s mL/min set \n\n" % \
                         (channel, runtime[i], flowrate[i])
        return_val = return_val
        # returns the text with set parameters
        return return_val

    @staticmethod
    def pump_stop(return_val='', pump=1, channels=[1, 2]):
        """
        Method to stop the channel(s).
        """
        client = testclient.RegloICCServiceClient()

        # Channel addressing (ability to "speak" to each separate channel) and event messaging (pump reports on what is
        # going on) are being set to 1 (on).
        # If it is already enabled, then the command are skipped
        if client.DeviceServicer_GetChannelAddressing(pump).ChannelAddressing.value is False:
            client.DeviceServicer_SetChannelAddressing(pump, 1)

        for channel in channels:
            client.DriveControlServicer_Stop(channel)
            return_val = return_val+"Channel %s stopped \n\n" % channel
        # returns the text with set parameters
        return return_val

    #@staticmethod
    def pump_status(self, return_val='', pump=1):
        """
        Method to check whether the pump is currently running (+) or not (-).

        If one or more channels are in use, the status would be 'running'. However, it is impossible to distinguish,
        which and how many channels are used.
        """

        return_val = self.client.DeviceServicer_GetPumpStatus(pump).CurrentPumpStatus.value
        return return_val

import pytest
import logging
import time
import random
import string

from sila2lib_implementations.BioREACTOR48.BioREACTOR48Service.BioREACTOR48Service_client import BioREACTOR48ServiceClient


# define sample-size for all the tests
sample_size = 20

# initialize logging
logging.basicConfig(format  = '%(asctime)s - %(name)s - %(levelname)s- %(module)s - linenumber: %(lineno)d - %(message)s', level=logging.DEBUG)

# create object that will be used for the communication with the SiLA-Server
BioREACTOR48Object = BioREACTOR48ServiceClient(server_ip = '127.0.0.1', server_port =50004)
safe = False  # indicator that checks if all tests should be performed


# tests about the device servicer go here

def test_GetDeviceStatus():
    Answer = BioREACTOR48Object.DeviceServicer_GetDeviceStatus()

    Status = Answer.Status.value
    assert Status == 'OK'
    Mode = Answer.Mode.value
    assert Mode == 'REM' or Mode == 'OFF'


def test_GetReactorStatus():
    Answer = BioREACTOR48Object.DeviceServicer_GetReactorStatus()
    assert len(Answer.ReactorStatus) == 48
    for i in Answer.ReactorStatus:
        assert type(i.value) == bool


@pytest.mark.skip(reason="currently not implemented")
def test_GetBarNumber():
    Answer = BioREACTOR48Object.DeviceServicer_Get_BarNumber()
    assert Answer != None

@pytest.mark.skip(reason="currently not implemented")
def test_GetBarReactors():
    Answer = BioREACTOR48Object.DeviceServicer_Get_BarReactors()
    assert Answer != None

@pytest.mark.skip(reason="currently not implemented")
def test_GetTotalReactors():
    Answer = BioREACTOR48Object.DeviceServicer_Get_TotalReactors()
    assert Answer != None

# tests about the motor servicer go here

def test_GetPower():
    Answer = BioREACTOR48Object.MotorServicer_GetPower()
    Curr_Power = Answer.CurrentPower.value
    assert type(Curr_Power) == int
    assert Curr_Power < 101
    assert Curr_Power > -1


def test_GetRPM():
    Answer = BioREACTOR48Object.MotorServicer_GetRPM()
    Curr_RPM = Answer.CurrentRPM.value
    assert type(Curr_RPM) == int



@pytest.mark.parametrize("RPM", random.sample(range(100, 4000, 100), sample_size))
def test_SetRPM(RPM):
    Answer = BioREACTOR48Object.MotorServicer_SetRPM(RPM)

    Curr_RPM = Answer.CurrentStatus.value.split('_') # convert the answer to float to be able to compare, sila server outputs the raw string
    Curr_RPM = Curr_RPM[1]
    Curr_RPM = Curr_RPM[:-3]
    Curr_RPM = float(Curr_RPM)
    assert Curr_RPM == RPM




@pytest.mark.parametrize("Power", [25, 50,75,100])
def test_SetPower(Power):
    Answer = BioREACTOR48Object.MotorServicer_SetPower(Power)
    logging.debug(Answer)

    Curr_Power = Answer.CurrentStatus.value.split('_') # convert the answer to float to be able to compare, sila server outputs the raw string
    Curr_Power = Curr_Power[-2]
    logging.debug(f'The current answer is {Curr_Power}')
    Curr_Power = Curr_Power[5:]
    logging.debug(f'The current answer is {Curr_Power}')
    Curr_Power = float(Curr_Power)
    assert Curr_Power == Power


@pytest.fixture
def workflow_structure():
    Answer = BioREACTOR48Object.MotorServicer_SetPower(100) # set parameters for test of stirrer start
    Answer = BioREACTOR48Object.MotorServicer_SetRPM(2800) # set parameters for test of stirrer start
    yield None
    Answer = BioREACTOR48Object.MotorServicer_StopStirrer()


@pytest.mark.skipif(safe == False, reason='Cooling of BioREACTOR48 not connected, will not test stirrer start')
def test_StirrerControl(workflow_structure):
    Answer = BioREACTOR48Object.MotorServicer_StartStirrer()
    time.sleep(5)
    assert Answer != None
    Answer = BioREACTOR48Object.MotorServicer_StopStirrer()
    assert Answer != None

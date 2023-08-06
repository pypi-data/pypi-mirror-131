import os
from pydantic import BaseSettings

PROJECT_ROOT = os.path.abspath(os.path.dirname('./'))
PROJECT_ROOT = '/home/lnx/PycharmProjects/sila2lib_implementations'  # needed for my pycharm debugging
if os.path.isfile(PROJECT_ROOT + '/.env'):
    from dotenv import load_dotenv
    load_dotenv()


class Settings(BaseSettings):
    PRESENS_IP: str
    PRESENS_PORT: int
    PRESENS_SIMULATION_MODE: bool

    BIOREACTOR48_IP: str
    BIOREACTOR48_PORT: int
    BIOREACTOR48_SIMULATION_MODE: bool

    BLUEVARY_IP: str
    BLUEVARY_PORT: int
    BLUEVARY_SIMULATION_MODE: bool

    DASGIP_IP: str
    DASGIP_PORT: int
    DASGIP_SIMULATION_MODE: bool

    REGLOICC_IP: str
    REGLOICC_PORT: int
    REGLOICC_SIMULATION_MODE: bool

    REGLOCD_IP: str
    REGLOCD_PORT: int
    REGLOCD_SIMULATION_MODE: bool

    LAUDA_IP: str
    LAUDA_PORT: int
    LAUDA_SIMULATION_MODE: bool

    MTVIPERSW_IP: str
    MTVIPERSW_PORT: int
    MTVIPERSW_SIMULATION_MODE: bool

    FLOWMETER_IP: str
    FLOWMETER_PORT: int
    FLOWMETER_SIMULATION_MODE: bool


settings = Settings()

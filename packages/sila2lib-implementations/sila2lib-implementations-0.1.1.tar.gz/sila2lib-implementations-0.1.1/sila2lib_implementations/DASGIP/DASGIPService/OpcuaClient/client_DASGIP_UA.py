import logging
from opcua import Client
from .unit import Unit
logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger()

class clientDASGIP():
    
    client: Client
    unit_1: Unit
    unit_ID = None
    url = "opc.tcp://ctpc06642:51530/UA/connectServer" #To connect to DASGIP Server
    url = "opc.tcp://10.152.248.57:51530/UA/connectServer"

    def __init__(self, unit_ID = None):
        self.unit_ID = unit_ID

    def run(self):
        try:
            self.client = Client(url=self.url)
            self.client.set_user('Lukas Bromig')
            self.client.set_password('DigInBio')
            self.client.connect()
            self.unit = Unit(client=self.client, unit_ID=self.unit_ID)

        except Exception:
            _logger.exception('error')
        finally:
            pass
            
    def close(self):
        self.client.disconnect()
    #async def disconnect(self):
    #    await self.client.disconnect()

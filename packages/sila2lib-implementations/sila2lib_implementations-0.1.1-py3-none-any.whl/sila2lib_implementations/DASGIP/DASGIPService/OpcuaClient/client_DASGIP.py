import asyncio
import logging
from asyncua import Client, Node, ua

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

from .unit import Unit

class clientDASGIP():

    client: Client
    unit_1: Unit
    unit_ID = None
    url = "opc.tcp://ctpc06642:51530/UA/connectServer"     #To connect to DASGIP Server 
    
    def __init__(self, unit_ID = None):
        self.unit_ID = unit_ID
        
    async def run(self):
        try:
            self.client = Client(url=self.url)
            self.client.set_user('Lukas Bromig')
            self.client.set_password('DigInBio')
            #client.server_policy_uri("http://opcfoundation.org/UA/SecurityPolicy#Basic256Sha256")
            #client.application_uri = 'urn:CTPC06642:connectServer'
            #await client.set_security_string("Basic256Sha256,SignAndEncrypt,client_certificate.der,client_private_key.pem")
            await self.client.connect()
            #print("Unit%s"%self.unit_ID)
            #Initialize a number of unit objects depending on the number of specified number of reactors (unit_ID)
            self.unit = Unit(client=self.client, unit_ID=self.unit_ID)
        except Exception:
            _logger.exception('error')
        finally:
            await self.client.disconnect()
    #async def disconnect(self):
    #    self.client = Client(url=self.url)
    #    await self.client.disconnect()



















async def browse_nodes(node: Node):
    """
    Build a nested node tree dict by recursion (filtered by OPC UA objects and variables).
    """
    node_class = await node.get_node_class()
    children = []
    for child in await node.get_children():
        if await child.get_node_class() in [ua.NodeClass.Object, ua.NodeClass.Variable,ua.NodeClass.Unspecified, ua.NodeClass.Method,ua.NodeClass.ObjectType,ua.NodeClass.VariableType,ua.NodeClass.ReferenceType,ua.NodeClass.DataType,ua.NodeClass.View]:
            #    Unspecified = 0Object = 1Variable = 2Method = 4ObjectType = 8VariableType = 16ReferenceType = 32DataType = 64View = 128
            children.append(
                await browse_nodes(child)
            )
    if node_class != ua.NodeClass.Variable:
        var_type = None
    else:
        try:
            if (await node.get_data_type_as_variant_type()).value !=0:
                var_type = (await node.get_data_type_as_variant_type()).value
            else:
                pass
        except ua.UaError:
            _logger.warning('Node Variable Type could not be determined for %r', node)
            print("Hier",(await node.get_display_name()).Text)
            var_type = None
    return {
        'id': node.nodeid.to_string(),
        'name': (await node.get_display_name()).Text,
        'cls': node_class.value,
        'children': children,
        'type': var_type,
    }

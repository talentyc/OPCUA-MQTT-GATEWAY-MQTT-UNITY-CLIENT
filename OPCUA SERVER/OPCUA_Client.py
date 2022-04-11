# encoding=utf-8
from Logger import Logger
import sys,time
from opcua import Client,ua
import paho.mqtt.publish as MqttPublisher
import datetime
from Message import Message


class MqttBroker():
    def __init__(self, host, port=1883, username=None, password=None):
        self.host=host
        self.port=port
        self.username=username
        self.password=password
        Logger.trace('Created MqttBroker', fields={
            'host': host,
            'port': port,
            'username': username,
            'password': '***' if password is not None else None
        })
    
    def publish(self,message):
        assert isinstance(message,Message)
        self.publish_multiple([message])
        
    def publish_multiple(self,messages):
        msgs=[]
        for message in messages:
            assert isinstance(message,Message)
            msgs.append((message.topic(),message.payload()))
        auth =None
        if self.username is not None:
            auth = {"username": self.username, "password": self.password}
        Logger.trace('Publishing messages', fields={
            'count': len(msgs),
            'host': self.host,
            'port': self.port,
            'auth': True if auth is not None else False
        })
        MqttPublisher.multiple(msgs,hostname=self.host,port=self.port,auth=auth)

class OpcClient():
    def __init__(self, host, port, path='/', username=None, password=None):
        self._client=None
        self._subscription=None
        self._sub_handles={}
        self._handlers=[]

        auth=''
        if username is not None:
            auth='{}:{}@'.format(username,password)
        self._address=self._address_obfuscated='opc.tcp://{}{}:{}{}'.format(auth,host,port,path)
        
        if username is not None and password is not None:
            self._address_obfuscated=self._address.replace(password,'***')
        print('Created OpcClient, ','address:', self._address_obfuscated)
    
        self.init_client()
        self.init_subscriptions()

    def init_client(self):
        try:
            self._client=Client(self._address)
            self._client.connect()
            #self._client.load_type_definitions()
            self.namespace=self._client.get_namespace_array()
            print('Connection established')
        except Exception as e:
            print('Failed connecting to address "{}"'.format(self._address_obfuscated))
            print('{}'.format(e))
            raise e

    def full_uri(self, node):
        return '{}/{}'.format(
            node.nodeid.NamespaceIndex, node.nodeid.Identifier)    
    
    def init_subscriptions(self):
        if self._client is None:
            raise RuntimeError('Client not initialized yet.')
        self._subscription=self._client.create_subscription(500,self)
        print('Base Subscription established')

    def subscribe_variable(self,variable):
        if self._subscription is None:
            raise RuntimeError('Subscription not initialzed yet.')
        if variable in self._sub_handles.keys():
            print('Already subscribed to "{}"'.format(variable))
            return
        self._sub_handles[variable]=self._subscription.subscribe_data_change(variable)

    def unsubscribe_variable(self, variable):
        if self._subscription is None:
            raise RuntimeError('Subscriptions not initialized yet.')

        if variable not in self._sub_handles.keys():
            print('Not subscribed to "{}"'.format(variable))
            return
        self._subscription.unsubscribe(self._sub_handles[variable])
        del self._sub_handles[variable]

    def disconnect(self):
        if self._client is None:
            return
        try:
            self._client.disconnect()
        except Exception:
            pass
    def datachange_notification(self, node, value, data):
        timestamp = datetime.datetime.now()
        if hasattr(data, 'MonitoredItemNotification') and \
                hasattr(data.MonitoredItemNotification, 'SourceTimestamp'):
            timestamp = data.MonitoredItemNotification.SourceTimestamp
        Logger.debug('OpcClient: Received data change notification', fields={
            'node': node,
            'value': value,
            'data': data,
            'timestamp': timestamp.isoformat()
        })
        # send update to handlers
        update = {
            'node': node,
            'value': value,
            'data': data,
            'timestamp': timestamp
        }
        for hdl in self._handlers:  #list []
            hdl(update)

    def add_notification_handler(self,handler):
        self._handlers.append(handler)

class OPCUA_MQTT_GATEWAY():
    def __init__(self, opc_client, mqtt_client):
        self.opc_client = opc_client
        self.mqtt_client = mqtt_client
    
        def handler(update):
            # try:
            self.route_update(update)
            # except (Exception, IOError, RuntimeError) as e:
            #     Logger.error('Failed routing update: {}'.format(e))
        opc_client.add_notification_handler(handler)

    def route_update(self, update):
        uri=self.opc_client.full_uri(update['node'])
        msg=Message(uri, update['timestamp'], update['value'])
        self.mqtt_client.publish(msg)

    def setup_proxy_for(self, node):
        self.opc_client.subscribe_variable(node)

    def keep_alive(self):
        Logger.info('Locking Gateway')
        try:
            while True:
                time.sleep(1)
        except:
            Logger.info('Stopped Gateway')
            return

if __name__ == "__main__":
    # client = Client("opc.tcp://localhost:4840")
    # print(client.get_node(ua.NodeId(2, 2)))
    try:
        #Setup mqtt client
        mqtt_client=MqttBroker("113.66.160.30",port=1883,username="67b8aef0b3cf56e74edcccbe97612b2d",password="mqtt")
        #Setup OPC UA client
        opc_client=OpcClient("localhost",48484)
        #Setup OPCUA-MQTT GATEWAY
        opc_mqtt_gateway=OPCUA_MQTT_GATEWAY(opc_client,mqtt_client)
        #Get Target Node
        
        Watchdog=opc_client._client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.Controls.Watchdog")
        # AccessCode=opc_client._client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.Controls.AccessCode")
        # Hoist_Up=opc_client._client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.Controls.Hoist.Up")
        # Hoist_Down=opc_client._client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.Controls.Hoist.Down")
        # Hoist_Speed=opc_client._client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.Controls.Hoist.Speed")
        # Trolley_Forward=opc_client._client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.Controls.Trolley.Forward")
        # Trolley_Backward=opc_client._client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.Controls.Trolley.Backward")
        # Trolley_Speed=opc_client._client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.Controls.Trolley.Speed")
        # Bridge_Forward=opc_client._client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.Controls.Bridge.Forward")
        # Bridge_Backward=opc_client._client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.Controls.Bridge.Backward")
        # Bridge_Speed=opc_client._client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.Controls.Bridge.Speed")
        #smart feature
        Inching=opc_client._client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.RadioSelection.Inching")
        MicroSpeed=opc_client._client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.RadioSelection.MicroSpeed")
        RopeAngleFeaturesBypass=opc_client._client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.RadioSelection.RopeAngleFeaturesBypass")
        SwayControl=opc_client._client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.RadioSelection.SwayControl")
        SwayControl_SlingLength_mm=opc_client._client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.RadioSelection.SwayControl_SlingLength_mm")
        #position
        HoistPosition=opc_client._client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.Status.Hoist.Position.Position_m")
        BridgePosition=opc_client._client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.Status.Bridge.Position.Position_m")
        TrolleyPosition=opc_client._client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.Status.Trolley.Position.Position_m")
        
        test_node=opc_client._client.get_node("ns=2;i=2")
        #Setup subscriptions to the node
        opc_mqtt_gateway.setup_proxy_for(Inching)
        opc_mqtt_gateway.setup_proxy_for(MicroSpeed)
        opc_mqtt_gateway.setup_proxy_for(RopeAngleFeaturesBypass)
        opc_mqtt_gateway.setup_proxy_for(SwayControl)
        opc_mqtt_gateway.setup_proxy_for(SwayControl_SlingLength_mm)
        opc_mqtt_gateway.setup_proxy_for(HoistPosition)
        opc_mqtt_gateway.setup_proxy_for(BridgePosition)
        opc_mqtt_gateway.setup_proxy_for(TrolleyPosition)
        opc_mqtt_gateway.setup_proxy_for(test_node)
   
        #Loop
        opc_mqtt_gateway.keep_alive()

    finally:
        if opc_client is not None:
            opc_client.disconnect()

    # def handler(update):
    #     print('"{}", node:"{}", value:"{}"'.format(update["timestamp"],update['node'],update['value']))
    

    # # print(opc_client.full_uri(opc_client._client.get_node("ns=2;i=2")))
    # def handler(update):
    #     print('"{}", node:"{}", value:"{}"'.format(update["timestamp"],update['node'],update['value']))
        
    # opc_client.add_notification_handler(handler)
    # opc_client.subscribe_variable(opc_client._client.get_node("ns=2;i=2"))
    # time.sleep(10)
    # opc_client.disconnect()

    




    
    # client = Client("opc.tcp://localhost:4840")
    #     #client = Client("opc.tcp://127.0.0.1:4840/freeopcua/server/")
    #     #client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user
    # try:
    #     res = client.connect()
    #     print("Client connected")
    #     while True:
    #     #Test=client.get_node("ns=2;s=2")
    #         Test=client.get_node(ua.NodeId(2, 2))
    #         TIME=datetime.datetime.now().isoformat()
    #         print(TIME,Test.get_value())
    #         time.sleep(1)
    #     # Test.set_value(1)
    # finally:
    #     client.disconnect()



from pydoc import cli
import sys,time
from opcua import Client,ua
import paho.mqtt.publish as MqttPublisher
import datetime



client = Client("opc.tcp://localhost:4840")
    #client = Client("opc.tcp://127.0.0.1:4840/freeopcua/server/")
    #client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user
try:
    res = client.connect()
    print("Client connected")
    while True:
    #Test=client.get_node("ns=2;s=2")
        #Test=client.get_node(ua.NodeId(2, 2))
        Test=client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.Controls.Watchdog")
        print("Brower name:",Test.get_browse_name())  # QualifiedName(0:Watchdog)
        print("nodeid:",client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.Controls.Watchdog").nodeid) #StringNodeId(ns=7;s=SCF.PLC.DX_Custom_V.Controls.Watchdog)
        print("nodeid.NamespaceIndex:",client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.Controls.Watchdog").nodeid.NamespaceIndex) # 7
        print("nodeid.Identifier:",client.get_node("ns=7;s=SCF.PLC.DX_Custom_V.Controls.Watchdog").nodeid.Identifier)    #SCF.PLC.DX_Custom_V.Controls.Watchdog
        TIME=datetime.datetime.now().isoformat()
        print(TIME,Test.get_value())
        time.sleep(1)
    # Test.set_value(1)
finally:
    client.disconnect()
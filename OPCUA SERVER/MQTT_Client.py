from Logger import Logger
from Message import Message
import paho.mqtt.publish as MqttPublisher
from datetime import datetime
import time
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

if __name__ == "__main__":
    mqtt_topic="/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d"
    message=Message(mqtt_topic,datetime.now(),23)
    mqtt_client=MqttBroker("113.66.160.184",port=1883,username="67b8aef0b3cf56e74edcccbe97612b2d",password="mqtt")
    while True:
        mqtt_client.publish(message)
        time.sleep(1)
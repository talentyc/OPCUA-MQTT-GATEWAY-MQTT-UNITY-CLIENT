from Logger import Logger
from datetime import datetime
import json
class Message():
    TOPIC_PREFIX = '/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d'
    def __init__(self, uri, timestamp, value):
        self.__uri = uri
        self.__topic = '{}/{}'.format(Message.TOPIC_PREFIX, uri)
        self.__timestamp = timestamp
        self.__value = value
        Logger.trace('Created message', fields={
            'topic': self.__topic,
            'uri': self.__uri,
            'timestamp': self.__timestamp.isoformat(),
            'value': self.__value
        })
    def topic(self):
        return self.__topic

    def payload(self):
        return json.dumps(
            # 'topic': self.__topic,
            # 'uri': self.__uri,
            # 'timestamp': self.__timestamp.isoformat(),
            # 'value': self.__value
            self.__value
        )
if __name__ == "__main__":
    mqtt_topic="/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d"
    message=Message(mqtt_topic,datetime.now(),23)
    print(message.topic())
    print(message.payload())
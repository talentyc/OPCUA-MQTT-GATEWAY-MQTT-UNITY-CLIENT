from Logger import Logger
class Message():
    """A message to use for publishing.

    Use this to create a message object
    that the broker can simply publish to
    the remote.

    A message is expected to contain a "data-update",
    meaning a timestamp/value tuple. Each message
    then belongs to a topic which identifies the
    series.

    Attributes
    ----------
    __uri : str
        The identifier for origin of this message
    __topic : str
        The mqtt topic to publish this at
    __timestamp : datetime
        The datetime of the message
    __value : any
        The value of the message
    """

    TOPIC_PREFIX = '/idatase'
    def __init__(self, uri, timestamp, value):
        """Create a new message.

        Parameters
        ----------
        uri : str
            The identifier for origin of this message
        timestamp : datetime
            The datetime of the message
        value : any
            The value of the message
        """
        self.__topic = '{}/{}'.format(Message.TOPIC_PREFIX, uri)
        self.__uri = uri
        self.__timestamp = timestamp
        self.__value = value
        Logger.trace('Created message', fields={
            'topic': self.__topic,
            'uri': self.__uri,
            'timestamp': self.__timestamp.isoformat(),
            'value': self.__value
        })

    def topic(self):
        """Return the topic of the message.
        """
        return self.__topic

    def payload(self):
        """Return the payload of the message.
        """
        return json.dumps({
            'topic': self.__topic,
            'uri': self.__uri,
            'timestamp': self.__timestamp.isoformat(),
            'value': self.__value
        })
    
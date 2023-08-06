import json
from typing import Any

from cbaxter1988_utils.log_utils import get_logger
from pika import BlockingConnection, URLParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import ChannelClosed, ChannelClosedByBroker
from pika.exchange_type import ExchangeType

logger = get_logger(__name__)

PREFETCH_COUNT = 1


class PikaUtilsError(BaseException):
    """Utils Exception"""


class BlockingConnectionAdapter:

    def __init__(self, amqp_url):
        self.amqp_url = amqp_url
        self.url_params = URLParameters(url=self.amqp_url)
        self._prefetch_count = PREFETCH_COUNT

        self._prepare_connection()
        self._prepare_channel()

    def _prepare_connection(self):
        self._connection = get_blocking_connection(url=self.amqp_url)

    def _prepare_channel(self):
        if self._connection.is_closed:
            self._prepare_connection()
        else:
            self._channel = open_channel_from_connection(connection=self._connection)
            self._prepare_channel_qos()

    def get_channel(self):
        self._channel = open_channel_from_connection(connection=self.connection)
        return self._channel

    def _prepare_channel_qos(self):
        set_channel_qos(self._channel, prefetch_count=PREFETCH_COUNT)

    def _close_connection(self):
        logger.info(f"Closing Connection to '{self.amqp_url}'")
        return close_connection(self._connection)

    def _close_channel(self):
        return close_channel(channel=self._channel)

    def connect(self):
        if self._connection.is_closed:
            self._prepare_connection()
            self._prepare_channel()

    @property
    def channel(self):
        return self._channel

    @property
    def connection(self):
        return self._connection


class BasicPikaPublisher:
    logger = get_logger("BasicPublisher")

    def __init__(self, connection_adapter: BlockingConnectionAdapter, exchange, queue, routing_key):
        self.connection_adapter = connection_adapter
        self.exchange = exchange
        self.queue = queue
        self.routing_key = routing_key

    def publish_message(self, body: Any):
        try:
            bind_queue(
                connection=self.connection_adapter.connection,
                queue=self.queue,
                exchange=self.exchange,
                routing_key=self.routing_key
            )

            publish_message(
                connection=self.connection_adapter.connection,
                exchange=self.exchange,
                routing_key=self.routing_key,
                data=body
            )
        except ChannelClosedByBroker as err:
            logger.error(f'{err}')
            self.bind_routing_key(exchange=self.exchange, queue=self.queue, routing_key=self.routing_key)
            publish_message(
                self.connection_adapter.connection,
                exchange=self.exchange,
                routing_key=self.routing_key,
                data=body
            )

    def publish(self, routing_key, body):
        if self.connection_adapter.connection.is_open:
            self.connection_adapter.channel.basic_publish(exchange=self.exchange, routing_key=routing_key,
                                                          body=body)

    def declare_exchange(self, exchange=None):
        if exchange:
            self.exchange = exchange

        create_exchange(connection=self.connection_adapter.connection, exchange=self.exchange)

    def declare_queue(self, queue=None):
        if queue:
            self.queue = queue

        create_queue(connection=self.connection_adapter.connection, queue=self.queue)

    def bind_routing_key(self, exchange, queue, routing_key):
        self.declare_exchange(exchange)
        self.declare_queue(queue)
        if routing_key:
            self.routing_key = routing_key

        bind_queue(
            connection=self.connection_adapter.connection,
            queue=self.queue,
            exchange=self.exchange,
            routing_key=self.routing_key
        )

    @property
    def connection(self):
        return self.connection_adapter.connection

    @property
    def channel(self):
        return self.connection_adapter.channel


class BasicPikaConsumer:

    def __init__(
            self,
            connection_adapter: BlockingConnectionAdapter,
            queue,
            on_message_callback: callable
    ):

        self.connection_adapter = connection_adapter
        self.on_message_callback = on_message_callback
        self.queue = queue

        self.pika_queue_service_wrapper = PikaQueueServiceWrapper(amqp_url=self.connection_adapter.amqp_url)

    def _consume(self):
        if self.connection_adapter.connection.is_open and self.connection_adapter.channel.is_open:

            try:
                self.connection_adapter.channel.basic_consume(self.queue, self.on_message_callback)
                logger.info(f'Awaiting Message on channel: {self.connection_adapter.channel.channel_number}')
                self.connection_adapter.channel.start_consuming()


            except KeyboardInterrupt:
                self.connection_adapter.channel.stop_consuming()

            except ChannelClosedByBroker:
                raise
        else:
            self.connection_adapter.connect()

            self.connection_adapter.channel.basic_consume(self.queue, self.on_message_callback)
            self.connection_adapter.channel.start_consuming()

    def _validate_queue(self):
        logger.info(f"Validating Queue: '{self.queue}'")
        # self.pika_queue_service_wrapper.create_queue(
        #     queue=self.queue,
        #
        # )
        # conn = self.connection_adapter.connection
        # if not validate_queue(conn, queue=self.queue):
        #     logger.info(f"{self.queue} not present")
        #     create_queue(conn, queue=self.queue)

        #
        # else:
        #     logger.info(f'({self.queue}) has been validated')

    def run(self):
        # self._validate_queue()

        if self.connection_adapter.connection.is_closed:
            logger.info("Connection Closed, Reopening")
            self.connection_adapter.connect()

        if self.connection_adapter.channel.is_closed:
            logger.info("Channel Closed, Reopening")
            self.connection_adapter.get_channel()

        logger.info("Starting Consumer")
        self._consume()


def make_amqp_url(amqp_user, amqp_pw, amqp_host, amqp_port):
    return f"amqp://{amqp_user}:{amqp_pw}@{amqp_host}:{amqp_port}"


def validate_queue(connection: BlockingConnection, queue) -> bool:
    ch = open_channel_from_connection(connection)
    try:

        ch.queue_declare(queue=queue, passive=True)
        close_channel(ch)
        return True
    except ChannelClosed:
        close_channel(ch)

        return False


def create_queue(connection: BlockingConnection, queue, arguments: dict = None) -> bool:
    ch = open_channel_from_connection(connection)
    logger.info(f"Creating/Validating Queue='{queue}'")
    result = ch.queue_declare(queue=queue, arguments=arguments)

    close_channel(ch)
    return result


def delete_queue(connection: BlockingConnection, queue, if_empty=False, if_unused=False) -> bool:
    ch = open_channel_from_connection(connection)
    results = ch.queue_delete(queue=queue, if_empty=if_empty, if_unused=if_unused)
    close_channel(ch)
    if results:
        logger.debug(f"Removing Queue: {queue}")
        return True
    else:
        return False


def purge_queue(connection: BlockingConnection, queue):
    ch = open_channel_from_connection(connection)
    if ch.is_open:
        logger.debug(f"Purging Queue: {queue}")
        ch.queue_purge(queue=queue)
        return True

    else:
        raise PikaUtilsError(f"{ch.channel_number} is Closed")


def create_exchange(connection: BlockingConnection, exchange: str, exchange_type='direct') -> bool:
    ch = open_channel_from_connection(connection)
    if ExchangeType(exchange_type):
        try:
            logger.info(f'Creating/Validating Exchange={exchange}, ExchangeType={exchange_type}')
            ch.exchange_declare(exchange=exchange, exchange_type=ExchangeType(exchange_type).value, durable=True)

        except Exception:
            raise

        close_channel(ch)
        return True
    else:
        return False


def delete_exchange(connection: BlockingConnection, exchange, if_unused=False) -> bool:
    ch = open_channel_from_connection(connection)
    try:
        ch.exchange_delete(exchange=exchange, if_unused=if_unused)
    except Exception:
        raise

    close_channel(ch)
    return True


def bind_queue(connection: BlockingConnection, queue, exchange, routing_key) -> bool:
    ch = open_channel_from_connection(connection)
    try:
        logger.info(f"Binding Exchange='{exchange}' to Queue='{queue}' with Key='{routing_key}')")
        ch.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)

    except Exception:
        raise

    close_channel(ch)
    return True


def unbind_queue(connection: BlockingConnection, queue, exchange, routing_key) -> bool:
    ch = open_channel_from_connection(connection)
    try:
        ch.queue_unbind(queue=queue, exchange=exchange, routing_key=routing_key)
    except Exception:
        raise

    close_channel(ch)
    return True


def open_channel_from_connection(connection: BlockingConnection) -> BlockingChannel:
    if connection.is_open:
        channel = connection.channel()
        logger.debug(f"Opened Channel: {channel.channel_number}")
        return channel
    else:
        raise PikaUtilsError(f"{connection} is Closed")


def close_channel(channel: BlockingChannel):
    if channel.is_open:
        logger.debug(f"Closing Channel: {channel.channel_number}")
        channel.close()
        return True
    else:
        return False


def close_connection(connection: BlockingConnection):
    if connection.is_open:
        logger.info(f"Closing Connection: {str(connection)}")
        connection.close()
        return True
    else:
        return False


def set_channel_qos(channel: BlockingChannel, prefetch_count):
    if channel.is_open:
        channel.basic_qos(prefetch_count=prefetch_count)
        return True
    else:
        raise PikaUtilsError(f"{channel.channel_number} is Closed")


def get_blocking_connection(url) -> BlockingConnection:
    logger.info(f"Connecting to URL: '{url}'")
    return BlockingConnection(
        parameters=URLParameters(url=url)
    )


def publish_message(connection: BlockingConnection, exchange: str, routing_key: str, data: Any) -> bool:
    ch = open_channel_from_connection(connection)
    if ch.is_open:
        try:
            logger.info(f"Publishing Message: {data}")
            if isinstance(data, bytes):
                ch.basic_publish(exchange=exchange, routing_key=routing_key, body=data)

            if isinstance(data, dict):
                ch.basic_publish(exchange=exchange, routing_key=routing_key, body=json.dumps(data).encode())

            close_channel(ch)
            return True
        except Exception:
            raise
    else:

        raise PikaUtilsError(f"{ch.channel_number} is Closed")


def acknowledge_message(channel: BlockingChannel, delivery_tag):
    channel.basic_ack(delivery_tag=delivery_tag)


def nacknowledge_message(channel: BlockingChannel, delivery_tag):
    channel.basic_nack(delivery_tag=delivery_tag)


class PikaQueueServiceWrapper:
    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url

        self.connection_adapter = BlockingConnectionAdapter(
            amqp_url=amqp_url
        )

    def create_queue(
            self,
            queue: str,
            dlq_queue: str = None,
            dlq_support: bool = False,
            dlq_exchange: str = None,
            dlq_routing_key: str = None
    ):
        queue_arguments = {}

        if dlq_support:
            create_queue(connection=self.connection_adapter.connection, queue=dlq_queue)
            create_exchange(connection=self.connection_adapter.connection, exchange=dlq_exchange)
            bind_queue(connection=self.connection_adapter.connection, queue=dlq_queue, exchange=dlq_exchange,
                       routing_key=dlq_routing_key)

            queue_arguments['x-dead-letter-exchange'] = dlq_exchange
            queue_arguments['x-dead-letter-routing-key'] = dlq_routing_key

            logger.info(f'Prepared Pika Queue Arguments={queue_arguments}')

        create_queue(connection=self.connection_adapter.connection, queue=queue, arguments=queue_arguments)

    def purge_queue(self, queue: str):
        purge_queue(connection=self.connection_adapter.connection, queue=queue)

    def delete_queue(self, queue: str, if_empty: bool = True):
        delete_queue(connection=self.connection_adapter.connection, queue=queue, if_empty=if_empty)


def make_basic_pika_publisher(amqp_url, exchange, queue, routing_key) -> BasicPikaPublisher:
    adapter = BlockingConnectionAdapter(amqp_url=amqp_url)
    return BasicPikaPublisher(connection_adapter=adapter, queue=queue, exchange=exchange, routing_key=routing_key)


def make_basic_pika_consumer(amqp_url, queue, on_message_callback: callable) -> BasicPikaConsumer:
    adapter = BlockingConnectionAdapter(amqp_url=amqp_url)
    return BasicPikaConsumer(connection_adapter=adapter, queue=queue, on_message_callback=on_message_callback)

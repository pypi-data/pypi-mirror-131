from typing import Any

import pika
from cbaxter1988_utils.log_utils import get_logger
from cbaxter1988_utils.pika_utils import (
    get_blocking_connection,
    open_channel_from_connection,
    set_channel_qos,
    close_channel,
    close_connection,
    publish_message,
    create_exchange,
    create_queue,
    bind_queue,
    validate_queue
)
from pika.exceptions import ChannelClosedByBroker

PREFETCH_COUNT = 1

logger = get_logger(__name__)


class BlockingConnectionAdapter:

    def __init__(self, amqp_url):
        self.amqp_url = amqp_url
        self.url_params = pika.URLParameters(url=self.amqp_url)
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
            publish_message(
                connection=self.connection_adapter.connection,
                exchange=self.exchange,
                routing_key=self.routing_key,
                data=body
            )
        except ChannelClosedByBroker:
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
        conn = self.connection_adapter.connection
        if not validate_queue(conn, queue=self.queue):
            logger.info(f"{self.queue} not present")
            create_queue(conn, queue=self.queue)


        else:
            logger.info(f'({self.queue}) has been validated')

    def run(self):
        self._validate_queue()

        if self.connection_adapter.connection.is_closed:
            logger.info("Connection Closed, Reopening")
            self.connection_adapter.connect()

        if self.connection_adapter.channel.is_closed:
            logger.info("Channel Closed, Reopening")
            self.connection_adapter.get_channel()

        logger.info("Starting Consumer")
        self._consume()

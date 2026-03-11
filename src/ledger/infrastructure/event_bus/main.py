from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from aio_pika.abc import AbstractConnection, AbstractChannel
from aio_pika.pool import Pool

from .config import EventBusConfig
from .factories import ConnectionFactory, ChannelFactory


@asynccontextmanager
async def build_rq_connection_pool(
    event_bus_config: EventBusConfig,
) -> AsyncGenerator[Pool[AbstractConnection], None]:
    connection_pool = Pool(ConnectionFactory(event_bus_config).get_connection, max_size=10)
    async with connection_pool:
        yield connection_pool


@asynccontextmanager
async def build_rq_channel_pool(
    rq_connection_pool: Pool[AbstractConnection],
) -> AsyncGenerator[Pool[AbstractChannel], None]:
    channel_pool = Pool(ChannelFactory(rq_connection_pool).get_channel, max_size=100)
    async with channel_pool:
        yield channel_pool

# ruff: noqa: E402
import asyncio

from .config import Settings

_config = Settings.get_config()

from openg2p_fastapi_common.app import Initializer as BaseInitializer
from openg2p_g2pconnect_mapper_lib.app import Initializer as MapperBaseInitializer

from .controllers import (
    AsyncMapperController,
    SyncMapperController,
)
from .models import IdFaMapping
from .services import (
    AsyncRequestHelper,
    AsyncResponseHelper,
    IdFaMappingValidations,
    MapperService,
    RequestValidation,
    SyncRequestHelper,
    SyncResponseHelper,
)


class Initializer(BaseInitializer):
    def initialize(self, **kwargs):
        super().initialize()

        MapperService()
        IdFaMappingValidations()
        SyncRequestHelper()
        AsyncRequestHelper()
        RequestValidation()
        SyncResponseHelper()
        AsyncResponseHelper()
        SyncMapperController().post_init()
        AsyncMapperController().post_init()
        MapperBaseInitializer()

    def migrate_database(self, args):
        super().migrate_database(args)

        async def migrate():
            await IdFaMapping.create_migrate()

        asyncio.run(migrate())

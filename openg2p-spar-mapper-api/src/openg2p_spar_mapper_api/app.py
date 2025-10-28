# ruff: noqa: E402
import asyncio
import logging

from .config import Settings

_config = Settings.get_config()

from openg2p_fastapi_common.app import Initializer as BaseInitializer
from openg2p_spar_mapper_core.services import (
    IdFaMappingValidations,
    MapperService,
    RequestValidation,
    ResponseHelper,
)
from openg2p_spar_models.models import (
    IdFaMapping,
)

from .controllers import MapperController

_logger = logging.getLogger(_config.logging_default_logger_name)


class Initializer(BaseInitializer):
    def initialize(self, **kwargs):
        super().initialize()

        IdFaMappingValidations()
        RequestValidation()
        MapperService()
        ResponseHelper()

        MapperController().post_init()

    def migrate_database(self, args):
        super().migrate_database(args)

        async def migrate():
            _logger.info("Migrating database")
            await IdFaMapping.create_migrate()

        asyncio.run(migrate())

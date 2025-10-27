# ruff: noqa: E402
import logging
import asyncio

from .config import Settings
_config = Settings.get_config()

from openg2p_fastapi_common.app import Initializer as BaseInitializer
from openg2p_spar_mapper_core.services import MapperService, ResponseHelper, RequestValidation, IdFaMappingValidations, DfspService
from openg2p_spar_models.models import IdFaMapping, Strategy, DfspProvider, DfspProviderValue

from .controllers import MapperController, DfspController

_logger = logging.getLogger(_config.logging_default_logger_name)


class Initializer(BaseInitializer):
    def initialize(self, **kwargs):
        super().initialize()
        _logger.info("Initializing SPAR Bene Portal API")
        IdFaMappingValidations()
        RequestValidation()
        MapperService()
        ResponseHelper()
        DfspService()

        MapperController().post_init()
        DfspController().post_init()

    def migrate_database(self, args):
        super().migrate_database(args)

        async def migrate():
            _logger.info("Migrating database")
            await IdFaMapping.create_migrate()
            await Strategy.create_migrate()
            await DfspProvider.create_migrate()
            await DfspProviderValue.create_migrate()

        asyncio.run(migrate())


            

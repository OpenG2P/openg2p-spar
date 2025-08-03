from openg2p_g2pconnect_mapper_lib.config import Settings as BaseSettings
from pydantic import AnyUrl
from pydantic_settings import SettingsConfigDict

from . import __version__


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="spar_mapper_", env_file=".env", extra="allow")

    openapi_title: str = "OpenG2P SPAR Account Mapper"
    openapi_description: str = """
    This module maps the beneficiary ID to a Financial Address.

    ***********************************
    Further details goes here
    ***********************************
    """
    openapi_version: str = __version__

    db_dbname: str = "openg2p_spar_db"

    default_callback_url: AnyUrl | None = None
    default_callback_timeout: int = 10

    jwt_validate_keymanager_app_id: str = "OPENG2P_SPAR_MAPPER"
    keymanager_auth_client_id: str = "openg2p-spar"

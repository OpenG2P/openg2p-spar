#!/usr/bin/env python3

# ruff: noqa: I001

from openg2p_spar_mapper_api.app import Initializer

from openg2p_fastapi_common.ping import PingInitializer
from openg2p_fastapi_common.context import app_registry

initializer = Initializer()
PingInitializer()
# initializer.main()
mapper_app = app_registry.get()

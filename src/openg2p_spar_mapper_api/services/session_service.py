from openg2p_fastapi_common.context import dbengine
from openg2p_fastapi_common.service import BaseService
from sqlalchemy.ext.asyncio import async_sessionmaker


class SessionInitializer(BaseService):
    def __init__(self):
        super().__init__("SessionInitializer")
        self.session_maker = None

    async def retrieve_session(self):
        if not self.session_maker:
            self.session_maker = async_sessionmaker(
                dbengine.get(), expire_on_commit=False
            )
        return self.session_maker

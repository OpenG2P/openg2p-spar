from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from openg2p_fastapi_common.service import BaseService
from openg2p_fastapi_common.context import dbengine


class SessionInitializer(BaseService):

    def __init__(self):
        super().__init__("SessionInitializer")
        self.session_maker = None

    async def retrieve_session(self) -> AsyncSession:
        if not self.session_maker:
            session_maker = async_sessionmaker(dbengine.get(), expire_on_commit=False)
        return session_maker

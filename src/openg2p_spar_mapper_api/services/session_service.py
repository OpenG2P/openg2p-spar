from openg2p_fastapi_common.context import dbengine
from openg2p_fastapi_common.service import BaseService
from sqlalchemy.ext.asyncio import async_sessionmaker


class SessionInitializer(BaseService):
    async def retrieve_session(self):
        session_maker = async_sessionmaker(dbengine.get(), expire_on_commit=False)
        return session_maker

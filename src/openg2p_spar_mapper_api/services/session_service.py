from openg2p_fastapi_common.context import dbengine
from openg2p_fastapi_common.service import BaseService
from sqlalchemy.ext.asyncio import async_sessionmaker


class SessionInitializer(BaseService):
    def __init__(self):
        super().__init__("SessionInitializer")
        self.session = None

    async def retrieve_session(self):
        if not self.session:
            session_maker = async_sessionmaker(dbengine.get(), expire_on_commit=False)
        async with session_maker() as session:
            self.session = session
        return self.session

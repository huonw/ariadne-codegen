from typing import Any, List, Optional

from .async_base_client import AsyncBaseClient
from .test import Test

gql = lambda q: q


class Client(AsyncBaseClient):
    async def test(self) -> Test:
        query = gql(
            """
            query test {
              testQuery
            }
            """
        )
        variables: dict = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return Test.parse_obj(data)

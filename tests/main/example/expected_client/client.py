from typing import Any, List, Optional

from .async_base_client import AsyncBaseClient
from .create_user import CreateUser
from .input_types import UserCreateInput
from .list_all_users import ListAllUsers
from .list_users_by_country import ListUsersByCountry

gql = lambda q: q


class Client(AsyncBaseClient):
    async def create_user(self, user_data: UserCreateInput) -> CreateUser:
        query = gql(
            """
            mutation CreateUser($userData: UserCreateInput!) {
              userCreate(userData: $userData) {
                id
              }
            }
            """
        )
        variables: dict = {"userData": user_data}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return CreateUser.parse_obj(data)

    async def list_all_users(self) -> ListAllUsers:
        query = gql(
            """
            query ListAllUsers {
              users {
                id
                firstName
                lastName
                email
                location {
                  country
                }
              }
            }
            """
        )
        variables: dict = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListAllUsers.parse_obj(data)

    async def list_users_by_country(self, country: str) -> ListUsersByCountry:
        query = gql(
            """
            query ListUsersByCountry($country: String!) {
              users(country: $country) {
                ...BasicUser
                ...UserPersonalData
                favouriteColor
              }
            }

            fragment BasicUser on User {
              id
              email
            }

            fragment UserPersonalData on User {
              firstName
              lastName
            }
            """
        )
        variables: dict = {"country": country}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListUsersByCountry.parse_obj(data)

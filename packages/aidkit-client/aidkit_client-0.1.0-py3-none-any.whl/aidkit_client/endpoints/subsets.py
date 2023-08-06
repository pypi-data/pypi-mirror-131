from aidkit_client.aidkit_api import HTTPService
from aidkit_client.constants import Constants
from aidkit_client.endpoints.models import SubsetResponse
from aidkit_client.exceptions import AidkitCLIError, ResourceWithIdNotFoundError


class SubsetAPI:
    api: HTTPService

    def __init__(self, api: HTTPService):
        self.api = api

    async def get(self, name: str) -> SubsetResponse:
        result = await self.api.get(
            path=f"{Constants.SUBSETS_PATH}/{name}", parameters=None
        )
        if result.is_not_found:
            raise ResourceWithIdNotFoundError(f"Subset with name {name} not found")
        if not result.is_success:
            raise AidkitCLIError(
                f"Error fetching Subset with name {name}. Error: {result.body}"
            )
        return SubsetResponse(**result.body)

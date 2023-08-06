from aidkit_client.aidkit_api import HTTPService
from aidkit_client.configuration import get_api_client
from aidkit_client.endpoints.models import SubsetResponse
from aidkit_client.endpoints.subsets import SubsetAPI


class Subset:
    def __init__(
        self, api_service: HTTPService, subset_response: SubsetResponse
    ) -> None:
        self._data = subset_response
        self._api_service = api_service

    @classmethod
    async def get_by_name(cls, name: str) -> "Subset":
        api_service = get_api_client()
        response = await SubsetAPI(api_service).get(name)
        return Subset(api_service, response)

    @property
    def id(self) -> int:
        return self._data.id

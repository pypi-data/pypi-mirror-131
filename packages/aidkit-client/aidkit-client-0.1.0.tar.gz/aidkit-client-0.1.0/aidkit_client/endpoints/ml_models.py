from typing import List

from aidkit_client.aidkit_api import HTTPService
from aidkit_client.constants import Constants
from aidkit_client.endpoints.models import (
    ListMLModelResponse,
    MLModelResponse,
    MLModelVersionResponse,
)
from aidkit_client.exceptions import AidkitCLIError, ResourceWithIdNotFoundError


class MLModelsAPI:
    api: HTTPService

    def __init__(self, api: HTTPService):
        self.api = api

    async def get_all(self) -> List[MLModelResponse]:
        result = await self.api.get(path=Constants.ML_MODELS_PATH, parameters=None)
        if not result.is_success:
            raise Exception("Failed to retrieve MLModels")
        return ListMLModelResponse(**result.body).ml_models

    async def get(self, name: str) -> MLModelResponse:
        result = await self.api.get(
            path=f"{Constants.ML_MODELS_PATH}/{name}", parameters=None
        )
        if result.is_not_found:
            raise ResourceWithIdNotFoundError(f"MLModel with name {name} not found")
        if not result.is_success:
            raise AidkitCLIError(
                f"Error fetching MLModel with name {name}. Error: {result.body}"
            )
        return MLModelResponse(**result.body)

    async def update(self, name: str, new_name: str) -> MLModelResponse:
        result = await self.api.patch(
            path=f"{Constants.ML_MODELS_PATH}/{name}",
            parameters=None,
            body={"name": new_name},
        )
        if result.is_bad:
            raise ResourceWithIdNotFoundError(
                f"Could not update MLModel name with {name}"
            )
        if not result.is_success:
            raise AidkitCLIError(
                f"Error patching MLModel with name {name}. Error: {result.body}"
            )
        return MLModelResponse(**result.body)

    async def upload_model_version(
        self, model_name: str, model_version: str, model_file_content: bytes
    ) -> MLModelVersionResponse:

        result = await self.api.post_multipart_data(
            path=f"{Constants.ML_MODELS_PATH}/{model_name}/versions",
            data={"name": model_version},
            files={"model": model_file_content},
        )
        if result.is_bad:
            raise ResourceWithIdNotFoundError(
                f"Could not update MLModel: {model_name} with version: {model_version}"
            )
        if not result.is_success:
            raise AidkitCLIError(
                f"Error updating MLModel: {model_name} with version {model_version}."
                f"Error: {result.body}"
            )
        return MLModelVersionResponse(**result.body)

    async def delete(self, name: str) -> bool:
        response = await self.api.delete(path=f"{Constants.ML_MODELS_PATH}/{name}")
        return response.is_success

from typing import List

from aidkit_client.aidkit_api import HTTPService
from aidkit_client.constants import Constants
from aidkit_client.endpoints.models import (
    CreatePipelineRunRequest,
    PipelineRunListResponse,
    PipelineRunResponse,
    TabularReport,
    UserProvidedContext,
)
from aidkit_client.exceptions import AidkitCLIError, ResourceWithIdNotFoundError


class PipelineRunsAPI:
    api: HTTPService

    def __init__(self, api: HTTPService):
        self.api = api

    async def get_all(self) -> List[PipelineRunResponse]:
        result = await self.api.get(path=Constants.PIPELINE_RUNS_PATH, parameters=None)
        if not result.is_success:
            raise Exception("Failed to retrieve PipelineRuns")

        return PipelineRunListResponse(**result.body).pipeline_runs

    async def run_pipeline(
        self, pipeline_id: int, context: List[UserProvidedContext]
    ) -> PipelineRunResponse:
        body = CreatePipelineRunRequest(pipeline_id=pipeline_id, context=context).dict()
        result = await self.api.post_json(
            path=Constants.PIPELINE_RUNS_PATH,
            body=body,
            parameters=None,
        )
        if not result.is_success:
            raise Exception(
                f"Failed to create PipelineRun with ID: {pipeline_id}: Error: {result.body}"
            )
        return PipelineRunResponse(**result.body)

    async def get(self, pipeline_run_id: int) -> PipelineRunResponse:
        result = await self.api.get(
            path=f"{Constants.PIPELINE_RUNS_PATH}/{pipeline_run_id}", parameters=None
        )
        if result.is_not_found:
            raise ResourceWithIdNotFoundError(
                f"PipelineRun with ID: {pipeline_run_id} not found"
            )
        if not result.is_success:
            raise AidkitCLIError(
                f"Error fetching PipelineRun with ID: {pipeline_run_id}. Error: {result.body}"
            )
        return PipelineRunResponse(**result.body)

    async def get_report(self, pipeline_run_id: int) -> TabularReport:
        result = await self.api.get(
            path=f"{Constants.PIPELINE_RUNS_PATH}/{pipeline_run_id}/report",
            parameters=None,
        )
        if result.is_not_found:
            raise ResourceWithIdNotFoundError(
                f"PipelineRun with ID: {pipeline_run_id} not found"
            )
        if not result.is_success:
            raise AidkitCLIError(
                f"Error fetching PipelineRun with ID: {pipeline_run_id}. Error: {result.body}"
            )
        return TabularReport(**result.body)

import asyncio
from enum import Enum
from functools import reduce
from time import time
from typing import Optional, Type, Union

from aidkit_client.aidkit_api import HTTPService
from aidkit_client.configuration import get_api_client
from aidkit_client.endpoints.models import (
    IdentifierInput,
    PipelineRunResponse,
    PipelineRunState,
    RequiredContextDescription,
    TabularReport,
    TargetClassInput,
    UserProvidedContext,
)
from aidkit_client.endpoints.pipeline_runs import PipelineRunsAPI
from aidkit_client.endpoints.pipelines import PipelineResponse, PipelinesAPI
from aidkit_client.exceptions import ResourceWithNameNotFoundError, RunTimeoutError
from aidkit_client.resources.dataset import Subset
from aidkit_client.resources.ml_model import MLModelVersion
from tabulate import tabulate


class PipelineRun:
    def __init__(
        self, api_service: HTTPService, pipeline_run_response: PipelineRunResponse
    ) -> None:
        self._data = pipeline_run_response
        self._api_service = api_service

    @classmethod
    async def get_by_id(cls, pipeline_run_id: int) -> "PipelineRun":
        api_service = get_api_client()
        response = await PipelineRunsAPI(api_service).get(pipeline_run_id)
        return PipelineRun(api_service, response)

    async def get_state(self) -> PipelineRunState:
        # if one node is stopped, the whole run is stopped
        # else, if any node is running, the whole pipeline is running
        # otherwise, it's either pending or finished
        response = await PipelineRunsAPI(self._api_service).get(self._data.id)

        def _reduce_state(
            left_state: PipelineRunState, right_state: PipelineRunState
        ) -> PipelineRunState:
            if PipelineRunState.FAILED in (left_state, right_state):
                return PipelineRunState.FAILED
            if PipelineRunState.STOPPED in (left_state, right_state):
                return PipelineRunState.STOPPED
            if (
                left_state == PipelineRunState.PENDING
                and right_state == PipelineRunState.PENDING
            ):
                return PipelineRunState.PENDING
            if (
                left_state == PipelineRunState.SUCCESS
                and right_state == PipelineRunState.SUCCESS
            ):
                return PipelineRunState.SUCCESS
            return PipelineRunState.RUNNING

        return reduce(_reduce_state, (node.state for node in response.nodes))

    async def report(self, pipeline_finish_timeout: Optional[int] = None) -> "Report":
        starting_time = time()
        current_time = starting_time
        while (
            pipeline_finish_timeout is None
            or current_time - starting_time < pipeline_finish_timeout
        ):
            current_status = await self.get_state()
            if current_status in [PipelineRunState.FAILED, PipelineRunState.STOPPED]:
                raise ValueError(
                    f"Pipeline is not run successful. State is {current_status}"
                )
            await asyncio.sleep(1)
            if current_status == PipelineRunState.SUCCESS:
                return await Report.get_by_pipeline_run_id(self._data.id)
            current_time = time()
        raise RunTimeoutError(
            f"Pipeline has not finished after the timeout of {pipeline_finish_timeout} seconds."
        )


class _ContextNames(Enum):
    ML_MODEL_VERSION = "ml_model_version_identifier"
    SUBSET = "subset_identifier"


_TARGET_CLASS_NAME = "TargetClassInput"


class Pipeline:
    def __init__(
        self, api_service: HTTPService, pipeline_response: PipelineResponse
    ) -> None:
        self._data = pipeline_response
        self._api_service = api_service

    @classmethod
    async def get_by_id(cls, pipeline_id: int) -> "Pipeline":
        api_service = get_api_client()
        pipeline_response = await PipelinesAPI(api_service).get_by_id(pipeline_id)
        return Pipeline(api_service, pipeline_response)

    @property
    def id(self) -> int:
        return self._data.id

    @property
    def name(self) -> str:
        return self._data.name

    async def run(
        self,
        model_version: Union[int, MLModelVersion],
        subset: Union[int, Subset],
        target_class: Optional[int] = None,
    ) -> PipelineRun:
        if isinstance(model_version, MLModelVersion):
            model_version_id = model_version.id
        else:
            model_version_id = model_version
        if isinstance(subset, Subset):
            subset_id = subset.id
        else:
            subset_id = subset
        required_context = self._data.context

        def required_context_to_context_mapper(
            required_context: RequiredContextDescription,
        ) -> UserProvidedContext:
            required_context_name = required_context.context_name
            context_value: Union[IdentifierInput, TargetClassInput]
            if required_context_name == _ContextNames.ML_MODEL_VERSION.value:
                context_value = IdentifierInput(value=model_version_id)
            elif required_context_name == _ContextNames.SUBSET.value:
                context_value = IdentifierInput(value=subset_id)
            elif required_context.context_type["title"] == _TARGET_CLASS_NAME:
                if target_class is None:
                    raise ValueError("Pipeline requires a target class to be set")
                context_value = TargetClassInput(value=target_class)
            else:
                raise ValueError(
                    f"Unknown context type '{required_context.context_type['title']}' required "
                    f"under context name {required_context_name}"
                )
            return UserProvidedContext(
                pipeline_node_id=required_context.pipeline_node_id,
                context_name=required_context.context_name,
                value=context_value,
            )

        context = map(required_context_to_context_mapper, required_context)
        pipeline_response = await PipelineRunsAPI(self._api_service).run_pipeline(
            self.id, context=list(context)
        )
        return PipelineRun(self._api_service, pipeline_response)

    @classmethod
    async def get_by_name(cls, name: str) -> "Pipeline":
        api_service = get_api_client()
        pipeline_response_list = await PipelinesAPI(api_service).get_all()
        try:
            (pipeline_response,) = [
                pipeline_response
                for pipeline_response in pipeline_response_list
                if pipeline_response.name == name
            ]
        except ValueError as wrong_entry_number:
            available_names = ", ".join(
                pipeline_response.name for pipeline_response in pipeline_response_list
            )
            raise ResourceWithNameNotFoundError(
                f"Pipeline with name '{name}' not found."
                f"Existing pipeline names: '[{available_names}]'."
            ) from wrong_entry_number
        # This refetch is required since get_all call returns only partial results.
        # Specifically, the required_context returned on the GET /pipelines/ endpoint is [].
        return await cls.get_by_id(pipeline_response.id)


class Report:
    def __init__(self, api_service: HTTPService, tabular_report: TabularReport) -> None:
        self._api_service = api_service
        self._tabular_report = tabular_report

    @classmethod
    async def get_by_pipeline_run_id(
        cls: Type["Report"], pipeline_run_id: int
    ) -> "Report":
        api_service = get_api_client()
        tabular_report = await PipelineRunsAPI(api_service).get_report(pipeline_run_id)
        return cls(api_service=api_service, tabular_report=tabular_report)

    @property
    def table(self) -> str:
        return tabulate(
            (
                [row.method.method_name, row.metric.method_name, row.metric_value]
                for row in self._tabular_report.rows
            ),
            headers=["Method", "Metric", "Value"],
        )

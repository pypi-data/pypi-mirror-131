from aidkit_client.aidkit_api import HTTPService
from aidkit_client.endpoints.ml_models import MLModelsAPI
from aidkit_client.endpoints.pipeline_runs import PipelineRunsAPI


class Aidkit:
    models: MLModelsAPI

    def __init__(self, api_client: HTTPService):
        self.models = MLModelsAPI(api_client)
        self.pipeline_runs = PipelineRunsAPI(api_client)

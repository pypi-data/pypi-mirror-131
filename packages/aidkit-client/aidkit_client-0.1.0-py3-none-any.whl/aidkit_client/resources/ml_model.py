import io
from typing import Any

from aidkit_client.aidkit_api import HTTPService
from aidkit_client.configuration import get_api_client
from aidkit_client.endpoints.ml_models import MLModelsAPI
from aidkit_client.endpoints.models import MLModelVersionResponse


def _model_to_bytes(model: Any) -> bytes:
    if isinstance(model, str):
        with open(model, "rb") as model_file:
            return model_file.read()
    try:
        # we do not require tensorflow - which in turn requires
        # h5py. _But_ if a user has tensorflow installed and hands over a
        # tensorflow model, we want to be able to serialize it.
        import h5py  # pylint: disable=import-outside-toplevel
        import tensorflow as tf  # pylint: disable=import-outside-toplevel

        if isinstance(model, tf.keras.Model):
            bio = io.BytesIO()
            with h5py.File(bio, "w") as file:
                model.save(file)
            return bio.getvalue()
    except ImportError:
        pass
    raise ValueError(f"ML Model type {type(model)} not understood.")


class MLModelVersion:
    def __init__(
        self, api_service: HTTPService, model_version_response: MLModelVersionResponse
    ) -> None:
        self._api_service = api_service
        self._model_version_response = model_version_response

    @classmethod
    async def upload(
        cls,
        model_name: str,
        model_version: str,
        ml_model_file: Any,
    ) -> "MLModelVersion":
        api_service = get_api_client()
        model_bytes = _model_to_bytes(ml_model_file)
        model_version_response = await MLModelsAPI(api_service).upload_model_version(
            model_name=model_name,
            model_version=model_version,
            model_file_content=model_bytes,
        )
        return MLModelVersion(
            api_service=api_service, model_version_response=model_version_response
        )

    @property
    def id(self) -> int:
        return self._model_version_response.id

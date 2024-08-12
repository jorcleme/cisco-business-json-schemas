import json
import requests
import jsonschema.exceptions
import logging
from jsonschema import validate
from typing import Literal, List, Dict
from referencing import Registry, Resource
from pathlib import Path

SCHEMA_DIR = Path(__file__).parent.parent / "schemas"
DATA_DIR = Path(__file__).parent.parent / "data"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SchemaValidator:
    LOGGING_PROPERTIES: Dict[str, List[str]] = {
        "Article": ["title", "document_id", "url", "series"],
        "Video": ["title", "video_id", "url", "series"],
    }

    def __init__(
        self, schema_path: str, data_path: str, type: Literal["Article", "Video"]
    ):
        self.schema = json.loads(open(schema_path).read())
        self.data = json.loads(open(data_path).read())
        self._type = type
        self.logging_props = self.resolve_logging_properties()
        self.registry = Registry(retrieve=self.retrieve_via_http)

    def retrieve_via_http(uri: str):
        res = requests.get(uri)
        return Resource.from_contents(res.json())

    def resolve_logging_properties(self):
        return self.LOGGING_PROPERTIES.get(self._type, [])

    def validate(self):
        for asset in self.data:
            what = {k: asset.get(k, None) for k in self.logging_props}
            try:
                validate(instance=asset, schema=self.schema)
                logger.info(f"Validated {what.get('title', 'Unknown')}")
            except jsonschema.exceptions.ValidationError as e:
                logger.error("Validation failed")
                props = {k: asset.get(k, None) for k in self.logging_props}
                props["path"] = f"{e.absolute_schema_path}"
                props["reason"] = f"{e}"
                logger.error(f"{' '.join([f'{k}: {v}' for k, v in props.items()])}")


def make_validators(l: list[tuple[str, str, str]]):
    validators = []
    for t in l:
        data, schema, name = t
        validators.append(
            SchemaValidator(schema_path=schema, data_path=data, type=name)
        )
    return validators


def run_validators(validators: List[SchemaValidator]):
    for v in validators:
        v.validate()


def run():
    articles_data_path = DATA_DIR / "articles_schema.json"
    videos_data_path = DATA_DIR / "youtube_videos.json"
    articles_schema_path = SCHEMA_DIR / "articles" / "articles.json"
    videos_schema_path = SCHEMA_DIR / "videos" / "videos.json"
    articles = (articles_data_path, articles_schema_path, "Article")
    videos = (videos_data_path, videos_schema_path, "Video")
    validators = make_validators([articles, videos])
    run_validators(validators)


if __name__ == "__main__":
    run()

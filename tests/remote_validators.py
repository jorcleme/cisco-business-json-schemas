import json
import jsonschema
from jsonschema import validate
import jsonschema.exceptions
from referencing import Registry, Resource
import logging
import requests
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VIDEO_DATA_PATH = Path.joinpath(Path.cwd(), "data", "youtube_videos.json")
ARTICLE_DATA_PATH = Path.cwd() / "data" / "articles_schema.json"

VIDEO_SCHEMA_URL = (
    "https://jorcleme.github.io/cisco-business-json-schemas/schemas/videos/videos.json"
)
ARTICLE_SCHEMA_URL = "https://jorcleme.github.io/cisco-business-json-schemas/schemas/articles/articles.json"

# Fetch the schema contents from the URLs
video_schema = requests.get(VIDEO_SCHEMA_URL).json()
article_schema = requests.get(ARTICLE_SCHEMA_URL).json()

# Load and register the schemas
registry = Registry().with_resources(
    [
        ("video", Resource.from_contents(video_schema)),
        ("article", Resource.from_contents(article_schema)),
    ]
)


# Load data
with open(VIDEO_DATA_PATH) as f:
    video_data = json.load(f) or []

with open(ARTICLE_DATA_PATH) as f:
    article_data = json.load(f) or []

# Validate video data
for video in video_data:
    try:
        validate(instance=video, schema=video_schema, registry=registry)
        logger.info(
            f"Validation Successful for video id: {video.get('video_id', None)}"
        )
    except jsonschema.exceptions.ValidationError as e:
        logger.error(f"Validation failed for video id: {video.get('video_id', None)}")

# Validate article data
for article in article_data:
    try:
        validate(instance=article, schema=article_schema, resolver=registry)
        logger.info(
            f"Validation Successful for article document id: {article.get('document_id', None)}"
        )
    except jsonschema.exceptions.ValidationError as e:
        logger.error(
            f"Validation failed for article document id: {article.get('document_id', None)}"
        )

###########

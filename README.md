# cisco-business-json-schemas

---

This repo contains JSON Schemas for Cisco Business resources, specifically videos and articles. These schemas are designed to ensure consistency and correctness across various video and article-related data used within Cisco's Small Business Dev Team.

| Schema Name                   | Schema ID                                                                               | Version | Title                         | Description                                                                                                              |
| ----------------------------- | --------------------------------------------------------------------------------------- | ------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Cisco Business Video Schema   | <https://jorcleme.github.io/cisco-business-json-schemas/schemas/videos/videos.json>     | 1.0.0   | Cisco Business Video Schema   | A JSON Schema to validate the structure of video data, ensuring that all fields are correctly formatted and populated.   |
| Cisco Business Article Schema | <https://jorcleme.github.io/cisco-business-json-schemas/schemas/articles/articles.json> | 1.0.0   | Cisco Business Article Schema | A JSON Schema to validate the structure of article data, ensuring that all fields are correctly formatted and populated. |

## How to use it

```bash
pip install jsonschema referencing
```

```python
import json
import jsonschema
from jsonschema import validate, RefResolver
from referencing import Registry, Resource
```

Assume you are scraping videos or articles and need to verify each against the schema

```python
# Schema URLs
VIDEO_SCHEMA_URL = "https://jorcleme.github.io/cisco-business-json-schemas/schemas/videos/videos.json"
ARTICLE_SCHEMA_URL = "https://jorcleme.github.io/cisco-business-json-schemas/schemas/articles/articles.json"

# Load and register the schemas
registry = Registry().with_resources(
    [
        ("video", Resource.from_contents(video_schema)),
        ("article", Resource.from_contents(article_schema)),
    ]
)
```

**Scrape Data**
Imagine you've scraped JSON data for videos and articles. You would now validate this data against the appropriate schema.

```python
# Example scraped video data
video_data = {
    "title": "Cisco Tech Talk: Radius and Duo Authentication on a C1200 or C1300 Switch Part 2",
    "published_date": "2024-05-16T15:11:42Z",
    "description": "In this second, of a two-part edition of Cisco Tech Talk...",
    "url": "https://www.youtube.com/embed/TSSFAraDSRM",
    "video_id": "TSSFAraDSRM",
    "views": 1308,
    "likes": 12,
    "duration": "PT3M48S",
    "comments": 0,
    "kind": "youtube",
    "tags": ["c1200", "c1300", "catalyst", "cisco small business"],
    "transcript": "Welcome back in this second of a two-part episode of Cisco tech talk...",
    "category": "Configuration",
    "series": "Cisco Catalyst 1200 Series Switches"
}

# Example scraped article data
article_data = {
    "series": "Cisco Business 220 Series Smart Switches",
    "title": "Configure SNMP Communities on a CBS220 Series Switch",
    "document_id": "1633639132343299",
    "category": "Configuration",
    "steps": [
        {
            "section": "Configure SNMP Community on a Switch",
            "step_number": 1,
            "text": "Log in to the web user interface (UI) of your switch."
        }
    ],
    "type": "Article"
}
```

**Validate Data**
Use `validate` with the custom `registry` to validate the scraped data against the registered schemas

```python
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
```

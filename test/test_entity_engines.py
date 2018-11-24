from sse.core.entity_engines import extract_entity
import pytest


@pytest.mark.skip
def test_extract_entity(api_key):
    json = {
        "documents": [
            {
                "id": "1",
                "language": "en",
                "text": "This aspirin will take your headaches!",
            },
        ]
    }

    expected = {
        'documents': [{
            'entities': [{
                'bingId': '0eed091f-0505-0f21-6172-0a205da372a4',
                'matches': [{
                    'length': 7,
                    'offset': 5,
                    'text': 'aspirin',
                }],
                'name': 'Aspirin',
                'wikipediaId': 'Aspirin',
                'wikipediaLanguage': 'en',
                'wikipediaUrl': 'https://en.wikipedia.org/wiki/Aspirin',
            }],
            'id': '1',
        }],
        'errors': [],
    }

    assert expected == extract_entity(json, api_key)

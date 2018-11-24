import copy
import requests


DEFAULT_ENDPOINT_URL = "https://westeurope.api.cognitive.microsoft.com/text/analytics/v2.0/entities"
DEFAULT_HEADERS = {
    'Content-Type': 'application/json',
}


def extract_entity(json, api_key=None, endpoint=None):
    """
    The function is extracting entity information (for the Hackaton, Azure is being used)

    Example of the call function to Cognitive API:

    >>> json = {
    ...     "documents": [
    ...         {
    ...             "id": "1",
    ...             "language": "en",
    ...             "text": "Microsoft released Windows 10",
    ...         },
    ...         {
    ...             "id": "2",
    ...             "language": "en",
    ...             "text": "Selenium-binding protein 1 [...].",
    ...         }
    ...     ]
    ... }
    >>> api_key = os.environ.get('AZURE_COGNITIVE_API_KEY')
    >>> endpoint = "https://westeurope.api.cognitive.microsoft.com/text/analytics/v2.0/entities"
    >>> extract_entity(json, api_key=api_key, endpoint=endpoint)
    """
    assert api_key is not None

    if endpoint is None:
        endpoint = DEFAULT_ENDPOINT_URL

    headers = DEFAULT_HEADERS.copy()
    headers.update({
        'Ocp-Apim-Subscription-Key': api_key,
    })

    response = requests.post(endpoint, headers=headers, json=json)
    response.raise_for_status()

    return response.json()

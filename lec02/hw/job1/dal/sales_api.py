import os
import requests
from typing import List, Dict, Any

API_URL = 'https://fake-api-vycpfa6oca-uc.a.run.app/sales'
API_AUTH_TOKEN = os.environ.get("API_AUTH_TOKEN")


def get_sales(date: str, page: int) -> List[Dict[str, Any]]:
    """
    Get data from sales API for specified date.

    :param date: date to retrieve the data from
    :param page: page number
    :return: list of records
    """

    if not API_AUTH_TOKEN:
        print("AUTH_TOKEN environment variable must be set")

    headers = {
        "Authorization": API_AUTH_TOKEN,
    }
    params = {
        "date": date,
        "page": page
    }
    response = requests.get(
        API_URL,
        headers=headers,
        params=params)

    if response.status_code == 404:
        return []

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from API, error: {response.status_code}, {response.text}")

    response_json = response.json()

    return response_json

import os
from typing import Any

import requests
import json


def scrape_linkedin_profile(linkedin_profile_url: str):
    """scrape information from LinkedIn profile,
    Manually scrape the information from LinkedIn profile"""

    # To support local development, we first attempt to load data from local file to save api call cost each time
    json_data = _get_profile_data_from_file()

    # If no data found locally in json file then attempt to load data
    if json_data is None:
        print("Loading data from proxycurl api")
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}

        response = requests.get(
            api_endpoint,
            params={"linkedin_profile_url": linkedin_profile_url},
            headers=header_dic,
        )

        json_data = response.json()

    # Some cleanup to remove empty or not wanted data
    return _clean_response(json_data)


def _clean_response(response: dict) -> dict:
    # Removing unnecessary empty notes
    data = {
        k: v
        for k, v in response.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }

    # Remove groups pic url
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


def _get_profile_data_from_file() -> Any:
    file_name = os.path.join(os.getcwd(), "third_parties/linkedin_data.json")

    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        print("Loading data from file >> skipping api call")
        with open(file_name, "r") as file:
            data = file.read()

        return json.loads(data)

    print(
        "The static file do not exist at path: third_parties/linkedin_data.json. In case you want to avoid http calls"
        "please store the json response in static file at third_parties/linkedin_data.json"
    )

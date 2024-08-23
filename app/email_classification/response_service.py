import logging
import os

import requests


class ResponseService:
    def __init__(self):
        self.angelos_api_key = os.getenv("")
        self.angelos_url = os.getenv("ANGELOS_URI")
        self.port = os.getenv("ANGELOS_PORT")
        self.api_url = os.getenv("ANGELOS_URI")
        self.headers = {
            # "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_response(self, payload):
        url = f"{self.api_url}"
        try:
            logging.info(f"Sending POST request to {url}")
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
            logging.info(f"Successfully sent request. Status Code: {response.status_code}")
            return response.json()  # Assuming the response is JSON and needs to be returned
        except requests.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            raise
        except Exception as err:
            logging.error(f"An error occurred: {err}")
            raise

import logging

import requests

from app.common.environment import config


class ResponseService:
    def __init__(self):
        self.angelos_api_key = config.ANGELOS_API_KEY
        self.angelos_url = config.ANGELOS_URI
        self.port = config.ANGELOS_PORT
        self.api_url = f"{self.angelos_url}:{self.port}/api/v1/question/ask"
        self.session = requests.Session()
        self.headers = {
            # "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_response(self, payload):
        url = f"{self.api_url}"
        try:
            logging.info(f"Sending POST request to {url}")
            response = self.session.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            logging.info(f"Successfully sent request. Status Code: {response.status_code}")
            return response.json()
        except requests.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            raise
        except Exception as err:
            logging.error(f"An error occurred: {err}")
            raise

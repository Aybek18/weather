from dataclasses import dataclass
from typing import Optional

import requests
from rest_framework.exceptions import ParseError, NotFound


class BaseWeatherIntegration:
    def __init__(self, base_url: str, timeout: int, api_key: str, ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.api_key = api_key

    def _get(self, url: str, query_params: Optional[dict] = None, timeout: Optional[int] = None, ) -> requests.Response:
        try:
            response = requests.get(url=url, params=query_params, timeout=timeout)
            if response.ok:
                return response
            raise NotFound()
        except requests.ConnectionError:
            raise ParseError()

    @classmethod
    def factory(cls, *args, **kwargs):
        return cls(*args, **kwargs)

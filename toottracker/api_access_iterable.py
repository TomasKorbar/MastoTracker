import requests
import re

from .api_access_exception import ApiAccessException


class ApiAccessIterable:
    next_link_re = re.compile(r'<(.*)>; rel="next"')

    def __init__(self, api_url):
        self._api_url = api_url

    def __iter__(self):
        return self

    def __next__(self):
        if not self._api_url:
            raise StopIteration
        response = requests.get(self._api_url)
        if response.status_code != 200:
            raise ApiAccessException(response.status_code,
                                     f"Error encountered while trying to proceed with pagination",
                                     response.json().get("error", None))
        next = re.search(ApiAccessIterable.next_link_re,
                         response.headers.get("Link", ""))
        self._api_url = next.group(1) if next else None
        return response.json()

"""
common_errors.py

Created by Ashish Patel on 14-12-2021
Copyright Ashish Patel, 2021

"""

import requests
import logging
from requests import Request
import ashishdotme_utils_lib.errors.common_errors as ae


class DashboardClient(object):
    """
    Dashboard API methods
    """

    def __init__(
            self
    ):
        self.endpoint = "https://systemapi.prod.ashish.me/"

    def get_data(self, request=None, params=None):
        full_url = "%s%s" % (self.endpoint, request)
        r = requests.get(url=full_url)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.exception(f"Exception while fetching {request}")
        return r.json()
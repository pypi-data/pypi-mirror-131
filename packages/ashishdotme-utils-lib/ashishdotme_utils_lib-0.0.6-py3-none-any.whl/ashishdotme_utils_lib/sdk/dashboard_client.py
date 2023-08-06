"""
common_errors.py

Created by Ashish Patel on 14-12-2021
Copyright Ashish Patel, 2021

"""

import requests
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
            error_handler(self, r)
        return r.json()


def error_handler(zot, req):
    error_codes = {
        400: ae.UnsupportedParams,
        401: ae.UserNotAuthorised,
        403: ae.UserNotAuthorised,
        404: ae.ResourceNotFound,
        409: ae.Conflict,
        412: ae.PreConditionFailed,
        413: ae.RequestEntityTooLarge,
        428: ae.PreConditionRequired,
        429: ae.TooManyRequests,
    }

    def err_msg(req):
        return "\nCode: %s\nURL: %s\nMethod: %s\nResponse: %s" % (
            req.status_code,
            # error.msg,
            req.url,
            req.request.method,
            req.text,
        )

    if error_codes.get(req.status_code):
        raise error_codes.get(req.status_code)(err_msg(req))
    else:
        raise ae.HTTPError(err_msg(req))


dashboardClient = DashboardClient()

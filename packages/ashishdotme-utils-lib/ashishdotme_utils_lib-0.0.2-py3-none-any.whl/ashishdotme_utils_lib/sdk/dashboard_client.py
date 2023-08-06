"""
common_errors.py

Created by Ashish Patel on 14-12-2021
Copyright Ashish Patel, 2021

"""


import requests
import ashishdotme_utils_lib.errors.common_errors as ze


class DashboardClient(object):
    """
    Dashboard API methods
    """

    def __init__(
            self
    ):
        """ Store Zotero credentials
        """
        self.endpoint = "https://systemapi.prod.ashish.me"

    def _retrieve_data(self, request=None, params=None):
        """
        Retrieve Zotero items via the API
        Combine endpoint and request to access the specific resource
        Returns a JSON document
        """
        full_url = "%s%s" % (self.endpoint, request)
        req = requests.get(
            url=full_url, headers=self.default_headers(), params=params
        )
        self.request.encoding = "utf-8"
        try:
            self.request.raise_for_status()
        except requests.exceptions.HTTPError:
            error_handler(self, self.request)
        return req.json()


def error_handler(zot, req):
    error_codes = {
        400: ze.UnsupportedParams,
        401: ze.UserNotAuthorised,
        403: ze.UserNotAuthorised,
        404: ze.ResourceNotFound,
        409: ze.Conflict,
        412: ze.PreConditionFailed,
        413: ze.RequestEntityTooLarge,
        428: ze.PreConditionRequired,
        429: ze.TooManyRequests,
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
        raise ze.HTTPError(err_msg(req))

dashboardClient = DashboardClient()
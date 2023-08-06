import requests

class Dashboard(object):
  
    """
    Dashboard API methods
    """

    def __init__(
        self,
        library_id=None,
        library_type=None,
        api_key=None,
        preserve_json_order=False,
        locale="en-US",
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

        # The API doesn't return this any more, so we have to cheat
        self.self_link = request

        # ensure that we wait if there's an active backoff
        self._check_backoff()
        self.request = requests.get(
            url=full_url, headers=self.default_headers(), params=params
        )
        self.request.encoding = "utf-8"
        try:
            self.request.raise_for_status()
        except requests.exceptions.HTTPError:
            error_handler(self, self.request)
        backoff = self.request.headers.get("backoff")
        if backoff:
            self._set_backoff(backoff)
        return self.request


def error_handler(zot, req):
    """ Error handler for HTTP requests
    """
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
        """ Return a nicely-formatted error message
        """
        return "\nCode: %s\nURL: %s\nMethod: %s\nResponse: %s" % (
            req.status_code,
            # error.msg,
            req.url,
            req.request.method,
            req.text,
        )

    if error_codes.get(req.status_code):
        # check to see whether its 429
        if req.status_code == 429:
            # try to get backoff duration
            delay = req.headers.get("backoff")
            if not delay:
                raise ze.TooManyRetries(
                    "You are being rate-limited and no backoff duration has been received from the server. Try again later"
                )
            else:
                zot._set_backoff(delay)
        else:
            raise error_codes.get(req.status_code)(err_msg(req))
    else:
        raise ze.HTTPError(err_msg(req))
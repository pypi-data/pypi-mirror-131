#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
common_errors.py

Created by Ashish Patel on 14-12-2021
Copyright Ashish Patel, 2021

"""


# Define some exceptions
class AError(Exception):
    """ Generic parent exception
    """
    pass


class ParamNotPassed(AError):
    """ Raised if a parameter which is required isn't passed
    """
    pass


class CallDoesNotExist(AError):
    """ Raised if the specified API call doesn't exist
    """
    pass


class UnsupportedParams(AError):
    """ Raised when unsupported parameters are passed
    """
    pass


class UserNotAuthorised(AError):
    """ Raised when the user is not allowed to retrieve the resource
    """
    pass


class TooManyItems(AError):
    """ Raised when too many items are passed to a Write API method
    """
    pass


class MissingCredentials(AError):
    """
    Raised when an attempt is made to create a Zotero instance
    without providing both the user ID and the user key
    """
    pass


class InvalidItemFields(AError):
    """ Raised when an attempt is made to create/update items w/invalid fields
    """
    pass


class ResourceNotFound(AError):
    """ Raised when a resource (item, collection etc.) could not be found
    """
    pass


class HTTPError(AError):
    """ Raised for miscellaneous URLLib errors
    """
    pass


class CouldNotReachURL(AError):
    """ Raised when we can't reach a URL
    """
    pass


class Conflict(AError):
    """ 409 - Raised when the target library is locked
    """
    pass


class PreConditionFailed(AError):
    """
    412 - Raised when the provided X-Zotero-Write-Token has already been
    submitted
    """
    pass


class RequestEntityTooLarge(AError):
    """
    413 – The upload would exceed the storage quota of the library owner.
    """
    pass


class PreConditionRequired(AError):
    """
    428 - Raised when If-Match or If-None-Match was not provided.
    """
    pass


class TooManyRequests(AError):
    """
    429 - Raised when Too many unfinished uploads.
    Try again after the number of seconds specified in the Retry-After header.
    """
    pass


class FileDoesNotExist(AError):
    """
    Raised when a file path to be attached can't be opened (or doesn't exist)
    """
    pass


class TooManyRetries(AError):
    """
    Raise after the backoff period for new requests exceeds 32s
    """
    pass
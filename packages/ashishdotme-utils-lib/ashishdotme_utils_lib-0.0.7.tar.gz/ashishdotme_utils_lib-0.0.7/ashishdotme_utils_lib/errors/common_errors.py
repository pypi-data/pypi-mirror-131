#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
common_errors.py

Created by Ashish Patel on 14-12-2021
Copyright Ashish Patel, 2021

"""


class AError(Exception):
    """ Generic parent exception
    """
    pass


class ParamNotPassed(AError):
    """ Raised if a parameter which is required isn't passed
    """
    pass
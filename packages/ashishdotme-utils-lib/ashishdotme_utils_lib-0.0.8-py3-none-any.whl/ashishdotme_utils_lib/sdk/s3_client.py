#!/usr/bin/env python3

import logging


def upload_file(bucket, key, filename):
    logging.info(f"Uploading File {filename} to {key}")
    try:
        bucket.upload_file(filename, key)
    except Exception as err:
        logging.exception(f"Exception uploading file: {err}")
        raise
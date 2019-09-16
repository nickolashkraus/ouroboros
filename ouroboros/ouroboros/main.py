# -*- coding: utf-8 -*-
"""Main AWS Lambda function module."""


def handler(event: dict, context: object) -> dict:
    """
    Handle AWS Lambda function event.

    :param event: event data
    :type event: dict
    :param context: runtime information of the AWS Lambda function
    :type context: LambdaContext object
    """
    return 'Hello, World!'

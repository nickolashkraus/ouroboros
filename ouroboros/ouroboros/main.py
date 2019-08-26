# -*- coding: utf-8 -*-

"""Main module."""


def handler(event: dict, context: object) -> dict:
    """
    Handler of AWS Lambda function.

    :param event: event data
    :type event: dict
    :param context: runtime information of the AWS Lambda function
    :type context: LambdaContext object
    """

    return 'Hello, World!'

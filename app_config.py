#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import logging


PRODUCTION_S3_BUCKET = 'apps.npr.org'
STAGING_S3_BUCKET = 'stage-apps.npr.org'
DEFAULT_MAX_AGE = 20

"""
Logging
"""
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(levelname)s:%(name)s:%(asctime)s: %(message)s'


def configure_targets(deployment_target):
    """
    Configure deployment targets. Abstracted so this can be
    overriden for rendering before deployment.
    """
    global S3_BUCKET
    global LOG_LEVEL
    global DEPLOYMENT_TARGET

    if deployment_target == 'production':
        S3_BUCKET = PRODUCTION_S3_BUCKET
        LOG_LEVEL = logging.WARNING
    elif deployment_target == 'staging':
        S3_BUCKET = STAGING_S3_BUCKET
        LOG_LEVEL = logging.DEBUG
    else:
        S3_BUCKET = None

    DEPLOYMENT_TARGET = deployment_target

#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from fabric.api import task, local, require
from fabric.state import env
import os
import shutil
import gzip
import tempfile
from termcolor import colored

import flat
import app_config
import utils
import logging


logging.basicConfig(format=app_config.LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(app_config.LOG_LEVEL)

"""
Environments

Changing environment requires a full-stack test.
An environment points to both a server and an S3
bucket.
"""


@task
def production():
    """
    Run as though on production.
    """
    env.settings = 'production'
    app_config.configure_targets(env.settings)


@task
def staging():
    """
    Run as though on staging.
    """
    env.settings = 'staging'
    app_config.configure_targets(env.settings)


@task
def deploy(path, slug=None):
    """
    manual deploy parts of a project that needs fixing
    """
    require('settings', provided_by=[production, staging])

    if not slug:
        slug = path

    utils.confirm(
        colored("You are trying to override parts of %s project in %s.\n"
                "Do you know what you're doing?" % (slug, env.settings), "red")
    )

    flat.deploy_folder(
        app_config.S3_BUCKET,
        path,
        slug,
        headers={
            'Cache-Control': 'max-age=%i' % app_config.DEFAULT_MAX_AGE
        }
    )


@task
def download(prefix):
    """
    downloads an s3 prefix and uncompresses gzip files recursively
    """
    GZIP_FILE_TYPES = ['.html', '.js', '.json', '.css', '.xml']
    require('settings', provided_by=[production, staging])
    if os.path.isdir(prefix):
        shutil.rmtree(prefix)

    # Sync S3 prefix files to tmp folder
    local('aws s3 sync s3://%s/%s %s' % (app_config.S3_BUCKET,
                                         prefix,
                                         prefix))

    for local_path, subdirs, filenames in os.walk(prefix, topdown=True):
        for name in filenames:
            src_path = os.path.join(local_path, name)
            logger.info(src_path)
            if os.path.splitext(src_path)[1].lower() in GZIP_FILE_TYPES:
                with tempfile.TemporaryFile() as temp:
                    try:
                        with gzip.open(src_path, 'rb') as f:
                            file_content = f.read()
                            temp.write(file_content)
                        temp.seek(0)
                        with open(src_path, 'wb') as fout:
                            fout.write(temp.read())
                    except IOError:
                        pass
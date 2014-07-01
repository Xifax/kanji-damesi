#!/usr/bin/env python

from fabric.api import local, shell_env, abort
try:
    from deploy.env import variables
except ImportError:
    abort('Cannot import environment variables from deploy/env.py')


def build():
    """Build static assets"""
    local('cd client && ./node_modules/.bin/grunt build')


def collect():
    """Collect static assets"""

    # Enable development environment (pass dict as kwargs)
    with shell_env(**variables):
        # Upload assets
        result = local('./manage.py collectstatic --noinput', capture=True)
        if result.failed:
            abort('Could not upload static assets to Amazon S3')


def commit():
    """Commit newest build"""
    local('git add -p && git commit')


def push():
    """Push to Dokku"""
    local('git push dokku master')


def deploy():
    """Build and deploy to Dokku"""
    build()
    collect()
    commit()
    push()

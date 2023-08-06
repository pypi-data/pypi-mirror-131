#!/usr/bin/env python

from setuptools import setup

# This setup is suitable for "python setup.py develop".

setup(
        name='awsneo',
        version='0.0.1',
        description='Library for python 3 that allows you to connect to different database engines (PostgreSQL, MySQL, MSSQL) through secrets manager (secret values) or direct connection, also allows you to execute queries from scripts in buckets or directly as a single query',
        author='Juan Rueda',
        author_email='Juan.Rueda@btgpactual.com',
        packages=['awsneo'],
        download_url='https://github.com/jprugo/awsneo/archive/refs/tags/0.0.1.tar.gz'
)
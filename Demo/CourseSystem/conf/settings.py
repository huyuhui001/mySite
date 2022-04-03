#!/usr/bin/env python3
# -*-coding:utf-8 -*-

#
# Configuration
#

import os

# Define the path to save data
# e.g.:
# BASE_PATH: /opt/myProject
# DB_PATH: /opt/myProject/db
# The os.path.join will automatically add '/' between two parameters

BASE_PATH = os.path.dirname(
    os.path.dirname(__file__)
)

DB_PATH = os.path.join(
    BASE_PATH, 'db'
)







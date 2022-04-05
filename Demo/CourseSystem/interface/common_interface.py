#!/usr/bin/env python3
# -*-coding:utf-8 -*-

#
# Common Interface
#

import os
from conf import settings


# Get all schools
def get_all_schools_interface():
    # Get path of saving school info
    school_dir = os.path.join(
        settings.DB_PATH, 'School'
    )

    # Check if school exists
    if not os.path.exists(school_dir):
        return False, "School does not exist, please contact with Admin"
    
    # If school exists, get school info
    school_list = os.listdir(school_dir)
    
    return True, school_list



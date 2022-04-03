#!/usr/bin/env python3
# -*-coding:utf-8 -*-

#
# Define CRUD to DB. Save object and get object
#

import os
import pickle
from conf import settings

# Save data to file
# File path structure: BASE_PATH/class_name/user_name (e.g., )
def save_data(obj):
    # Get class name
    # obj.__class__: get current obj's class
    # obj.__class__.__name__: get class' name
    class_name = obj.__class__.__name__
    
    # Consolidate full path for saving file
    user_dir_path = os.path.join(
        settings.DB_PATH, class_name
    )

    # If generated path does not exist, create it
    if not os.path.exists(user_dir_path):
        os.mkdir(user_dir_path)
    
    # Consolidate pinkle file path for current user, using username as filename
    user_path = os.path.join(
        user_dir_path, obj.usr
    )

    # Open file, save object. Pinkle file is binary file
    with open(user_path, 'wb') as f:
        pickle.dump(obj, f)


# Get data from file
def get_data(cls, usr):    
    # Get class name from cls
    class_name = cls.__name__

    # Consolidate full path for saving file
    user_dir_path = os.path.join(
        settings.DB_PATH, class_name
    )

    # Consolidate pinkle file path for current user, using username as filename
    user_path = os.path.join(
        user_dir_path, usr
    )

    # Check if file exists already. 
    # If file exists, open Pinkle file and load object, or return None
    if os.path.exists(user_path):
        with open(user_path, 'rb') as f:
            obj = pickle.load(f)
            return obj
    
    return None




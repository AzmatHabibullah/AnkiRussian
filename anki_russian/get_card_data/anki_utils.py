import os
import json
import pandas as pd

home_directory = os.getcwd() + "/00_own_projects/anki_russian/"


def read_file(relative_dir):
    if ".txt" in relative_dir:
        with open(home_directory + relative_dir, 'r') as file:
            return file
    elif ".xlsx" in relative_dir or ".xls" in relative_dir:
        return pd.read_excel(home_directory + relative_dir)
    elif ".json" in relative_dir:
        with open(home_directory + relative_dir, 'r') as file:
            return json.load(file)
    else:
        with open(home_directory + relative_dir, 'r') as file:
            return file
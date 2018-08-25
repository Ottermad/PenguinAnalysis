"""Responsible for importing csv data into database."""
import os


def import_data(path_to_csvs):
    """Read each csv file and adds to database."""
    list_of_filenames = os.listdir(path_to_csvs)

    for filename in list_of_filenames:
        # Open file
        with open(path_to_csvs + '/' + filename) as f:  # TODO: Refactor
            first_line = True
            for line in f.readlines():
                # Skip header
                if first_line:
                    first_line = False
                    continue
                # Create db object
                

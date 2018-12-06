"""Responsible for importing csv data into database."""
import os
from app.db.models import ImageClick, db

def create_click(user_name, subject_zooniverse_id, lunar_phase, original_size_x, original_size_y, path, temperature_f, tmstamp, animals_present, all_marked, mark_order, value, x, y):
    click = ImageClick(
        user_name=user_name,
        subject_zooniverse_id=subject_zooniverse_id,
        lunar_phase=lunar_phase,
        original_size_x=original_size_x,
        original_size_y=original_size_y,
        path=path,
        temperature_f=temperature_f,
        tmstamp=tmstamp,
        animals_present=animals_present,
        all_marked=all_marked,
        mark_order=mark_order,
        value=value,
        x=x,
        y=y
    )
    return click


def import_data(path_to_csvs):
    """Read each csv file and adds to database."""
    list_of_filenames = os.listdir(path_to_csvs)
    print(list_of_filenames)
    length = len(list_of_filenames)
    c = 0
    for filename in list_of_filenames:
        # Open file
        clicks = []
        data_source = []
        with open(path_to_csvs + '/' + filename) as f:  # TODO: Refactor
            first_line = True
            print("Opened file {}".format(filename))
            for line in f.readlines():
                # Skip header
                if first_line:
                    first_line = False
                    continue
                # Create db object
                split_row = line.strip("\n").strip(" ").strip(",").split(",")
                data_source.append(split_row)
                # try:
                #     # click = create_click(*split_row)
                #     # clicks.append(click)
                # except Exception as e:
                #     print(e)
                #     print(line)
                #     print(line.strip("\n").strip(","))
                #     print(split_row)
                #     break
            with db.atomic():
                for idx in range(0, len(data_source), 50):
                    ImageClick.insert_many(data_source[idx:idx+50], fields=[
                        ImageClick.user_name,
                        ImageClick.subject_zooniverse_id,
                        ImageClick.lunar_phase,
                        ImageClick.original_size_x,
                        ImageClick.original_size_y,
                        ImageClick.path,
                        ImageClick.temperature_f,
                        ImageClick.tmstamp,
                        ImageClick.animals_present,
                        ImageClick.all_marked,
                        ImageClick.mark_order,
                        ImageClick.value,
                        ImageClick.x,
                        ImageClick.y
                    ]).execute()
            c += 1
            print("Done {} out of {}".format(c, length))

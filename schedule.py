import yaml

file_path = './_data/schedule.yaml'

try:
    with open(file_path, 'r') as f:
        schedule = yaml.load(f)
except yaml.YAMLError as ex:
    print('Error with yaml file loading')


def get_track(title):
    for track in schedule:
        if track['name'] == title:
            return track


def get_all():
    return schedule

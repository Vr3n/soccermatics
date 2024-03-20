import pathlib
import os
import pandas as pd
import json

def get_data(*args):
    path = os.path.join(str(pathlib.Path().resolve()), *args)

    with open(path) as f:
        data = json.load(f)

    return data


df_competitions = pd.DataFrame(get_data('data', 'Wyscout', 'competitions.json'))
df_matches = pd.DataFrame(get_data('data', 'Wyscout', 'matches_England.json'))

df_matches.info()

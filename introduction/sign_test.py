import pandas as pd
import numpy as np
import json
from statsmodels.stats.descriptivestats import sign_test

import matplotlib.pyplot as plt

import os
import pathlib
import warnings


def get_data(*args):
    path = os.path.join(str(pathlib.Path().resolve()), *args)

    with open(path) as f:
        data = json.load(f)

    return data

pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

train = pd.DataFrame(get_data('data', 'Wyscout', 'events_England.json'))
player_df = pd.DataFrame(get_data('data', 'Wyscout', 'players.json'))

train.info()
player_df.info()


## keeping only shots of son.
shots = train.loc[train['subEventName'] == 'Shot']

# look for son's id.
son_id = player_df.loc[player_df['shortName'] == "Son Heung-Min"]['wyId'].iloc[0]

# filtering son's shots.
son_shots = shots.loc[shots['playerId'] == son_id]

# Left leg shots.
lefty_shots = son_shots.loc[son_shots.apply(lambda x: {'id': 401} in x.tags, axis=1)]

# Right leg shots.
righty_shots = son_shots.loc[son_shots.apply(lambda x: {'id': 402} in x.tags, axis=1)]

# Create list with ones for left foot shots and -1 for right foot shots.
l = [1] * len(lefty_shots)
l.extend([-1] * len(lefty_shots))


# Testing the hypothesis.
test = sign_test(l, mu0=0)
pvalue = test[1]

if pvalue < 0.05:
    print("P-value amounts to", str(pvalue)[:5], "- We reject the null hypothesis - Heung-Min Son is not ambidextrous")
else:
    print("P-value amounts to", str(pvalue)[:5], "- We fail to reject the null hypothesis - Heung-Min Son is ambidextrous")
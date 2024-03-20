import pandas as pd
import numpy as np
import json
# plotting
import matplotlib.pyplot as plt
from scipy.stats import ttest_1samp

#opening data
import os
import pathlib
import warnings
pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

def get_data(*args):
    path = os.path.join(str(pathlib.Path().resolve()), *args)

    with open(path) as f:
        data = json.load(f)

    return data

train = pd.DataFrame(get_data('data', 'Wyscout', 'events_England.json'))
teams_df = pd.DataFrame(get_data('data', 'Wyscout', 'teams.json'))
teams_df.rename(columns={"wyId": "teamId"}, inplace=True)

corners = train.loc[train['subEventName'] == "Corner"]
corners_by_team = corners.groupby(['teamId']).size().reset_index(name='counts')

summary = corners_by_team.merge(teams_df[['name', 'teamId']], how="left", on=["teamId"])

corners_by_game = corners.groupby(['teamId', "matchId"]).size().reset_index(name='counts')
summary_2 = corners_by_game.merge(teams_df[['name', 'teamId']], how="left", on=['teamId'])


team_name = "Manchester City"

city_corners = summary_2.loc[summary_2['name'] == team_name]['counts']


def format_figure(ax):
    ax.legend(loc="upper left")
    ax.set_ylim(0, 0.25)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylabel('')
    ax.set_xlabel('Corners')
    ax.set_ylabel('Proportion of games.')
    ax.set_xticks(np.arange(0, 21, step=1))


fig, ax1 = plt.subplots(1, 1)
ax1.hist(city_corners, np.arange(0.01, 20.5, 1), color='lightblue', edgecolor='white', linestyle='-', alpha=0.5,
                                label=team_name, density=True, align='right')
format_figure(ax1)

mean = city_corners.mean()
std = city_corners.std()
print('City typically had %.2f  plus/minus %.2f corners per match in the 2017/18 season.'%(mean,std))
plt.show()

t, pvalue = ttest_1samp(city_corners, popmean=6)

print("The t-staistic is %.2f and the P-value is %.2f."%(t,pvalue))
if pvalue < 0.05:
    print("We reject null hypothesis - " + team_name + " typically take more than 6 corners per match.")
else:
    print("We cannot reject null hypothesis - " + team_name + " do not typically take more than 6 corners per match.")
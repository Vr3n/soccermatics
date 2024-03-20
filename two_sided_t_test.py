import pandas as pd
import numpy as np
import json
# plotting
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

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

liverpool_corners = summary_2.loc[summary_2['name'] == "Liverpool"]['counts']
everton_corners = summary_2.loc[summary_2['name'] == "Everton"]['counts']


liv_mean = liverpool_corners.mean()
liv_std = liverpool_corners.std()
print('Liverpool typically had %.2f plus/minus %.2f corners per match in the 2017/18 season.'%(liv_mean,liv_std))
liv_std_error=liv_std/np.sqrt(len(liverpool_corners))
print('The standard error in the number of corners per match is %.4f'%liv_std_error)


def format_figure(ax):
    ax.legend(loc="upper left")
    ax.set_ylim(0, 0.25)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylabel('')
    ax.set_xlabel('Corners')
    ax.set_ylabel('Proportion of games.')
    ax.set_xticks(np.arange(0, 21, step=1))


mean = everton_corners.mean()
std = everton_corners.std()
print('Everton typically had %.2f plus/minus %.2f corners per match in the 2017/18 season.'%(mean,std))
std_error=std/np.sqrt(len(everton_corners))
print('The standard error in the number of corners per match is %.4f'%std_error)

t, pvalue  = ttest_ind(a=liverpool_corners, b=everton_corners, equal_var=True)

print("The t-staistic is %.2f and the P-value is %.2f."%(t,pvalue))
if pvalue < 0.05:
    print("We reject null hypothesis - Liverpool took different number of corners per game than Everton")
else:
    print("We cannot reject the null hypothesis that Liverpool took the same number of corners per game as Everton")

fig,ax=plt.subplots(1,1)
ax.hist(liverpool_corners, np.arange(0.01,15.5,1), color='red', edgecolor = 'white',linestyle='-',alpha=1.0, label="Liverpool", density=True,align='right')
ax.hist(everton_corners, np.arange(0.01,15.5,1), alpha=0.25, color='blue', edgecolor = 'black', label='Everton',  density=True,align='right')
format_figure(ax)
plt.show()
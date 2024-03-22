import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Pitch, Sbopen
import pandas as pd


# Opening the dataset.
parser = Sbopen()

df, related, freeze, tactics = parser.event(69301)

sub = df.loc[df['type_name'] == "Substitution"].loc[df['team_name'] == "England Women's"].iloc[0]['index']
mask_england = (df.type_name == "Pass") & (df.team_name == "England Women's") & (df.index < sub) & (df.outcome_name.isnull()) & (df.sub_type_name != "Throw-in")

df_pass = df.loc[mask_england, ['x', 'y', 'end_x', 'end_y', 'player_name', 'pass_recipient_name']]

df_pass['player_name'] = df_pass['player_name'].apply(lambda x: str(x).split()[-1])
df_pass['pass_recipient_name'] = df_pass['pass_recipient_name'].apply(lambda x: str(x).split()[-1])


scatter_df = pd.DataFrame()

for i, name in enumerate(df_pass['player_name'].unique()):
    pass_x = df_pass.loc[df_pass['player_name'] == name]['x'].to_numpy()
    rec_x = df_pass.loc[df_pass['pass_recipient_name'] == name]['end_x'].to_numpy()
    pass_y = df_pass.loc[df_pass['player_name'] == name]['y'].to_numpy()
    rec_y = df_pass.loc[df_pass['pass_recipient_name'] == name]['end_y'].to_numpy()

    scatter_df.at[i, 'player_name'] = name

    # Average passes.
    scatter_df.at[i, "x"] = np.mean(np.concatenate([pass_x, rec_x]))
    scatter_df.at[i, 'y'] = np.mean(np.concatenate([pass_y, rec_y]))

    scatter_df.at[i, 'no'] = df_pass.loc[df_pass['player_name'] == name].count().iloc[0]

scatter_df['marker_size'] = (scatter_df['no'] / scatter_df['no'].max() * 1500)

# Calculating Edges width.
df_pass['pair_key'] = df_pass.apply(lambda x: "_".join(sorted([x['player_name'], x['pass_recipient_name']])), axis=1)
lines_df = df_pass.groupby(['pair_key']).x.count().reset_index()
lines_df.rename({'x': 'pass_count'}, axis="columns", inplace=True)
lines_df = lines_df[lines_df['pass_count'] > 2]


# plotting vertices.
pitch = Pitch(line_color='#d4534a', pitch_color="#363131")
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)

pitch.scatter(scatter_df.x, scatter_df.y, s=scatter_df.marker_size, color='#5a9acc', edgecolors='#8496a3', linewidth=1, alpha=1, ax=ax["pitch"], zorder = 3)

# annotating player nmes.
for i, row in scatter_df.iterrows():
    pitch.annotate(row.player_name, xy=(row.x, row.y), c="#e6e6e6", va="center", ha='center', weight='bold', size=16, ax=ax['pitch'], zorder=4)

# plotting edges.
for i, row in lines_df.iterrows():
    player_1 = row['pair_key'].split("_")[0]
    player_2 = row['pair_key'].split("_")[1]

    player_1_x = scatter_df.loc[scatter_df['player_name'] == player_1]['x'].iloc[0]
    player_1_y = scatter_df.loc[scatter_df['player_name'] == player_1]['y'].iloc[0]
    player_2_x = scatter_df.loc[scatter_df['player_name'] == player_2]['x'].iloc[0]
    player_2_y = scatter_df.loc[scatter_df['player_name'] == player_2]['y'].iloc[0]

    num_passes = row['pass_count']

    line_width = (num_passes / lines_df['pass_count'].max() * 10)

    pitch.lines(player_1_x, player_1_y, player_2_x, player_2_y, alpha=1, lw=line_width, zorder=2, color="#406dd6", ax=ax['pitch'])

# Calculate the number of successful passes by player.
no_passes = df_pass.groupby(['player_name']).x.count().reset_index()
no_passes.rename({'x': 'pass_count'}, axis='columns', inplace=True)

# find one who made most passes.
max_no = no_passes['pass_count'].max()

# calculate the denominator - 10 * the total sum of passes.
denominator = 10 * no_passes['pass_count'].sum()

nominator = (max_no - no_passes['pass_count']).sum()

centralisation_index = nominator / denominator

print("Centralisation index is: ", centralisation_index)

fig.suptitle("Nodes location - England", fontsize=30)
plt.show()
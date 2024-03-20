import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Pitch, Sbopen


# Opening the dataset.
parser = Sbopen()

df, related, freeze, tactics = parser.event(69301)
passes = df.loc[df['type_name'] == "Pass"].loc[df['sub_type_name'] != 'Throw-in'].set_index('id')

mask_bronze = (df.type_name == "Pass") & (df.player_name == "Lucy Bronze")
df_pass = df.loc[mask_bronze, ['x', 'y', 'end_x', 'end_y']]

pitch = Pitch(line_color='#c25d4c', pitch_color='#242424')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)

pitch.arrows(df_pass.x, df_pass.y,
             df_pass.end_x, df_pass.end_y, color="#bfd5e0", ax=ax['pitch'])
pitch.scatter(df_pass.x, df_pass.y, alpha=0.2, s=500, color="#3689b5", ax=ax['pitch'])

fig.suptitle("Lucy Bronze passes against sweden", fontsize=30)

# prepare the dataframe of passes by England that were no-throw ins.
mask_england = (df.type_name == "Pass") & (df.team_name == "England Women's") & (df.sub_type_name != "Throw-in")
df_passes = df.loc[mask_england, ['x', 'y', 'end_x', 'end_y', 'player_name']]

names = df_passes['player_name'].unique()

# draw 4x4 Pitches.
pitch = Pitch(line_color='#c25d4c', pitch_color='#242424')
fig, axs = pitch.grid(ncols=4, nrows=4, grid_height=0.85,
                      title_height=0.06, axis=False, endnote_height=0.04,
                      title_space=0.04, endnote_space=0.01)

# plotting each player.
for name, ax in zip(names, axs['pitch'].flat[:len(names)]):
    ax.text(60, -10, name, ha='center', va='center', fontsize=14)

    player_df = df_passes.loc[df_passes['player_name'] == name]

    pitch.scatter(player_df.x, player_df.y, alpha=0.2, s=50, color="#3689b5", ax=ax)
    pitch.arrows(player_df.x, player_df.y,
                 player_df.end_x, player_df.end_y, color="white", ax=ax, width=1)


for ax in axs['pitch'][-1, 16 - len(names):]:
    ax.remove()

axs['title'].text(0.5, 0.5, 'England passes against Sweden', ha='center', va='center', fontsize=30)

plt.show()
## Challenge

# 1. Create a dataframe of passes which contains all the passes in the match.
# 2. Plot the start point of every sweden pass. Attacking left to right.
# 3. Plot only passes made by Caroline Seger (she is Sara Caroline Seger in the database.)
# 4. Plot arrows to show where the passes went to.

import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Pitch, Sbopen, VerticalPitch

# Opening the dataset.
parser = Sbopen()

df, related, freeze, tactics = parser.event(69301)

## get team names.
team1, team2 = df.team_name.unique()

# Dataframe of passes.
passes = df.loc[df['type_name'] == "Pass"].set_index('id')

pitch = Pitch(line_color="#c25d4c", pitch_color="#2e2d2d")
fig, ax = pitch.grid(
                grid_height=0.9, title_height=0.06, axis=False,
                endnote_height=0.04, title_space=0, endnote_space=0
)

pitchLengthX = 120
pitchWidthY = 80

mask_sweden = (df.type_name == "Pass") & (df.team_name == team2) & (df.player_name == "Sara Caroline Seger")
df_sweden = df.loc[mask_sweden, ['x', 'y', 'end_x', 'end_y','outcome_name', 'player_name', 'pass_angle', 'pass_length']]

for i, row in df_sweden.iterrows():
    if row['outcome_name'] == "Incomplete" or row['outcome_name'] == "Out":
        pitch.scatter(120 - row.x, 80 - row.y, s=100, color="#427bad", ax=ax['pitch'], alpha=0.02)
    else:
        pitch.arrows(xstart=120-row.x, ystart=80-row.y, xend=120-row.end_x, yend=80-row.end_y,ax=ax['pitch'], color="white", alpha=0.5, )
        pitch.scatter(120 - row.x, 80 - row.y, alpha=1, s=500, color="#427bad", ax=ax['pitch'])

fig.suptitle("Sara Caroline Seger successful passes in England vs Sweden.", fontsize=24)
plt.show()
import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Pitch, Sbopen, VerticalPitch


# Opening the dataset.
parser = Sbopen()
df, related, freeze, tactics = parser.event(69301)

# Get the team names.
team_1, team_2 = df.team_name.unique()

# A dataframe of shots.
shots = df.loc[df['type_name'] == 'Shot'].set_index('id')
# statsbomb opensource data.
from mplsoccer import Sbopen

# Initialize the parser of SBopen.
parser = Sbopen()

# Competitions.
# df_competition = parser.competition()

# # structure of the data.
# df_competition.info()


# Match data.
# df_match = parser.match(competition_id=72, season_id=30)

# df_match.info()

# Lineup Data.
df_lineup = parser.lineup(69301)

# structure of lineup data.
df_lineup.info()


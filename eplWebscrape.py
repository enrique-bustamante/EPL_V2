# %%
# Import dependencies
import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup as soup
# %%
url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

# %%
r = requests.get(url)
json = r.json()
# %%
json.keys()
# %%
elementsDf = pd.DataFrame(json['elements'])
elementTypesDf = pd.DataFrame(json['element_types'])
teamsDf = pd.DataFrame(json['teams'])
# %%
elementsDf['position'] = elementsDf.element_type.map(elementTypesDf.set_index('id').singular_name)

# %%
elementsDf['team'] = elementsDf.team.map(teamsDf.set_index('id').name)

# %%
elementsDf['value'] = elementsDf.value_season.astype(float)
elementColumns = elementsDf.columns
# %%
elementsDf = elementsDf[['second_name', 'team', 'position', 'form','points_per_game', 'total_points', 'now_cost', 'minutes','goals_scored', 'assists', 'clean_sheets', 'goals_conceded', 'own_goals', 'penalties_saved', 'penalties_missed', 'yellow_cards', 'red_cards', 'saves', 'bonus', 'bps', 'total_points', 'value']]
# %%
elementsDf = elementsDf.sort_values('value', ascending=False)

# %%
elementsDf['now_cost'] = elementsDf['now_cost']/10
# %%
print(elementsDf.head(25))
print(elementColumns)
# %%

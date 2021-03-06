# %%
# Import dependencies
import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup as soup
# %%
# set the url for the api in order to pull the data
url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

# %%
# read in the data from the JSON
r = requests.get(url)
json = r.json()
json.keys()
# %%
# create the dataframes that will be used to create the main dataframe
elementsDf = pd.DataFrame(json['elements'])
elementTypesDf = pd.DataFrame(json['element_types'])
teamsDf = pd.DataFrame(json['teams'])
# %%
# Add columns from other categories in the JSON file
elementsDf['position'] = elementsDf.element_type.map(elementTypesDf.set_index('id').singular_name)
elementsDf['team'] = elementsDf.team.map(teamsDf.set_index('id').name)
elementsDf['value'] = elementsDf.value_season.astype(float)
elementColumns = elementsDf.columns
# %%
elementsDf = elementsDf[['second_name', 'team', 'position', 'form','points_per_game', 'total_points', 'now_cost', 'minutes','goals_scored', 'assists', 'clean_sheets', 'goals_conceded', 'own_goals', 'penalties_saved', 'penalties_missed', 'yellow_cards', 'red_cards', 'saves', 'bonus', 'bps', 'total_points', 'value']]

# %%
# Make needed calculations and adjustments to the data
elementsDf['now_cost'] = elementsDf['now_cost']/10
# %%
# separate the dataframe into categorical and numerical values

# %%
# Run the numerical data through standardizer


# %%
# Fine tune the model using GridSearch

# %%
# Pass standardized data through random forest model

# %% 
# test accuracy of model

# %%
# The necessary data will be combined into one main dataframe

# %%
# Separate the data into positional dataframes and finally export in needed format
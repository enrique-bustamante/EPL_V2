# %%
# Import dependencies
import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup as soup
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

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
# Make needed calculations and adjustments to the data
elementsDf['now_cost'] = elementsDf['now_cost']/10
elementsDf['value'] = elementsDf['total_points']/elementsDf['now_cost']
elementColumns = elementsDf.columns

# %%
# Check data types and convert necessary columns
elementsDf.dtypes
elementsDf['form'] = elementsDf['form'].astype(float)
elementsDf['points_per_game'] = elementsDf['points_per_game'].astype(float)
elementsDf['bps'] = elementsDf['bps'].astype(float)
elementsDf.dtypes


# %%
elementsDf = elementsDf[['second_name', 'team', 'position', 'form','points_per_game', 'now_cost', 'minutes','goals_scored', 'assists', 'clean_sheets', 'goals_conceded', 'own_goals', 'penalties_saved', 'penalties_missed', 'yellow_cards', 'red_cards', 'saves', 'bonus', 'bps', 'total_points', 'value']]
elementsDf.isnull().values.any()
elementsDf.describe()
# %%
# separate the dataframe into categorical and numerical values
categoricalDf = elementsDf[['second_name', 'team', 'position', 'form', 'value', 'now_cost']]
numericalDf = elementsDf.drop(columns=['second_name', 'team', 'position', 'form', 'now_cost'])

# %%
# split data into training and tessting sets
numericAttributes = numericalDf.drop(['value'], axis=1)
numericFeatures = numericalDf['value']

numericTrainAttributes, numericTestAttributes, numericTrainFeatures, numericTestFeatures = train_test_split(numericAttributes, numericFeatures, test_size=0.2, random_state=42)


# %%
# Run the numerical data through standardizer
scaler = StandardScaler()
trainScaled = scaler.fit_transform(numericTrainAttributes)

testScaled = scaler.transform(numericTestAttributes)

# %%
# Fine tune the model using GridSearch
parameters = {'n_estimators': [50, 100, 150, 200]}


search = GridSearchCV(RandomForestRegressor(), param_grid=parameters, cv=5)
# %%
# Pass standardized data through random forest model
search.fit(trainScaled, numericTrainFeatures)

# %%
search.best_params_

# %%
rfModel = RandomForestRegressor(n_estimators=200)
rfModel.fit(trainScaled, numericTrainFeatures)
yPred = rfModel.predict(testScaled)
# %% 
# test accuracy of model
r2_score(numericTestFeatures, yPred)

# %%
# Add prediction column 
categoricalDf['predicted_value'] = rfModel.predict(scaler.transform(numericAttributes))
# %%
# The necessary data will be combined into one main dataframe
categoricalDf.head(10)
# %%
# Separate the data into positional dataframes and finally export in needed format
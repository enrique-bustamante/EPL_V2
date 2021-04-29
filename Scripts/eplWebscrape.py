# %%
def webscrape():

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
    from IPython.display import HTML

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
    elementsDf = elementsDf[['web_name', 'team', 'position', 'form','points_per_game', 'now_cost', 'minutes','goals_scored', 'assists', 'clean_sheets', 'goals_conceded', 'own_goals', 'penalties_saved', 'penalties_missed', 'yellow_cards', 'red_cards', 'saves', 'bonus', 'bps', 'total_points', 'value']]
    elementsDf.isnull().values.any()
    elementsDf.describe()
    elementsDf.set_index(['web_name'])

    # %%
    # separate the dataframe into categorical and numerical values
    categoricalDf = elementsDf[['web_name', 'team', 'position', 'form', 'value', 'now_cost']].set_index(['web_name'])
    numericalDf = elementsDf.drop(columns=['team', 'position', 'form', 'now_cost']).set_index(['web_name'])
    print([categoricalDf.head(), numericalDf.head()])
    # %%
    # import the rankings from the prior week
    #defLWRDf = pd.read_csv('rankings/DefenderRank copy.csv', index_col=0)[['team', 'total_rank']]
    #golLWRDf = pd.read_csv('rankings/GoalieRank copy.csv', index_col=0)[['team', 'total_rank']]
    #midLWRDf = pd.read_csv('rankings/MidfielderRank copy.csv', index_col=0)[['team', 'total_rank']]
    #forLWRDf = pd.read_csv('rankings/ForwardRank copy.csv', index_col=0)[['team', 'total_rank']]

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
    # convert best parameter into integer for use in the model
    bestParam = search.best_params_.get('n_estimators')


    # %%
    rfModel = RandomForestRegressor(n_estimators=bestParam)
    rfModel.fit(trainScaled, numericTrainFeatures)
    yPred = rfModel.predict(testScaled)
    # %%
    # test accuracy of model
    r2_score(numericTestFeatures, yPred)

    # %%
    # Add prediction column
    categoricalDf['predicted_value'] = rfModel.predict(scaler.transform(numericAttributes))
    categoricalDf['projection'] = categoricalDf['predicted_value'] * categoricalDf['now_cost']

    # Separate the data into positional dataframes
    defenderDf = categoricalDf[categoricalDf['position'] == 'Defender']
    goalieDf = categoricalDf[categoricalDf['position'] == 'Goalkeeper']
    middieDf = categoricalDf[categoricalDf['position'] == 'Midfielder']
    forwardDf = categoricalDf[categoricalDf['position'] == 'Forward']
    print(defenderDf)

    # %%
    # calculate Z scores
    def zScore(df):
        # Calculate means and STD for value and projections
        dfValueMean = df['value'].mean()
        dfValueSTD = df['value'].std()
        dfProjMean = df['projection'].mean()
        dfProjSTD = df['projection'].std()
        dfFormMean = df['form'].mean()
        dfFormSTD = df['form'].std()
        df['Z Score'] = (2 * ((df['value'] - dfValueMean)/dfValueSTD)) + (2 * ((df['projection'] - dfProjMean)/dfProjSTD)) + (((df['form']) - dfFormMean)/dfFormSTD)

        df['total_rank'] = df['Z Score'].rank(ascending=False)
        df = df[['team', 'position', 'value', 'projection', 'now_cost', 'total_rank', 'form']]
        df = df.sort_values('total_rank')
        return df

    # %%
    # pass the positional dataframes through the zScore function
    defenderDf = zScore(defenderDf)
    goalieDf = zScore(goalieDf)
    middieDf = zScore(middieDf)
    forwardDf = zScore(forwardDf)
    print(defenderDf)
    # %%
    # add last week rank
    #defenderDf['last_week_rank'] = defLWRDf['total_rank']
    #goalieDf['last_week_rank'] = golLWRDf['total_rank']
    #middieDf['last_week_rank'] = midLWRDf['total_rank']
    #forwardDf['last_week_rank'] = forLWRDf['total_rank']

    # %%
    HTML(defenderDf.head(20).to_html('templates/defenders.html', classes='table table-striped'))
    HTML(goalieDf.head(20).to_html('templates/goalies.html', classes='table table-striped'))
    HTML(middieDf.head(20).to_html('templates/midfielders.html', classes='table table-striped'))
    HTML(forwardDf.head(20).to_html('templates/forwards.html', classes='table table-striped'))

    # %%
    defenderDf.to_csv('rankings/DefenderRank.csv',index=True)
    goalieDf.to_csv('rankings/GoalieRank.csv', index=True)
    middieDf.to_csv('rankings/MidfielderRank.csv', index=True)
    forwardDf.to_csv('rankings/ForwardRank.csv',index=True)


        # %%

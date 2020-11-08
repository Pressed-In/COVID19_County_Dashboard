import pandas as pd
import pandas as pd

county_df = pd.read_csv("https://raw.githubusercontent.com/kjhealy/fips-codes/master/county_fips_master.csv", encoding='latin-1')

covid_df = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv", encoding='latin-1')

config = {'displayModeBar': False}

county_df["fips"] = county_df["fips"].astype(float)
covid_df["fips"] = covid_df["fips"].astype(float)


covid_df = covid_df.merge(county_df, on='fips', how='left', indicator=True) ### Join county info

covid_df = covid_df[['date', 'fips', 'state_abbr', 'state_name', 'county_x', 'cases', 'deaths']]

covid_df = covid_df.sort_values(by=['fips', 'date'], ignore_index=True)


covid_df['daily_cases'] = covid_df.groupby(['fips'])['cases'].diff().fillna(covid_df['cases']) ### Add daily cases column

covid_df['daily_deaths'] = covid_df.groupby(['fips'])['deaths'].diff().fillna(covid_df['deaths']) ### Add daily deaths column

covid_df.update(covid_df.filter(items=['daily_cases', 'daily_deaths']).clip(lower=0)) ### For daily cases & deaily deaths, nothing below 0

covid_df = covid_df[covid_df['fips'].notnull()]

covid_df = covid_df[covid_df['state_abbr'].notnull()]

covid_df = covid_df[covid_df['state_name'].notnull()]

print(covid_df)

covid_df.to_csv('dataframe.csv', index=False)
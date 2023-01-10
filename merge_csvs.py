import pandas as pd
from pandas import DataFrame, Series
from matplotlib import pyplot as plt

df1_composite_col_name = 'accomunit,unit,nace_r2,geo\\time'
df2_composite_col_name = 'indic_is,ind_type,unit,geo\\time'

df1 = pd.read_table('./tour_cap_nat.tsv', usecols=[df1_composite_col_name, '2016 '])
df2 = pd.read_table('./tin00083.tsv', usecols=[df2_composite_col_name, '2016 '])

df1[df1_composite_col_name.split(',')] =  df1[df1_composite_col_name].str.split(',', expand=True)
df2[df2_composite_col_name.split(',')] = df2[df2_composite_col_name].str.split(',', expand=True)

df1 = df1[
    (df1['accomunit'] == 'BEDPL')
    & (df1['unit'] == 'NR')
    & (df1['nace_r2'] == 'I551')
][['geo\\time', '2016 ']]

df2 = df2[df2['ind_type'] == 'IND_TOTAL'][['geo\\time', '2016 ']]

def filter_df(df: DataFrame):
    df = df[~df['2016 '].str.contains(':')]
    df = df[~df['2016 '].str.contains('^.*(?:u|bu)$')]
    df = df[~df['geo\\time'].isin(['EA', 'EU27_2007', 'EU27_2020', 'EU28'])]
    return df

def convert_val_col_to_float(series: Series):
    return series.replace({' b': ''}, regex=True).astype(float)

df1 = filter_df(df1)
df2 = filter_df(df2)
df1['2016 '] = convert_val_col_to_float(df1['2016 '])
df2['2016 '] = convert_val_col_to_float(df2['2016 '])

df1 = df1.rename(columns={'geo\\time': 'country_code', '2016 ': 'number_of_bed_places'})
df2 = df2.rename(columns={'geo\\time': 'country_code', '2016 ': 'percentage_of_individuals_online'})
df1 = df1[['country_code', 'number_of_bed_places']]
df2 = df2[['country_code', 'percentage_of_individuals_online']]

df_merged = pd.merge(df1, df2, on='country_code', how='outer')

df_merged.rename(columns={
    'country_code': 'Country Code',
    'percentage_of_individuals_online': 'Percentage of individuals online',
    'number_of_bed_places': 'Number of Bed-places'}
).to_csv('./merged.csv', index=False)

ax = df_merged.plot.scatter(x='number_of_bed_places', y='percentage_of_individuals_online')
for k, v in df_merged.iterrows():
    ax.annotate(v['country_code'], (v['number_of_bed_places'], v['percentage_of_individuals_online']))

plt.show()

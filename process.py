# coding: utf-8

import locale
from pathlib import Path
import pandas as pd
import numpy as np


def log10_row(row):
    try:
        for key in row.keys():
            if not isinstance(row[key], str) and isinstance(row[key], float) and row[key] != 0:
                row[key] = np.log10(row[key])
    except Exception as e:
        print("error log10", e)
    return row


if __name__ == '__main__':
    data_url = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data' \
               r'/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv '
    # use system decimal_point
    locale.setlocale(locale.LC_ALL, "")
    decimal_char = locale.localeconv()["decimal_point"]
    path = r"data/"
    in_path = Path(path)
    in_path.mkdir(parents=True, exist_ok=True)
    # main dataframe
    df = pd.read_csv(data_url)
    df.index.names = ['id']

    # rename korea
    df['Country/Region'] = df['Country/Region'].replace({'Korea, South': 'South Korea'})
    # Remove Cruise Ship
    df = df[~df['Country/Region'].isin(['Cruise Ship'])]
    df = df[~df['Country/Region'].isin(['Diamond Princess'])]
    # dt_cols = df.columns[~df.columns.isin(['Province/State', 'Country/Region', 'Lat', 'Long'])]

    country_path = r"assets/countries.csv"
    # do not use default NA values, because of NA region
    cf = pd.read_csv(country_path, sep=";", keep_default_na=False, na_values=[''])
    cf.index.names = ['id']
    pcf = cf
    cf = cf.drop('code', 1).drop('population', 1)

    # sum days cols values by country
    # prepare col list for grouping
    date_cols = df.keys()[4:]
    sum_cols = {}
    for date in date_cols:
        sum_cols[date] = 'sum'
    gdf = df.groupby(['Country/Region']).agg(sum_cols).reset_index()
    gdf.index.names = ['id']

    # sort by max in last column
    gdf = gdf.sort_values(by=[date_cols[-1]], ascending=True)
    gdf = pd.concat([gdf.set_index("Country/Region"), cf.set_index("country")], axis=1, join='outer', sort=False)
    gdf.index.names = ["Country/Region"]

    # move region column to the beginning
    gdf = gdf.reindex(columns=['region'] + gdf.columns[:-1].tolist())
    gdf = gdf.reset_index()
    gdf.index.names = ['id']

    # remove rows without values
    gdf = gdf.dropna(thresh=5)
    # copy gdf into tdf
    tdf = gdf
    pdf = gdf
    pcdf = gdf

    with open(in_path.joinpath("time_series_confirmed_country.csv"), 'w') as csv_file:
        gdf.to_csv(path_or_buf=csv_file, sep=";", line_terminator='\n', encoding='utf-8', decimal=decimal_char)

    gdf = gdf.drop('region', 1)

    # full reshaped frame
    reshaped_df = pd.melt(gdf, id_vars=["Country/Region"], var_name="date")
    rdf = reshaped_df.pivot(index='date', columns='Country/Region', values='value')
    # index to datetime
    rdf.index = pd.to_datetime(rdf.index)

    with open(in_path.joinpath("time_series_confirmed_country_pivot.csv"), 'w') as csv_file:
        rdf.to_csv(path_or_buf=csv_file, sep=";", line_terminator='\n', encoding='utf-8')

    # attention, garder country comme index
    # use df.diff() luke!
    reg = pd.DataFrame()
    reg["region"] = tdf.pop('region')
    reg = reg.reset_index()
    tdf = tdf.set_index("Country/Region").diff(periods=1, axis=1)
    # add column region
    # insert performed with values from reg["region"].values
    tdf.insert(0, "region", value=reg["region"].values, allow_duplicates=True)
    # sort by max in last column
    tdf = tdf.sort_values(by=[date_cols[-1]], ascending=True)

    with open(in_path.joinpath("time_series_confirmed_country_day.csv"), 'w') as csv_file:
        tdf.to_csv(path_or_buf=csv_file, sep=";", line_terminator='\n', encoding='utf-8', decimal=decimal_char)

    # calc percentage change between 2 cols, rounded
    pdf = pdf.set_index("Country/Region").pct_change(periods=1, axis='columns').round(3)
    # insert region series
    pdf.insert(0, "region", value=reg["region"].values, allow_duplicates=True)
    pdf = pdf.replace([np.inf, -np.inf], np.nan, regex=True)

    # use comma as decimal separator
    # remove inf results
    with open(in_path.joinpath("time_series_confirmed_country_pct.csv"), 'w') as csv_file:
        pdf.to_csv(path_or_buf=csv_file, sep=";", line_terminator='\n', encoding='utf-8', decimal=decimal_char)

    # pcf pcdf
    pcdf = pd.concat([pcdf.set_index("Country/Region"), pcf.set_index("country")], axis=1, join='outer', sort=False)
    pcdf.index.names = ["Country/Region"]
    pcdf = pcdf.drop('code', 1)
    pcdf = pcdf.drop('region', 1)
    pcdf = pcdf.dropna(thresh=5)

    pop = pd.DataFrame()
    # population normale pour la comparaison
    # use 100K or 1M --> 1M
    norm_pop = 1000000
    pop["population"] = pcdf.pop('population')
    pop = pop.reset_index()
    pcdf = pcdf.div(pop["population"].values, axis=0).mul(norm_pop).round(1)
    # insert population series
    pcdf.insert(0, "population", value=pop["population"].values, allow_duplicates=True)

    # cases by population and normalized for 1M
    with open(in_path.joinpath("time_series_confirmed_country_cases_1m_pop.csv"), 'w') as csv_file:
        pcdf.to_csv(path_or_buf=csv_file, sep=";", line_terminator='\n', encoding='utf-8', decimal=decimal_char)

    # log10 dataframe
    # gdt_cols = gdf.columns[~gdf.columns.isin(['Country/Region'])]
    ldf = gdf.apply(log10_row, axis=1)
    # remove index id

    # log10 cases by population
    with open(in_path.joinpath("time_series_confirmed_country_log10.csv"), 'w') as csv_file:
        ldf.to_csv(path_or_buf=csv_file, sep=";", line_terminator='\n', encoding='utf-8', decimal=decimal_char)

    print("Done")

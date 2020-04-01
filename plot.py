# coding: utf-8

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    decimal_char = ','
    path = r"data/"
    in_path = Path(path)
    # main dataframe
    # do not use default NA values, because of NA region
    gdf = pd.read_csv(in_path.joinpath("time_series_confirmed_country.csv"), sep=";", encoding='utf-8', decimal=decimal_char,
                      keep_default_na=False, na_values=[''])
    gdf = gdf.drop('id', 1)
    gdf.index.names = ['id']
    date_cols = gdf.keys()[3:]

    # Create filtered dataframes
    # european df
    nodata_mask = (gdf["region"] == "EU")
    e_df = gdf.loc[nodata_mask]
    # we do not need region col anymore
    e_df = e_df.drop('region', 1)
    gdf = gdf.drop('region', 1)

    # small europeans (0-90)
    min_limit = 40
    max_limit = 500
    nodata_mask = (e_df[date_cols[-1]] > min_limit) & (e_df[date_cols[-1]] < max_limit)
    se_df = e_df.loc[nodata_mask]
    se_df = se_df.tail(6)

    # middle europeans
    min_limit = 501
    max_limit = 5000
    nodata_mask = (e_df[date_cols[-1]] > min_limit) & (e_df[date_cols[-1]] < max_limit)
    me_df = e_df.loc[nodata_mask]
    # limit results to max 8 countries
    me_df = me_df.tail(8)

    # middle europeans 2
    min_limit = 5001
    max_limit = 50000
    nodata_mask = (e_df[date_cols[-1]] > min_limit) & (e_df[date_cols[-1]] < max_limit)
    me2_df = e_df.loc[nodata_mask]
    me2_df = me2_df.tail(8)

    # large europeans
    min_limit = 50001
    max_limit = 9999999
    nodata_mask = (e_df[date_cols[-1]] > min_limit) & (e_df[date_cols[-1]] < max_limit)
    lei_df = e_df.loc[nodata_mask]

    # large europeans w/o italy
    min_limit = 50001
    max_limit = 9999999
    nodata_mask = (e_df[date_cols[-1]] > min_limit) & (e_df[date_cols[-1]] < max_limit) & (
            gdf["Country/Region"] != "Italy")
    le_df = e_df.loc[nodata_mask]

    # top 8 world w/o china
    # tail and not head because sort order
    nodata_mask = (gdf["Country/Region"] != "China")
    t5_df = gdf.loc[nodata_mask].tail(8)

    # top 8 world
    # tail and not head because sort order
    t5c_df = gdf.tail(8)

    # *************
    # PLOT SECTION
    # *************

    # generate some graphs from gdf
    plt.close('all')
    # plt.style.use('classic')
    plt.style.use('Solarize_Light2')

    # full reshaped frame
    reshaped_df = pd.melt(gdf, id_vars=["Country/Region"], var_name="date")
    rdf = reshaped_df.pivot(index='date', columns='Country/Region', values='value')
    # index to datetime
    rdf.index = pd.to_datetime(rdf.index)

    min_month = 2

    # se reshaped frame
    rse_df = pd.melt(se_df, id_vars=["Country/Region"], var_name="date")
    rse_df = rse_df.pivot(index='date', columns='Country/Region', values='value')
    # index to datetime
    rse_df.index = pd.to_datetime(rse_df.index)
    # filter all dates before march
    rse_df = rse_df[(rse_df.index.month > min_month)]

    # me reshaped frame
    rme_df = pd.melt(me_df, id_vars=["Country/Region"], var_name="date")
    rme_df = rme_df.pivot(index='date', columns='Country/Region', values='value')
    # index to datetime
    rme_df.index = pd.to_datetime(rme_df.index)
    # filter all dates before march
    rme_df = rme_df[(rme_df.index.month > min_month)]

    # me reshaped frame
    rme2_df = pd.melt(me2_df, id_vars=["Country/Region"], var_name="date")
    rme2_df = rme2_df.pivot(index='date', columns='Country/Region', values='value')
    # index to datetime
    rme2_df.index = pd.to_datetime(rme2_df.index)
    # filter all dates before march
    rme2_df = rme2_df[(rme2_df.index.month > min_month)]

    # le reshaped frame
    rle_df = pd.melt(le_df, id_vars=["Country/Region"], var_name="date")
    rle_df = rle_df.pivot(index='date', columns='Country/Region', values='value')
    # index to datetime
    rle_df.index = pd.to_datetime(rle_df.index)
    # filter all dates before march
    rle_df = rle_df[(rle_df.index.month > min_month)]

    # le reshaped frame
    rlei_df = pd.melt(lei_df, id_vars=["Country/Region"], var_name="date")
    rlei_df = rlei_df.pivot(index='date', columns='Country/Region', values='value')
    # index to datetime
    rlei_df.index = pd.to_datetime(rlei_df.index)
    # filter all dates before march
    rlei_df = rlei_df[(rlei_df.index.month > min_month)]

    # t5 reshaped frame
    rt5_df = pd.melt(t5_df, id_vars=["Country/Region"], var_name="date")
    rt5_df = rt5_df.pivot(index='date', columns='Country/Region', values='value')
    # index to datetime
    rt5_df.index = pd.to_datetime(rt5_df.index)
    # filter all dates before march
    rt5_df = rt5_df[(rt5_df.index.month > min_month)]

    # t5c reshaped frame
    rt5c_df = pd.melt(t5c_df, id_vars=["Country/Region"], var_name="date")
    rt5c_df = rt5c_df.pivot(index='date', columns='Country/Region', values='value')
    # index to datetime
    rt5c_df.index = pd.to_datetime(rt5c_df.index)
    # filter all dates before march
    rt5c_df = rt5c_df[(rt5c_df.index.month > min_month)]

    fig, ax = plt.subplots()
    # Don't allow the axis to be on top of your data
    ax.set_axisbelow(True)
    # Turn on the minor TICKS, which are required for the minor GRID
    ax.minorticks_on()
    # Customize the major grid
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='black')
    # Customize the minor grid
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

    # look how to properly show multiple plots
    rse_df.plot(linewidth=3, ax=ax)
    rme_df.plot(linewidth=3)
    rme2_df.plot(linewidth=3)
    rle_df.plot(linewidth=3)
    rlei_df.plot(linewidth=3)
    rt5_df.plot(linewidth=3)
    rt5c_df.plot(linewidth=3)
    plt.show()

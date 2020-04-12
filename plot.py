# coding: utf-8

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def prepare_dataframe(src_df, filter):
    df = pd.melt(src_df, id_vars=["Country/Region"], var_name="date")
    df = df.pivot(index='date', columns='Country/Region', values='value')
    # index to datetime
    df.index = pd.to_datetime(df.index)
    # filter all dates before march
    df = df[(df.index > filter)]
    return df


if __name__ == '__main__':
    decimal_char = ','
    path = r"data/"
    in_path = Path(path)
    # main dataframe
    # do not use default NA values, because of NA region
    gdf = pd.read_csv(in_path.joinpath("time_series_confirmed_country.csv"), sep=";", encoding='utf-8',
                      decimal=decimal_char, keep_default_na=False, na_values=[''])
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
    # min_limit = 40
    # max_limit = 500
    # nodata_mask = (e_df[date_cols[-1]] > min_limit) & (e_df[date_cols[-1]] < max_limit)
    # se_df = e_df.loc[nodata_mask]
    # se_df = se_df.tail(6)

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

    # selected eu countries
    # 'Italy', 'Spain', 'Germany', 'France', 'United Kingdom'
    edf_m = e_df[e_df['Country/Region'].isin(['Switzerland', 'Belgium', 'Austria', 'Portugal',
                                              'Netherlands', 'Sweden', 'Norway', 'Denmark'])]
    # small eu
    edf_r = e_df[e_df['Country/Region'].isin(['Ireland', 'Czechia', 'Poland',
                                              'Romania', 'Finland', 'Greece', 'Luxembourg'])]

    # east eu
    edf_e = e_df[e_df['Country/Region'].isin(['Russia', 'Ukraine', 'Belarus', 'Poland',
                                              'Estonia', 'Lithuania'])]

    # top 8 world w/o us
    # tail and not head because sort order
    nodata_mask = (gdf["Country/Region"] != "US")
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

    # from march
    min_month = 2
    min_date = '2020-2-20'

    # se reshaped frame
    # rse_df = prepare_dataframe(se_df, min_date)

    # me reshaped frame
    rme_df = prepare_dataframe(me_df, min_date)

    # me reshaped frame
    rme2_df = prepare_dataframe(me2_df, min_date)

    # le reshaped frame
    rlei_df = prepare_dataframe(lei_df, min_date)

    # t5 reshaped frame
    rt5_df = prepare_dataframe(t5_df, min_date)

    # t5c reshaped frame
    rt5c_df = prepare_dataframe(t5c_df, min_date)

    # edf_m reshaped frame
    redf_m = prepare_dataframe(edf_m, min_date)

    # edf_r reshaped frame
    redf_r = prepare_dataframe(edf_r, min_date)

    # east eu other
    redf_e = prepare_dataframe(edf_e, min_date)

    # play with log
    ldf = pd.read_csv(in_path.joinpath("time_series_confirmed_country_log10.csv"), sep=";", encoding='utf-8',
                      decimal=decimal_char,
                      keep_default_na=False, na_values=[''])
    ldf = ldf.drop('id', 1)
    date_cols = ldf.keys()[3:]
    ldf = ldf[ldf['Country/Region'].isin(['US', 'Italy', 'Spain',
                                              'Germany', 'France', 'United Kingdom'])]
    rldf = prepare_dataframe(ldf, min_date)

    fig, ax = plt.subplots()
    # Don't allow the axis to be on top of your data
    ax.set_axisbelow(True)
    # Turn on the minor TICKS, which are required for the minor GRID
    # ax.minorticks_on()
    # Customize the major grid
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='black')
    # Customize the minor grid
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

    # look how to properly show multiple plots
    # , ax=ax
    # rse_df.plot(linewidth=3, ax=ax)
    rme_df.plot(linewidth=3, ax=ax)
    rme2_df.plot(linewidth=3)
    rlei_df.plot(linewidth=3)
    rt5_df.plot(linewidth=3)
    rt5c_df.plot(linewidth=3)
    redf_e.plot(linewidth=3, title="Other east europe")
    redf_r.plot(linewidth=3, title="Small sized european countries")
    redf_m.plot(linewidth=3, title="Middle sized european countries")
    rldf.plot(linewidth=3, title="Log10")
    plt.show()

    # plt.close('all')
    # fig, axes = plt.subplots(nrows=1, ncols=2)
    # redf_m.plot(ax=axes[0], title="Middle sized european countries")
    # redf_r.plot(ax=axes[1], title="Small sized european countries")
    # plt.show()

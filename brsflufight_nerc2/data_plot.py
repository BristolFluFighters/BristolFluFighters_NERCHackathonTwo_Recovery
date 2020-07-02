import math

from matplotlib import pyplot as plt
import pandas as pd

from .data_access import DataSet


def plot_yearly_series(
    series,
    series_name='series',
    norms = ['1D', '7D', '30D'],
):
    df = pd.DataFrame({series_name: series})
    df["dayofyear"] = df.index.dayofyear
    fig, axs = plt.subplots(1, len(norms))

    fig.set_size_inches(5*len(norms) + 1 , 5)
    fig.suptitle(f"{series_name}")
    axs[0].set_ylabel('')

    for norm in norms:
        df[f"{series_name}_{norm}"] = df[series_name].rolling(norm).mean()
    for year in ["2016", "2017", "2018", "2019", "2020"]:  # df.index.year.unique()
        year = str(year)
        for i, norm in enumerate(norms):
            df[year].plot(x="dayofyear", y=f"{series_name}_{norm}", ax=axs[i], label=year)
    for ax in axs:
        ax.legend(ncol=3)

def plot_yearly_data(
    data_sets,
    data_source,
    fields = "demand",
    norms = ['1D', '7D', '30D'],
    country = 'United Kingdom',
):
    df = data_sets[data_source].get_country(country)
    df["dayofyear"] = df.index.dayofyear
    if isinstance(fields, type(str())):
        fields = [fields]

    for field in fields:
        fig, axs = plt.subplots(1, len(norms))

        fig.set_size_inches(5*len(norms) + 1 , 5)
        fig.suptitle(f"UK energy - {field}")
        axs[0].set_ylabel('Power [MW]')

        for norm in norms:
            df[f"{field}_{norm}"] = df[field].rolling(norm, center=True).mean()
        for year in ["2016", "2017", "2018", "2019", "2020"]:  # df.index.year.unique()
            year = str(year)
            for i, norm in enumerate(norms):
                df[year].plot(x="dayofyear", y=f"{field}_{norm}", ax=axs[i], label=year)
        for ax in axs:
            ax.legend(ncol=3)


def squarish_layout(n, h_max=4):
    if n <= 0:
        ValueError()
    nh = min(math.ceil(math.sqrt(n)), h_max)
    nv = math.ceil(n/nh)
    return nv,nh


def rectangular_layout(n, h_max=4):
    if n <= 0:
        ValueError()
    
    nv = math.ceil(n / h_max)
    nh = math.ceil(n / nv) 
    
    return nv,nh
    

def plot_historical_GHG_columns(
    df,
    columns,
    countries,
    gas=None,
):
    if gas is None:
        y_label_fun = "{} [{}]".format
    else:
        y_label_fun = lambda x, y :"{} [{}]".format(gas, y)

    layout = rectangular_layout(len(columns), h_max=4)
    fig, axs = plt.subplots(layout[0], layout[1])
    fig.suptitle(gas)
    fig.set_size_inches(layout[1]*5 + 2, layout[0]*5)
    axs = axs.flatten()
    for i, sector in enumerate(columns):
        for country in countries:
            idx = country
            df.loc[idx].plot(x="date", y=sector, label=f"{idx}", ax=axs[i])
        unit = df.loc[idx, "Unit"].unique()[-1]
        axs[i].set_ylabel(y_label_fun(sector, unit))
        axs[i].set_title(f"{sector}")


def plot_historical_GHG(
    data_sets,
    data_source,
    countries,
    gases=None,
    partial_sectors=None,
    group_by=None
):
    df = data_sets[data_source].df
    col = data_sets[data_source].data_columns

    if partial_sectors is None:
        sectors = col
    else:
        sectors = []
        for s in partial_sectors:
            sectors.extend([c for c in col if s in c])    
    
    if gases is not None:
        sectors_gas = []
        for gas in gases:
            sectors_gas.extend([c for c in sectors if f"({gas})" in c])
        sectors = sectors_gas

    if group_by == 'ghg':
        for gas in gases:
            active_sectors = [s for s in sectors if f"({gas})" in s]
            plot_historical_GHG_columns(df, active_sectors, countries, gas=gas)
    elif group_by == 'sector':
        for p_sector in partial_sectors:
            active_sectors = [s for s in sectors if f"{p_sector}" in s]
            plot_historical_GHG_columns(df, active_sectors, countries)
    else:
        plot_historical_GHG_columns(df, sectors, countries)


def plot_mobility(
    data_source:str,
    data_zone:str,
    data_sets:[dict, DataSet],
):
    df = data_sets[data_source].df
    cols = data_sets[data_source].data_columns

    fig, axs = plt.subplots(1,2)
    fig.set_size_inches(14,5)
    fig.suptitle(f"{data_source} in {data_zone}")
    label_fun = "{} - {}".format
    if isinstance(data_zone, type(str())):
        data_zone = [data_zone]
        label_fun = lambda x, y: y

    for zone in data_zone:
        # same plot as above
        labels = [label_fun(zone, c) for c in cols]
        axs[0].set_title('Raw mobility data')
        df.loc[zone].plot(y=cols, ax=axs[0], label=labels)
        # 7 Day rolling average
        axs[1].set_title('Weekly averaged mobility data')
        df.loc[zone, cols].rolling('7D').mean().plot(
            y=cols, ax=axs[1], label=labels)

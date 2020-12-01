import os
import numpy as np
import pandas as pd
from datetime import timedelta
import holidays

def file_names(path='../'):
    csv_files = []
    for root, direc, files in os.walk('../'):
        if 'raw_data\\' in root:
            csv_files.append(files)
    return csv_files


def get_price(path='../raw_data/price/'):
    price_files = file_names()[2]
    df = pd.read_csv(path+price_files[0])
    for file in price_files[1:]:
        df_2 = pd.read_csv(path+file)
        df = pd.concat([df, df_2])
    df = df.reset_index(drop=True)
    df.columns = ['time', 'price']
    df['time'] = df.time.str[:16]
    df = df[df.price!='-'] # filtering the timestamps till 24.11.2020
    df['time'] = pd.to_datetime(df['time'], format='%d.%m.%Y %H:%M')
    df['price'] = df.price.astype('float')
    df.set_index(pd.DatetimeIndex(df['time']), inplace=True)
    df.drop(columns=['time'], inplace=True)
    return df

def get_load(path='../raw_data/load/'):
    load_files = file_names()[1]
    df = pd.read_csv(path+load_files[0])
    for file in load_files[1:]:
        df_2 = pd.read_csv(path+file)
        df = pd.concat([df, df_2])
    df = df.reset_index(drop=True)
    df = df.drop(columns='Day-ahead Total Load Forecast [MW] - BZN|DK1')
    df.columns = ['time', 'load']
    df['time'] = df.time.str[:16]
    df = df[df.load!='-'] # filtering the timestamps till 24.11.2020
    df['time'] = pd.to_datetime(df['time'], format='%d.%m.%Y %H:%M')
    df['load'] = df.load.astype('float')
    df.set_index(pd.DatetimeIndex(df['time']), inplace=True)
    df.drop(columns=['time'], inplace=True)
    return df

def get_shifted_price():
    """Takes in dataframe and performs shift to compensate for daylight saving"""
    df = get_price()
    df_1 = df.loc['2015-01-01 00:00:00':'2015-03-29 01:00:00']
    df_2 = df.loc['2015-03-29 02:00:00':'2015-10-25 02:00:00']
    df_3 = df.loc['2015-10-25 03:00:00':'2016-03-27 01:00:00']
    df_4 = df.loc['2016-03-27 02:00:00':'2016-10-30 02:00:00']
    df_5 = df.loc['2016-10-30 03:00:00':'2017-03-26 01:00:00']
    df_6 = df.loc['2017-03-26 02:00:00':'2017-10-29 02:00:00']
    df_7 = df.loc['2017-10-29 03:00:00':'2018-03-25 01:00:00']
    df_8 = df.loc['2018-03-25 02:00:00':'2018-10-28 02:00:00']
    df_9 = df.loc['2018-10-28 03:00:00':'2019-03-31 01:00:00']
    df_10 = df.loc['2019-03-31 02:00:00':'2019-10-27 02:00:00']
    df_11 = df.loc['2019-10-27 03:00:00':'2020-03-29 01:00:00']
    df_12 = df.loc['2020-03-29 02:00:00':'2020-10-25 02:00:00']
    df_13 = df.loc['2020-10-25 03:00:00':'2020-11-23 16:00:00']

    df_shift = [df_2, df_4, df_6, df_8, df_10, df_12]
    no_shift = [df_1, df_3, df_5, df_7, df_9, df_11, df_13]

    price_df = df_1
    for data in no_shift[1:]:
        price_df = pd.concat([price_df, data])
    for data in df_shift:
        data = data.shift(periods=-1).dropna()
        price_df = pd.concat([price_df, data])

    price_df = price_df.sort_index()

    return price_df


def get_shifted_load():
    """Takes in dataframe and performs shift to compensate for daylight saving"""
    df = get_load()
    df_1 = df.loc['2015-01-01 00:00:00':'2015-03-29 01:00:00']
    df_2 = df.loc['2015-03-29 02:00:00':'2015-10-25 02:00:00']
    df_3 = df.loc['2015-10-25 03:00:00':'2016-03-27 01:00:00']
    df_4 = df.loc['2016-03-27 02:00:00':'2016-10-30 02:00:00']
    df_5 = df.loc['2016-10-30 03:00:00':'2017-03-26 01:00:00']
    df_6 = df.loc['2017-03-26 02:00:00':'2017-10-29 02:00:00']
    df_7 = df.loc['2017-10-29 03:00:00':'2018-03-25 01:00:00']
    df_8 = df.loc['2018-03-25 02:00:00':'2018-10-28 02:00:00']
    df_9 = df.loc['2018-10-28 03:00:00':'2019-03-31 01:00:00']
    df_10 = df.loc['2019-03-31 02:00:00':'2019-10-27 02:00:00']
    df_11 = df.loc['2019-10-27 03:00:00':'2020-03-29 01:00:00']
    df_12 = df.loc['2020-03-29 02:00:00':'2020-10-25 02:00:00']
    df_13 = df.loc['2020-10-25 03:00:00':'2020-11-23 16:00:00']

    df_shift = [df_2, df_4, df_6, df_8, df_10, df_12]
    no_shift = [df_1, df_3, df_5, df_7, df_9, df_11, df_13]

    load_df = df_1
    for data in no_shift[1:]:
        load_df = pd.concat([load_df, data])
    for data in df_shift:
        data = data.shift(periods=-1).dropna()
        load_df = pd.concat([load_df, data])

    load_df = load_df.sort_index()

    return load_df


def get_weather(path='../raw_data/weather_2015_2020.csv'):
    df = pd.read_csv(path)

    df['dt'] = pd.to_datetime(df.dt)

    # drop unnecessary columns
    to_drop = ['dt_iso','timezone','lat', 'lon','sea_level','grnd_level',
               'rain_1h','rain_3h', 'pressure', 'snow_1h', 'snow_3h',
               'temp_min','temp_max','weather_id', 'weather_description',
               'weather_icon', 'wind_deg']
    df = df.drop(to_drop, axis=1)

    # population of each city in the df
    pop = {'Aarhus': 349_983,
        'Odense': 204_895,
        'Aalborg': 217_075,
        'Esbjerg': 115_748,
        'Vejle': 111_743,
        'Randers': 96_559,
        'Viborg': 93_819,
        'Kolding': 89_412,
        'Silkeborg': 89_328,
        'Herning': 86_348,
        'Horsens': 83_598}

    df['population'] = [pop[city] for city in df.city_name]

    # numeric weather values as affects demand or supply
    numeric_cols = ['temp', 'feels_like', 'humidity',  'clouds_all','wind_speed']

    weather_df = pd.DataFrame()

    #for the numeric columns, group by datetime and average according to their population weight
    for col in numeric_cols:
    #group by the datecolumn for each element in the column average it by it's weight
        weather_df[col] = df.groupby(df.dt).apply(lambda x : np.average(x[col], weights=x.population))

    # check for missing indices
    missing_idx = pd.date_range(start = '2015-01-01', end = '2020-11-24', freq='H' ).difference(weather_df.index)

    # impute missing indices with average of bounding rows
    for idx in missing_idx:
        weather_df.loc[idx] = weather_df.loc[pd.to_datetime(idx) - timedelta(hours= 1)] + \
                      weather_df.loc[pd.to_datetime(idx) + timedelta(hours= 1)] / 2

    weather_df = weather_df.sort_index()

    return weather_df


def get_holidays(start='1/1/2015', stop='23/11/2020', country='DK', frequency='D'):
    """
    Takes in a start and stop date and a country.
    Produces a dataframe with a daily date time index and columns:
    day_of_week - numerical day of the week identifier 0 for monday
    holiday_bool - boolean true or false for holiday
    holiday_name - name of the holiday if holiday_bool is true
    Returns a dataframe
    """
    #generate the range of daily dates
    dates = pd.date_range(start=start, end=stop, freq=frequency)
    #create the holiday object
    country_holidays = holidays.CountryHoliday(country)
    #create a list for the holiday bool and name
    holiday_list = []
    #loop through the dates
    for date in dates:
        #true if holiday in object, false otherwise
        holiday_bool = date in country_holidays
        holiday_names = country_holidays.get(date)
        holiday_list.append([holiday_bool, holiday_names])
    #create return dataframe
    holidays_data = pd.DataFrame(holiday_list, index=dates, columns=['holiday', 'holiday_name'])
    holidays_data.holiday=holidays_data.holiday.astype('int')
    # add whether it is weekend
    holidays_data['weekend'] = 0
    holidays_data.loc[(holidays_data.index.dayofweek==5) | (holidays_data.index.dayofweek==6), 'weekend'] = 1
    return holidays_data


def get_days_dummies(start='1/1/2015', stop='23/11/2020', frequency='D'):
    """
    Takes in a start and stop date and frequency.
    Produces a dataframe with a date time index at the frequency input and columns:
    weekday_id - numerical day of the week identifier 0 for monday
    Returns a dataframe
    """
    #generate the range of daily dates
    dates = pd.date_range(start=start, end=stop, freq=frequency)
    #create a dataframe of weekday categories
    days = pd.DataFrame(list(dates.weekday), index=dates, columns=['weekday_id'])
    days = pd.get_dummies(days['weekday_id'])
    columns = ['mon', 'tue', 'wed', 'thur', 'fri', 'sat', 'sun']
    days.columns = columns
    return days


def get_coal_price(path='../raw_data/coal_price.xls'):
    """return daily coal prices from 25-NOV-15 till 24-NOV-20"""
    df = pd.read_excel(path, skiprows=2)
    df = df.rename(columns={'Unnamed: 0':'time',
                            'ROTTERDAM COAL': 'coal_price'})
    df.time = pd.to_datetime(df.time)

    df = df.set_index('time').sort_index()
    df.fillna(method='ffill', inplace=True)

    return df


def get_wind_prod(path="../raw_data/productionconsumptionsettlement.csv"):
    """Returns a feature-engineered dataframe including:
    1. Wind production
    2. Wind share of total production
    """
    data = pd.read_csv(path)

    # columns with actual (needed) prod values
    measures = data.drop(columns=["HourUTC","HourDK"]).columns
    df = data[["HourDK"] + list(measures)]

    # convert to datetime and set time index
    df['time'] = pd.to_datetime(df['HourDK'].replace("T", " "))
    df = df.drop(columns="HourDK").sort_values(by="time").set_index("time").loc["2015-01-01":]

    # columns to be engineered
    wind = ["OffshoreWindLt100MW_MWh", "OffshoreWindGe100MW_MWh",
            "OnshoreWindLt50kW_MWh", "OnshoreWindGe50kW_MWh"]

    non_wind = ["CentralPowerMWh", "LocalPowerMWh", "HydroPowerMWh",
                "SolarPowerLt10kW_MWh", "SolarPowerGe10Lt40kW_MWh",
                "SolarPowerGe40kW_MWh", "TransmissionLossMWh"]

    irrelevant_cols = ["PriceArea","ExchangeGE_MWh","PowerToHeatMWh",
                       "ExchangeNO_MWh","ExchangeSE_MWh", "ExchangeNL_MWh",
                       "GrossConsumptionMWh","ExchangeGreatBelt_MWh",
                       "LocalPowerSelfConMWh"]

    substract_cols = "SolarPowerSelfConMWh"

    part_null_cols = ["SolarPowerGe10Lt40kW_MWh","SolarPowerGe40kW_MWh",
                      "SolarPowerLt10kW_MWh","TransmissionLossMWh"]

    # drop irrelevant
    df = df.drop(columns=irrelevant_cols)
    # deal with NaNs
    df[substract_cols] = df[substract_cols].fillna(0)
    df[part_null_cols] = df[part_null_cols].fillna(0)

    # wind_prod & non_wind engineered from sum off all wind / nonwind cols
    df['wind_prod'] = df[wind].sum(axis=1)
    df["non_wind_prod"] = df[non_wind].sum(axis=1)

    # total prod and wind percentage of total defined
    df["total_prod"] = df["wind_prod"] + df["non_wind_prod"] - df[substract_cols]
    df["wind_share"] = df["wind_prod"] / df["total_prod"]

    # final df with needed engineered cols
    final_df = df[["total_prod", "wind_prod", "wind_share"]]

    return final_df

def get_all(hour=11):
    '''take a hour=n and returns a df,
    df contains the values for price and all the other features for the specific
    hour (n) of the day '''
    df_price = get_shifted_price()
    df_price_11 = df_price[df_price.index.hour==hour]
    df_load = get_shifted_load()
    df_load_11 = df_load[df_load.index.hour==hour]
    df_weather = get_weather()
    df_weather_11 = df_weather[df_weather.index.hour==hour]
    df_holidays = get_holidays().drop(columns=['holiday_name'])
    df_wind = get_wind_prod()
    df_wind_11 = df_wind[df_wind.index.hour==hour]
    df_coal = get_coal_price()
    df_coal_11 = df_coal[df_coal.index.hour==hour]
    # change the index of df_holidays so that it can be joined with others
    df_coal['time']=f'{str(hour)}:00'
    df_coal.time = pd.to_timedelta(df_coal.time + ':00')
    df_coal.index = df_coal.index + df_coal.time
    df_coal_11 = df_coal.drop('time', axis=1)
    # change the index of df_holidays so that it can be joined with others
    df_holidays['time']=f'{str(hour)}:00'
    df_holidays.time = pd.to_timedelta(df_holidays.time + ':00')
    df_holidays.index = df_holidays.index + df_holidays.time
    df_holidays_11 = df_holidays.drop('time', axis=1)
    # joining all the dataframes
    dfs = dict(load=df_load_11, coal=df_coal_11, weather=df_weather_11, wind=df_wind_11, holidays=df_holidays_11)
    # merge all features
    df_all = df_price_11
    for df in dfs.values():
        df_all = df_all.join(df, how='outer')
    # wind production data is only available till 2020-11-18, so cut the date
    #df_all = df_all[df_all.index < '2020-11-19 00:00:00']
    return df_all

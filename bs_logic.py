import calendar as cal
import time

import pandas as pd

CITY_DATA = {'Chicago': 'chicago.csv',
             'New York City': 'new_york_city.csv',
             'Washington': 'washington.csv'}
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June']
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    filename = 'static\\' + CITY_DATA[city]
    # load data file into a dataframe
    df = pd.read_csv(filename)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    try:
        df['Gender'].fillna('Not Available', inplace=True)
    except KeyError:
        pass

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe

        day = DAYS.index(day)
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """
    Args:
        df - Pandas DataFrame containing filtered data

    Returns:
        Time Statistics -> Most common month of travel, Most Common Day of Week of travel,
        Most Common Hour of Travel, and time taken for the processing. """

    start_time = time.time()

    comm_month = cal.month_name[df['month'].mode()[0]]
    comm_dow = cal.day_name[df['day_of_week'].mode()[0]]
    comm_hour = df['Start Time'].dt.hour.mode()[0]
    time_taken = time.time() - start_time

    return comm_month, comm_dow, comm_hour, time_taken


def station_stats(df):
    """
    Args:
        df - Pandas DataFrame containing filtered data

    Returns:
        Station Statistics -> Most Common Starting Station, Most Common Ending Station, Most Common Station Combination,
        and time taken for the processing. """

    start_time = time.time()

    comm_s_stn = df['Start Station'].mode()[0]
    comm_e_stn = df['End Station'].mode()[0]
    df['combo station'] = df['Start Station'] + ' -> ' + df['End Station']
    comm_b_stn = df['combo station'].mode()[0]
    time_taken = time.time() - start_time

    return comm_s_stn, comm_e_stn, comm_b_stn, time_taken


def trip_duration_stats(df):
    """
    Args:
        df - Pandas DataFrame containing filtered data
    Returns:
        Trip Duration Statistics -> Total time of travel, average trip duration, and time taken for the processing."""

    start_time = time.time()
    total_time = df['Trip Duration'].sum()
    avg_time = df['Trip Duration'].mean()
    time_taken = time.time() - start_time
    return total_time, avg_time, time_taken


def user_stats(df):
    """
    Args:
        df - Pandas DataFrame containing filtered data
    Returns (if available):
        User Statistics -> Gender Split of Users, Minimum Year of Birth,
        Most Recent year of Birth, Most Common Year of Birth and time taken for the processing."""

    start_time = time.time()

    try:
        count_by_gender = df['Gender'].value_counts().sort_index(ascending=True)
    except KeyError:
        count_by_gender = 'No Gender Data available for this City'

    try:
        min_yob = df['Birth Year'].min()
        max_yob = df['Birth Year'].max()
        comm_yob = df['Birth Year'].mode()[0]
    except KeyError:
        min_yob = None
        max_yob = None
        comm_yob = None
    time_taken = time.time() - start_time

    return count_by_gender, min_yob, max_yob, comm_yob, time_taken


def render_result(df):
    """ Calls the individual methods and Prepares data to be consumed by the final html
    Args:
        df - Pandas DataFrame containing filtered data
    Returns:
        result_dict - A dictionary of dictionaries containing all information required for the user"""
    result_dict = {}

    comm_month, comm_dow, comm_hour, time_taken_ts = time_stats(df)
    result_dict['Time Statistics'] = {'Most Common Month of Travel: ': comm_month,
                                      'Most Common Day of Travel: ': comm_dow,
                                      'Most Common Hour of Travel: ': comm_hour,
                                      'Time Taken:': time_taken_ts}

    comm_s_stn, comm_e_stn, comm_b_stn, time_taken_ss = station_stats(df)
    result_dict['Station Statistics'] = {'Most Common Starting Station:': comm_s_stn,
                                         'Most Common Ending Station:': comm_e_stn,
                                         'Most Common Start -> End Station Combination:': comm_b_stn,
                                         'Time Taken:': time_taken_ss}

    total_time, avg_time, time_taken_tds = trip_duration_stats(df)
    result_dict['Trip Duration Statistics'] = {'Total Time of Travel (in seconds): ': total_time,
                                               'Average Time of Travel per trip (in seconds): ': avg_time,
                                               'Time Taken:': time_taken_tds}

    count_by_gender, min_yob, max_yob, comm_yob, time_taken_us = user_stats(df)
    # Check if gender and birth year data is available and handle it
    try:
        p_count_by_gender = count_by_gender.to_string()
    except:
        p_count_by_gender = 'No Gender Data available for this City'

    # Check if Birth Year data is available and handle it
    if min_yob:
        min_yob = int(min_yob)
        max_yob = int(max_yob)
        comm_yob = int(comm_yob)
    else:
        min_yob = 'No Birth Year Data available for this City'
        max_yob = 'No Birth Year Data available for this City'
        comm_yob = 'No Birth Year Data available for this City'

    result_dict['User Statistics'] = {'Gender Split: ': p_count_by_gender,
                                      'Minimum Year of Birth: ': min_yob,
                                      'Most Recent Year of Birth: ': max_yob,
                                      'Most Common Year of Birth: ': comm_yob,
                                      'Time Taken:': time_taken_us}

    return result_dict


def main():
    pd.set_option("display.max_columns", 20)

    city, month, day = 'Washington', 'All', 'All'
    df = load_data(city, month, day)
    print(df.head())
    r_dict = render_result(df)
    print(r_dict)

    city, month, day = 'Chicago', 'All', 'Sun'
    df = load_data(city, month, day)
    print(df.head())
    r_dict = render_result(df)
    print(r_dict)

    city, month, day = 'New York City', 'All', 'All'
    df = load_data(city, month, day)
    print(df.head())
    r_dict = render_result(df)
    print(r_dict)


if __name__ == "__main__":
    main()

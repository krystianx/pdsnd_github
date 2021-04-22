import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')


    while True:
        try:
            city = str(input('Which city would you like to explore? \nOptions are Chicago, New York City or Washington \n').lower())
            CITY_DATA[city]
            break
        except KeyError:
            print('\nThat\'s \033[4mnot\033[0m a listed city. \nPlease check spelling!')

    while True:
        try:
            month = str(input('Which month would you like to explore? \nOptions are January through June or All \n').lower())
            if not month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
                raise NameError("User entry is not in allowed list of months")
            break
        except NameError:
            print("\nUser entry is \033[4mnot\033[0m in allowed list of months. Please try again!")

    while True:
        try:
            day = str(input('Which day would you like to explore? \nOptions are Sunday through Saturday or All \n').lower())
            if not day in ['sunday','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']:
                raise NameError("User entry is not in allowed list of days of the week. \nPlease check spelling!")
            break
        except NameError:
            print("\nUser entry is \033[4mnot\033[0m in allowed list of days of the week. Please try again!")

    print('-'*40)
    return city, month, day


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    # This is when the calculation started
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month

    # find the most popular hour
    popular_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('Most Popular Start Month: {}'.format(months[popular_month-1].title()))

    df['dow'] = df['Start Time'].dt.weekday_name

    popular_dow = df['dow'].mode()[0]
    print('Most Popular Day of the Week: {}'.format(popular_dow))

    df['hour'] = df['Start Time'].dt.hour

    popular_hour = df['hour'].mode()[0]
    popular_hour_conv = pd.to_datetime(popular_hour,  format='%H').strftime("%I:00 %p")
    print('Most Popular Hour: {}'.format(popular_hour_conv))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_startstation = df['Start Station'].mode()[0]
    print('Most Popular Start Station: {}'.format(popular_startstation))

    popular_endstation = df['End Station'].mode()[0]
    print('Most Popular End Station: {}'.format(popular_endstation))

    df['combotrip'] = df['Start Station'] + ' to ' + df['End Station']
    popular_trip = df['combotrip'].mode()[0]
    print('Most Popular Trip: {}'.format(popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['totaltime'] = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])

    total_time = df['totaltime'].sum()
    print('The total travel time across this dataset is: {}'.format(total_time))

    mean_time = df['totaltime'].mean()
    days, seconds = mean_time.days, mean_time.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    print(mean_time)
    print('The average travel time in this dataset is: {} hours, {} minutes and {} seconds'.format(hours, minutes, seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('What is the breakdown of users?\n')
    print(df['User Type'].value_counts(ascending=False))

    print('\nWhat is the breakdown by gender?\n')
    try:
        print(df['Gender'].value_counts(ascending=False))
    except KeyError:
        print('There is no information in data set about Gender')

    print('\nWhat is the breakdown by age?\n')
    try:
        max_age = df['Birth Year'].min()
        min_age = df['Birth Year'].max()
        common_age = df['Birth Year'].mode()[0]
        print('The oldest user was born in {}'.format(int(max_age)))
        print('The youngest user was born in {}'.format(int(min_age)))
        print('The most common birth year is {}'.format(int(common_age)))
    except KeyError:
        print('There is no information in data set about birth year')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Asks user if they would like to see a subset of the data."""
    i = 0
    while True:
        try:
            x = str(input('Would you like to see a subset of the data? yes/no \n'))
            if not x in ['yes', 'no']:
                raise NameError("Did not answer yes or no")
            if x == 'yes':
                print(df.iloc[i:i+5])
                i += 5
            break
        except NameError:
            print("\nPlease respond in \033[4myes\033[0m or \033[4mno\033[0m!")
    if x == 'yes':
        while True:
            try:
                x = str(input('Would you like to see another 5 rows? yes/no \n'))
                if not x in ['yes', 'no']:
                    raise NameError("Did not answer yes or no")
                if x == 'yes':
                    if i >= df.shape[0]:
                        raise LookupError('Out of Data')
                    print(df.iloc[i:i+5])
                    i += 5
                if x == 'no':
                    break
            except NameError:
                print("\nPlease respond in \033[4myes\033[0m or \033[4mno\033[0m!")
            except LookupError:
                print('Out of Data!')
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

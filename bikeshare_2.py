import time
import pandas as pd
import numpy as np

CITY_DATA = {'Chicago': 'chicago.csv',
             'New York City': 'new_york_city.csv',
             'Washington': 'washington.csv'}


def get_filters():
    while True:
        city = input("enter the city name\n1] chicago\n2] new york city\n3] washington\n").title()
        if city not in ('New York City', 'Chicago', 'Washington'):
            print("---------------invaild input try again------------")
            continue
        else:
            break

    while True:
        month = input(
            "\nWhich month would you like to filter by? January, February, March, April, May, June or type 'all' if you do not have any preference?\n")
        print(
            "--------------------------------------------------------------------------------------------------------------------")
        if month not in ('January', 'February', 'March', 'April', 'May', 'June', 'all'):
            print("---------------invaild input try again------------")
            continue
        else:
            break

    while True:
        day = input(
            "\nAre you looking for a particular day? If so, kindly enter the day as follows: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type 'all' if you do not have any preference.\n")
        print(
            "------------------------------------------------------------------------------------------------------------------------")
        if day not in ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'all'):
            print("---------------invaild input try again------------")
            continue
        else:
            break

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = df['month'].mode()[0]
    print('Most Common Month:', popular_month)

    popular_day = df['day_of_week'].mode()[0]
    print('Most Common day:', popular_day)

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    Start_Station = df['Start Station'].value_counts().idxmax()
    print('common start station:', Start_Station)

    End_Station = df['End Station'].value_counts().idxmax()
    print('\nCommon end station:', End_Station)

    most_common_combination = df['Start Station'] + ' to ' + df['End Station']
    print('The most popular combination is: {}'.format(most_common_combination.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    Total_Travel_Time = sum(df['Trip Duration'])
    print('Total travel time in minutes:', Total_Travel_Time)

    Mean_Travel_Time = df['Trip Duration'].mean()
    print('Mean travel time:', Mean_Travel_Time, " Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()

    print('User Types:\n', user_types)
    if 'Gender' not in df:
        print('Sorry! Gender data unavailable for Washington')
    else:
        print('The genders are \n{}'.format(df['Gender'].value_counts()))
    if 'Birth Year' not in df:
        print('Sorry! Birth year data unavailable for Washington')
    else:
        print('The Earliest birth year is: {}'.format(df['Birth Year'].min()))
        print('The most recent birth year is: {}'.format(df['Birth Year'].max()))
        print('The most common birth year is: {}'.format(df['Birth Year'].mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def view_data(df):
    start = 0
    choice = input('\nDo you want to view the data? Enter yes or no.\n')
    while choice == 'yes':
        try:
            n = int(input('Enter the number of rows to view\n'))
            n = start + n
            print(df[start:n])
            choice = input('More rows? Enter yes or no.\n')
            start = n

        except ValueError:
            print('Enter appropriate integer value')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

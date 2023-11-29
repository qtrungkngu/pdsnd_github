import time
import pandas as pd
import numpy as np
 
 
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}
MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
 
 
def input_data(promptMsg, validData):
    """
    Asks user to input a data.
    Parrams:
        (str) promptMsg - The prompt message
        (collection) validData - valid data collection
    Returns:
        (str) data - the input data
    """
 
    rslt = ''
    while rslt not in validData:
        # Prompt the user for input
        rslt = input("%s, or 'x' to exit: " % promptMsg).lower().strip()
        # Allow user to exit the programe any time they want
        if rslt == 'x':
            exit()
 
        # Check if the input is valid
        if rslt not in validData:
            print("Invalid input. Please try again.")
 
    return rslt
 
 
def print_horizontal_line():
    """Print a horizontal line with symbol `=`."""
    print('=' * 40)
 
 
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
 
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = month = day = ""
 
    # Get user input for city (chicago, new york city, washington)
    city = input_data("Enter a city (Chicago, New York City, Washington)", CITY_DATA)
 
    # Get user input for month (all, january, february, ... , june)
    month = input_data("Enter a month (all, January, February, ..., June)", MONTHS)
 
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = input_data("Enter a day (all, Monday, Tuesday, ..., Sunday)", DAYS)
 
    print_horizontal_line()
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
    fileName = './' + CITY_DATA[city]
    data = pd.read_csv(fileName)
    data["Start Time"] = pd.to_datetime(data["Start Time"])
    if month != "all":
        print("Filter data by month {}...\n".format(month.capitalize()))
        data = data[data["Start Time"].dt.month == MONTHS.index(month)]
 
    if day != "all":
        print("Filter data by day of week {}...\n".format(day.capitalize()))
        data = data[data["Start Time"].dt.dayofweek == DAYS.index(day)]
 
    df = pd.DataFrame(data)
    return df
 
 
def log_time_spent(startTime):
    """Display the time spent. For readability, it is highlighted to miliseconds."""
    spentTime = str(time.time() - startTime)
    highlightedSpentTime = "\033[1;37m" + spentTime[:5] + "\033[0m" + spentTime[5:]
    print("\nThis took " + highlightedSpentTime + " seconds.")
 
 
def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""
 
    print('\nCalculating The Most Frequent Times of Travel...\n')
    startTime = time.time()
 
    # Display the most common month (only when not specified a month).
    if month == "all":
        monthCounts = df["Start Time"].dt.month.value_counts()
        mostCommonMonthIndex = monthCounts.idxmax()
        print("The most common month: ", MONTHS[mostCommonMonthIndex].capitalize())
 
    # Display the most common day of week (only when not specified a day)
    if day == "all":
        countsByDay = df["Start Time"].dt.dayofweek.value_counts()
        mostCommonDayIndex = countsByDay.idxmax()
        print("The most common day of week:", DAYS[mostCommonDayIndex].capitalize())
 
    # Display the most common start hour
    startHourCounts = df["Start Time"].dt.hour.value_counts()
    mostCommonHour = startHourCounts.idxmax()
    print("The most common hour:", mostCommonHour)
 
    # Display the time spent.
    log_time_spent(startTime)
 
    print_horizontal_line()
 
 
def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    startTime = time.time()
 
    # Display most commonly used start station
    popularStartStation = df['Start Station'].mode()[0]
    print('Most commonly used start station:', popularStartStation)
 
    # Display most commonly used end station
    popularEndStation = df['End Station'].mode()[0]
    print('Most commonly used end station:', popularEndStation)
 
    # Display most frequent combination of start station and end station trip
    stationCombination = (df['Start Station'] + ", " + df['End Station'])
    mostFrequentCombination = stationCombination.mode()[0]
    print('Most frequent combination of start station and end station trip:', mostFrequentCombination)
 
    log_time_spent(startTime)
    print_horizontal_line()
 
 
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
 
    print('\nCalculating Trip Duration...\n')
    startTime = time.time()
    df['Trip Duration'] = df['Trip Duration'].astype('int')
 
    # Display total travel time
    totalTravel = df['Trip Duration'].sum()
    print("Total travel time(seconds): ", totalTravel)
 
    # Misplay mean travel time
    meanTravel = df['Trip Duration'].mean()
    print("Mean travel time(seconds): ", meanTravel)
 
    log_time_spent(startTime)
    print_horizontal_line()
 
 
def user_stats(df):
    """Displays statistics on bikeshare users."""
 
    print('\nCalculating User Stats...\n')
    startTime = time.time()
 
    # Display counts of user types
    userTypesCount = df["User Type"].value_counts()
    print("User types count:\n", userTypesCount.to_string(index = True, dtype = False))
    print("\n")
 
    # Display counts of gender
    try:
        gendersCount = df['Gender'].value_counts()
        print("Genders count:\n", gendersCount.to_string(index = True, dtype = False))
    except Exception:
        print("Genders count: N/A")
 
    print("\n")
 
    # Display earliest, most recent, and most common year of birth
    try:
        birthYear = df['Birth Year']
        earliest = birthYear.min()
        mostRecent = birthYear.max()
        mostCommon = birthYear.mode()[0]
    except Exception:
        earliest = mostRecent = mostCommon = "N/A"
    finally:
        print("Earliest year of birth: ", earliest)
        print("Most recent year of birth: ", mostRecent)
        print("Most common year of birth: ", mostCommon)
 
    log_time_spent(startTime)
    print_horizontal_line()
def display_data(df):
    """Display raw data upon request by user
 
    Args:
        df (DataFrame): DataFrame of csv file
    """
 
    linesPerChunk = 5
    currentLine = 0
    displayData = input("Would you like to see the data? Type 'y' or 'n': ")
    if ('y' != displayData.lower()):
        return
 
    while currentLine < len(df):
        # Print the next chunk of data
        for index, row in df[currentLine:currentLine + linesPerChunk].iterrows():
            print(row.to_string(index = True, dtype = False))
            print("\n")
        currentLine += linesPerChunk
 
        # Check for user input
        userInput = input("Press Enter to continue or 'x' to stop: ")
        if userInput.lower() == "x":
            return
 
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
 
        restart = input("\nWould you like to restart? Enter 'y' or 'n'.\n")
        if restart.lower() != 'y':
            break
 
 
if __name__ == "__main__":
	main()
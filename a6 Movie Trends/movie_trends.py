# top_level_script
from apikeys import TMDB_KEY
import numpy as np
import pandas as pd
import requests
from bokeh.plotting import figure, output_file, show
from bokeh.models.tickers import FixedTicker
import calendar

api_key = TMDB_KEY

# Analysis-1 - Genre by Season - sabhas2 - starts


def fetch_genres():
    """
    Function Description
    -------------
    Fetches Genre Id and Genre Name for all the genres 
    Returns
    --------
    data: JSON formatted data extracted from API
    """
    # base url for the TMDb API
    base_uri = 'https://api.themoviedb.org/3/genre/movie/list'
    query_params = {'api_key': api_key}
    response = requests.get(base_uri, params=query_params)
    if response.status_code == 200:
        data = response.json()
    else:
        print('Error in getting data from API')
        exit()

    return data


def find_releases_pergenre_permonth(genre, month, year=2017):
    """
    Function Description
    -------------
    Fetches Movies data for a particular genre, release year and release month

    Input
    ------------------
    genre: genre of movie
    month: month the movie was released in
    year: year the movie was released in
    Returns
    --------
    data: JSON formatted data extracted from API
    """
    num_days_in_month = calendar.monthrange(year, month)[1]
    start_date = str(year)+'-'+str(month)+'-1'
    end_date = str(year)+'-'+str(month)+'-'+str(num_days_in_month)
    # base url for the TMDb Discover API
    base_uri = 'https://api.themoviedb.org/3/discover/movie'
    query_params = {'api_key': api_key,
                    'with_genres': genre,
                    'primary_release_year': year,
                    'year': year,
                    'primary_release_date.gte': start_date,
                    'primary_release_date.lte': end_date,
                    'release_date.gte': start_date,
                    'release_date.lte': end_date}
    response = requests.get(base_uri, params=query_params)
    if response.status_code == 200:
        data = response.json()
    else:
        print('Error in getting data from discover API')
        exit()

    return data


def get_total_releases(user_input, year=2017):
    """
    Function Description
    -------------
    Fetches Movies data each month and genre and returns a data structure with number of releases, genre and month

    Input
    ------------------
    user_input: Genres entered by the user
    year: year the movie was released in
    Returns
    --------
    dict_genres_final: Dictionary of lists of dictionaries of number of releases for each genre and month 
    """
    dict_genres_final = {}

    # extracting all genre ids and genre names
    dict_genres = fetch_genres()

    # if user has entered genres pick them otherwise consider default genres
    if user_input[0] == 'N' or user_input[0] == 'n':
        genres = ['Action', 'Comedy', 'Thriller', 'Drama', 'Family']
    else:
        genres = user_input

    # filter dictionary data of genre id and genre name for only the 5 genres taken
    dict_updated_genres = [genre_id_name for genre in genres for genre_id_name in dict_genres['genres']
                           if genre.strip().capitalize() in genre_id_name['name']]

    # create mapping for month numbers and months
    month_mapping = {k: v for k, v in enumerate(calendar.month_abbr)}

    for genre in dict_updated_genres:
        list_releases_for_genre = []
        for num_month in range(1, 13):
            # extract data for each genre and month
            movies_data = find_releases_pergenre_permonth(
                genre['id'], num_month, year)

            # Add progress bar
            print(".", flush=True, end="")

            # create dictionary for genre name, month number and number of releases
            movie_releases = {'genre': genre['name'], 'month_num': num_month,
                              'month': month_mapping[num_month], 'num_of_releases': movies_data['total_results']}
            list_releases_for_genre.append(movie_releases)
        # creating a dictionary of lists of dictionaries
        dict_genres_final[genre['name']] = list_releases_for_genre

    return dict_genres_final


def visualization_genre_by_season(dict_release_overview, year=2017):
    """
    Function Description
    -------------
    Uses the Bokeh library to plot the monthly distribution of films by genre

    Input
    ------------------
    dict_release_overview : A dictionary of lists of dictionaries that has number of releases for each genre and month
    """
    month_mapping = {k: v for k, v in enumerate(calendar.month_abbr)}
    month_mapping.pop(0)

    p = figure(title='Releases by Genre: {}'.format(year),
               x_axis_label='Months', y_axis_label='Releases')

    max_v, count = 0, 0
    colors = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99']

    for genre, list_releases in dict_release_overview.items():
        x, y = [], []
        # add month numbers in x and corresponding number of releases on y axis for the genre
        for dict_release in list_releases:
            x.append(dict_release['month_num'])
            y.append(dict_release['num_of_releases'])
            if dict_release['num_of_releases'] > max_v:
                max_v = dict_release['num_of_releases']

        # add a line renderer with legend and line thickness
        p.line(x, y, legend=genre, line_width=2, color=colors[count])
        p.xaxis.major_label_overrides = month_mapping

        # Defining X ticks
        p.xaxis.ticker = FixedTicker(ticks=list(month_mapping.keys()))
        p.xgrid.ticker = FixedTicker(ticks=list(month_mapping.keys()))

        # Defining y ticks
        p.yaxis.ticker = FixedTicker(ticks=np.arange(0, max_v+50, 50))
        p.ygrid.ticker = FixedTicker(ticks=np.arange(0, max_v+50, 50))

        p.y_range.end = max_v+50
        count = count+1

    # output to static HTML file
    output_file('genre_by_season.html')

    show(p)
# Analysis-1 - Ends


# Analysis-2 - Actor Popularity - sahil - starts

def movies_of_actor(name):
    """
    Function Description
    -------------
    Searches the TMDB database using the search API and returns the actor ID for the passed actor name.
    From that Actor ID finds the actors filmography using the discover API.

    Input
    ------------------
    name : Name of the actor

    Returns
    --------
    flat_list_movies : A list of movies for that actor.
    """
    name = name.replace(
        ' ', '+')  # split user name based on space and add + for query parameter
    # base url for the TMDb search API
    base_url_search_api = 'https://api.themoviedb.org/3/search/person'

    query_parameter_search_api = {'query': name, 'api_key': api_key}

    # base url for the TMDb discover API
    base_url_discover_api = 'https://api.themoviedb.org/3/discover/movie'

    # Requesting data from the search API with actor name as query
    response_actorID = requests.get(
        base_url_search_api, query_parameter_search_api)

    # Check for successful response
    if(response_actorID.status_code == 200):

        known_for_films = response_actorID.json()  # Convert from json into a list

        # Extract data from results key of the list returned
        res = known_for_films['results']
        actor_id = res[0]['id']  # Extract actor ID from results

        query_parameter_discover_api = {
            'with_people': actor_id, 'api_key': api_key}
        # requesting discover API for movies for particular actor ID
        response_movieIDs = requests.get(
            base_url_discover_api, query_parameter_discover_api)

        # Check for successful response
        if(response_movieIDs.status_code == 200):
            films = response_movieIDs.json()
            results = films['results']  # Appending results to list

            # Check for results on pages after Page 1
            for i in range(2, films['total_pages']+1):
                query_parameter_discover_api = {
                    'with_people': actor_id, 'api_key': api_key, 'page': i}
                response = requests.get(
                    base_url_discover_api, query_parameter_discover_api)
                films1 = response.json()
                results.extend(films1['results'])  # Appending results to list
        else:
            print('Error in getting data from discover API')
    else:
        print("Please enter in correct format -- FirstName<space>LastName")

    return results


def popularity_of_actor(list_of_movies):
    """
    Function Description
    -------------
    Searches the TMDB database for movies related metadata for each movie from
    the list of passed movies for a particular  actor. Populates a dataframe with
    movie name, release year, budget, revenue and profit. Also filters for rows with
    0 as revenue or budget to avoid outliers.

    Input
    ------------------
    list_of_movies : List of movies of the actor requested by the user

    Returns
    --------
    popularity_per_year : A dataframe with each movie's metadata enacted by that actor.
    """

    # Base URL to search movies
    base_url = 'https://api.themoviedb.org/3/movie/'

    # Defining a dataframe to store movie metadata
    columns = ['film', 'release_date', 'revenue', 'budget']
    revenue_df = pd.DataFrame(columns=columns)

    # For each movie retreive metadata and populate dataframe
    for film in list_of_movies:
        query_paramter = {'api_key': api_key}

        film_revenue = requests.get(
            base_url + str(film['id']), query_paramter)
        # Add progress bar
        print(".", flush=True, end="")
        film_revenue = film_revenue.json()

        revenue_df.loc[len(revenue_df)] = [film_revenue['title'], film_revenue['release_date'],
                                           film_revenue['revenue'], film_revenue['budget']]

    # Defining profit for each movie
    revenue_df['Profit'] = revenue_df['revenue'] - revenue_df['budget']

    revenue_df.sort_values(by='Profit', ascending=False)

    # Retrieving year of release from release_date
    revenue_df['Year'] = [i[0:4] for i in revenue_df.release_date]

    # Removing values=0 from the dataframe
    revenue_df['Year'].replace('', np.nan, inplace=True)  # replace 0 with nan
    revenue_df.dropna(subset=['Year'], inplace=True)  # drap nan

    revenue_df['revenue'].replace(
        0, np.nan, inplace=True)  # replace 0 with nan
    revenue_df.dropna(subset=['revenue'], inplace=True)  # drap nan

    # New dataframe with just year of release and profit for a movie
    popularity_per_year = revenue_df[["Year", 'Profit']]

    popularity_per_year = popularity_per_year.reset_index(level=0)
    popularity_per_year = popularity_per_year.sort_values(by='Year')

    return popularity_per_year


def visualization_actors_popularity(popularity_per_year, name):
    """
    Function Description
    -------------
    Uses the Bokeh library to plot the popularity of each movie in the actor's career over time.

    Input
    ------------------
    popularity_per_year : A dataframe with each movie's metadata enacted by that actor.
    """
    # output to static HTML file
    output_file("actor_popularity.html")

    # create a new plot with a title and axis labels
    p = figure(title=name+" Popularity over Time",
               x_axis_label='Date', y_axis_label='Revenue($)', y_range=(-(1e8), 5e8))

    # add a line renderer with legend and line thickness
    p.line(popularity_per_year['Year'],
           popularity_per_year['Profit'], line_width=2)

    # Defining X ticks
    p.xaxis.ticker = FixedTicker(ticks=np.arange(1985, 2020, 5))
    p.xgrid.ticker = FixedTicker(ticks=np.arange(1985, 2020, 5))

    # show the results
    show(p)

# Analysis-2 - Ends

# MAIN block


def main():
    # prompt the user for analysis 1 or analysis 2
    u_input = input("Which task do you want to analyze: \nA. Distribution of Film releases of different Genre?"
                    + "\nB. Popularity of a particular actor's films over that actor's career? \n\nEnter 'A' or 'B'")

    if u_input == 'A' or u_input == 'a':

        # call for analysis 1
        # prompt the user for a list of genres
        s = input("Enter genres(at maximum of 10) separated by commas." +
                  "\nPress 'N' if you want to analyze default genres - 'Action', 'Comedy', 'Thriller', 'Drama', 'Family': ")
        user_input = s.split(',')

        dict_release_overview = get_total_releases(user_input, year=2017)
        visualization_genre_by_season(dict_release_overview, year=2017)

    elif u_input == 'B' or u_input == 'b':
        # call for analysis 2
        # prompt the user for an actor name
        name = input('Please name the Actor you want to visualize? ')
        list_of_movies = movies_of_actor(name)
        popularity_per_year = popularity_of_actor(list_of_movies)
        visualization_actors_popularity(popularity_per_year, name)


if __name__ == "__main__":
    main()

# MAIN block ends

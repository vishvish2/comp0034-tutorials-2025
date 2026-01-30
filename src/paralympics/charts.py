import requests
import pandas as pd
import plotly.express as px


def get_api_data(url):
    """ Gets the JSON data from the mock_api REST API

    Args:
        url: URL for the REST API route, e.g. http://127.0.0.1:8000/all

    Returns:
        df: DataFrame with the data
    """
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    return df


def line_chart(feature):
    """ Creates a line chart

    Data is displayed over time from 1960 onwards.
    The figure shows separate trends for the winter and summer events.

     Args:
        feature (str): events, sports, countries, or participants

     Returns:
        fig: Plotly Express line figure

     Raises:
         ValueError: If the feature is not one of the valid options
     """
    if feature not in ["sports", "participants", "events", "countries"]:
        raise ValueError(
            'Invalid value for "feature". Must be one of ["sports", "participants", "events", "countries"]')
    else:
        # Make sure it is lowercase to match the dataframe column names
        feature = feature.lower()

    # Get the data from the REST API using the get_api_data() function you just created
    df = get_api_data("http://127.0.0.1:8000/all")

    # Only the columns needed for this chart
    chart_df = df[["event_type", "year", feature]]

    # Create a Plotly Express line chart with the following parameters
    #    chart_df is the DataFrame
    #    x="year" is the column to use as the x-axis
    #    y=feature is the column to use as the y-axis
    #    color="event_type" indicates if winter or summer
    fig = px.line(chart_df, x="year", y=feature, color="event_type")
    return fig


def bar_chart(event_type):
    """
    Creates a stacked bar chart showing change in the ration of male and female competitors in the summer and winter paralympics.

    Parameters
    event_type: str Winter or Summer

    Returns
    fig: Plotly Express bar chart
    """
    df = get_api_data("http://127.0.0.1:8000/all")
    needed = ['event_type', 'year', 'place_name', 'participants_m', 'participants_f',
              'participants']
    df_plot = (
        df[needed]
        .dropna(subset=['participants_m', 'participants_f'])
        .query("event_type == @event_type")
        .assign(  # Avoid divide-by-zero; if participants==0, set NaN, then drop
            Male=lambda d: d['participants_m'].where(d['participants'] != 0, pd.NA) / d[
                'participants'],
            Female=lambda d: d['participants_f'].where(d['participants'] != 0, pd.NA) / d[
                'participants'],
            xlabel=lambda d: d['place_name'] + " " + d['year'].astype(str), )
        .dropna(subset=['Male', 'Female'])
        .sort_values(['event_type', 'year'])
    )

    fig = px.bar(df_plot,
                 x='xlabel',
                 y=['Male', 'Female'],
                 title=f'How has the ratio of female:male participants changed in the {event_type} paralympics?',
                 labels={'xlabel': '', 'value': '', 'variable': ''},
                 template="simple_white"
                 )
    fig.update_xaxes(ticklen=0)
    fig.update_yaxes(tickformat=".0%")
    return fig


def scatter_map():
    """ Creates a scatter chart with locations of all Paralympics

    Returns:
        fig: Plotly Express scatter geo figure
    """

    # Prepare the data
    df = get_api_data("http://127.0.0.1:8000/all")
    chart_df = df[["year", "place_name", "latitude", "longitude"]]
    # The lat and lon must be floats for the scatter_geo
    chart_df['longitude'] = chart_df['longitude'].astype(float)
    chart_df['latitude'] = chart_df['latitude'].astype(float)
    # Add a new column that concatenates the place_name and year e.g. Barcelona 2012
    chart_df['name'] = chart_df['place_name'] + ' ' + chart_df['year'].astype(str)

    # Create the figure
    fig = px.scatter_geo(chart_df,
                         lat=chart_df.latitude,
                         lon=chart_df.longitude,
                         hover_name=chart_df.name,
                         title="Where have the paralympics been held?"
                         )
    return fig


if __name__ == '__main__':
    fig_sport = line_chart("sports")
    fig_sport.show()
    fig_part = line_chart("participants")
    fig_part.show()
    fig_sport_bar = bar_chart("Winter")
    fig_sport_bar.show()
    fig_part_bar = bar_chart("Summer")
    fig_part_bar.show()
    fig_sport_scatter = scatter_map()
    fig_sport_scatter.show()

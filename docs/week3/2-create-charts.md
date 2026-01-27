# 2. Create charts using Plotly Express

In this activity you will create the three charts that you added the selectors for in week 2's
activities:

1. A line chart with a dropdown to select variants ("sports", "events", "counties", "participants")
2. A bar chart showing the change in male/female participants in summer and winter Paralympics. This
   has a checkbox selector for Winter and/or Summer.
3. A map with points showing where each of the Paralympics has been held.

## Create a line chart

Create
a [Plotly Express line chart](https://plotly.com/python-api-reference/generated/plotly.express.line.html)
that displays for each paralympics the total number of events, competitors and sports. The data will
be displayed from 1960 through to 2022.

The data attributes needed are:
`["type", "year", "host", "events", "sports", "participants", "countries"]`.

Create a function to create the line chart. The function should take a parameter that accepts
whether the chart should display events, sports or participants. For example:

```python
import plotly.express as px


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
```

You won't see anything as this is just a function.

Check the chart by creating one or more instances and run the code in `chart.py` e.g. add a
temporary section:

```python
if __name__ == '__main__':
    fig_sport = line_chart("sports")
    fig_sport.show()
    fig_part = line_chart("participants")
    fig_part.show()
```

### (Optional) Add styling

Refer to the [documentation for styling Express](https://plotly.com/python/styling-plotly-express/).

Amend the code that creates the line chart to:

1. Set the figure title to `How has the number of {feature} changed over time?`:
   `title=f"How has the number of {feature} changed over time?"`
2. Change the axis labels to remove the word 'feature' from the Y axis and change the X axis label
   to start with a capital letter: e.g.
   ```python
   labels = { 
                 "feature": "",
                 "year": "Year"
             }
   ```
3. Use a template to apply a more simple style that has no background, e.g.,
   `template="simple_white"`

## Create a bar chart

Create a
stacked [bar chart](https://plotly.com/python-api-reference/generated/plotly.express.bar.html) that
shows the
ratio of female:male competitors for either winter or summer events.

Add the code to create a bar chart:

```python
import plotly.express as px


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
```

### (Optional) Add styling

Try and change some of the [styling options](https://plotly.com/python/styling-plotly-express/) of
the bar chart e.g. change the colour of the bars with `color_discrete_map={'Male': 'blue', 'Female': 'green'}`.

## Create the map

Create
a [Plotly Express Scatter Map](https://plotly.com/python/tile-scatter-maps/),
a world map with markers to show the locations of the Paralympics.

The map requires the latitude and longitude of each Paralympic Games. These have been added to the SQLite
database in the `host`table.

```python
import plotly.express as px


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
```

### (Optional) Style the markers

Styling the markers requires Plotly Go syntax.
Refer to the [Plotly maps documentation](https://plotly.com/python/scatter-plots-on-maps/) if you
want to try to change the marker styles.

## (Optional) Create your own chart

Look at the [Plotly charts selector](https://plotly.com/python/) and try to create another chart.

## Next activity

The next activity varies by framework:

[Next activity – Dash](3-add-charts-dash.md)

[Next activity – Flask](3-add-charts-flask.md)

[Next activity – Streamlit](3-add-charts-streamlit.md)
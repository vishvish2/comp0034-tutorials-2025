from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Sample map data
df = pd.DataFrame({
    "lat": [51.5074, 48.8566, 40.7128],
    "lon": [-0.1278, 2.3522, -74.0060],
    "city": ["London", "Paris", "New York"],
    "description": [
        "Capital of the United Kingdom",
        "Capital of France",
        "Largest city in the United States"
    ],
    "population": ["8.9M", "2.1M", "8.3M"]
})

fig = px.scatter_map(
    df,
    lat="lat",
    lon="lon",
    hover_name="city",
    hover_data=["population"],
    custom_data=["description", "population"],  # used in callback
    zoom=1,
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin={"l": 0, "r": 0, "t": 0, "b": 0},
)


# App and Layout

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="map", figure=fig),
                    width=8
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("City Information"),
                            dbc.CardBody(
                                id="hover-card",
                                children="Hover over a point on the map."
                            )
                        ],
                        style={"width": "100%"}
                    ),
                    width=4
                )
            ],
            className="mt-4"
        )
    ],
    fluid=True
)

# Callbacks
@app.callback(
    Output("hover-card", "children"),
    Input("map", "hoverData")
)
def update_card(hoverData):
    if hoverData is None:
        return "Hover over a point on the map."

    point = hoverData["points"][0]

    city = point["hovertext"]
    description = point["customdata"][0]
    population = point["customdata"][1]

    return [
        html.H4(city),
        html.P(description),
        html.P(f"Population: {population}")
    ]


if __name__ == "__main__":
    app.run(debug=True)

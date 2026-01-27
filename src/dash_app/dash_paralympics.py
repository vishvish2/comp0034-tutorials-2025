from io import StringIO

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, dash_table, dcc, html

from src.data.mock_api import get_event_data
from src.utils.line_chart import line_chart

# Create the app
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load the data
para_data = get_event_data()
df = pd.read_json(StringIO(para_data))
df['start'] = pd.to_datetime(df['start'], dayfirst=True)
df['end'] = pd.to_datetime(df['end'], dayfirst=True)

# Add the layout
app.layout = dbc.Container([
    html.H1(children='Paralympics Dash app'),
    html.H2("Data table"),
    dash_table.DataTable(df.to_dict('records')),
    html.H2("AG Grid table"),
    dag.AgGrid(
        rowData=df.to_dict("records"),
        columnDefs=[{"field": col} for col in df.columns]),
    html.H2("Line charts"),
    dcc.Graph(figure=line_chart("participants", df))
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

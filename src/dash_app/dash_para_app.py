import pandas as pd
# import dash_ag_grid as dag
from dash import Dash, html, dash_table, dcc
from src.data.mock_api import get_event_data
from src.utils.line_chart import line_chart

app = Dash()

para_data = get_event_data()
df = pd.read_csv('src/data/paralympic_events.csv')
df['start'] = pd.to_datetime(df['start'], dayfirst=True)
df['end'] = pd.to_datetime(df['end'], dayfirst=True)

app.layout = [
    html.H1(children='Title of Dash App'),
    dash_table.DataTable(df.to_dict('records')),
    dcc.Graph(figure=line_chart("participants", df))
]

if __name__ == '__main__':
    app.run(debug=True)

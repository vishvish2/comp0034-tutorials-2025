from io import StringIO

import pandas as pd
from flask import Flask, render_template

from src.data.mock_api import get_event_data
from src.utils.line_chart import line_chart

app = Flask(__name__)


@app.route("/")
def paralympics():
    # Get the data
    para_data = get_event_data()
    df = pd.read_json(StringIO(para_data))
    df['start'] = pd.to_datetime(df['start'], dayfirst=True)
    df['end'] = pd.to_datetime(df['end'], dayfirst=True)

    # Convert the data to a type the Jinja template will accept for the table
    data = df.to_dict('records')

    # Generate the plotly chart as HTML
    fig = line_chart("participants", df)
    plot_html = fig.to_html()

    # Render the template using the data and the chart_html
    return render_template("paralympics.html", data=data, plot_html=plot_html)

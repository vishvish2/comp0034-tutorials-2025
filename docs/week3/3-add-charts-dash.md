# 3. Adding charts to the Dash app layout

Last week you created the layout and added the dropdowns and checkboxes to select options for the
charts. This activity implements the functions that create the charts when choices are made in the
selectors.

In Dash, you will use **callback** functions for this.

[Basic callbacks](https://dash.plotly.com/basic-callbacks) documentation

[Advanced callbacks](https://dash.plotly.com/advanced-callbacks) documentation

## Introduction to Dash `callback` functions

Dash automatically calls a callback function whenever an input component's property changes. For
example, when a user makes a choice from a dropdown list or ticks a checkbox.

The basic steps for the callback function are:

- Define the input(s)
- Define the output(s)
- Write the callback function using the `@callback` decorator

With a structure like this:

```python
from dash import Input, Output


# Code omitted here that creates the app and adds the layout

# Define the callbacks after the app.layout
@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return f'Output: {input_value}'
```

You may need to refer to the [Dash callback documentation](https://dash.plotly.com/basic-callbacks).

### `@callback` decorator rules

- The decorator tells Dash to call the function for us whenever the value of the "input" component  
  e.g. a text box changes to update the children of the "output" component on the page e.g. an HTML
  div.
- Use any name for the function that is wrapped by the `@app.callback` decorator. The convention is
  that the name describes the callback output(s).
- Use any name for the function arguments, but you must use the same names inside the callback
  function as you do in its definition, just like in a regular Python function. The arguments are
  positional: first the Input items and then any State items are given in the same order as in the
  decorator.
- You must use the same `id` you gave a Dash component in the `app.layout` when referring to it as
  either an input or output of the `@app.callback` decorator.
- The `@app.callback` decorator needs to be directly above the callback function declaration. If
  there is a blank line between the decorator and the function definition, the callback registration
  will not be successful.

### Callback 'gotchas'

[callback gotchas](https://dash.plotly.com/callback-gotchas):

- Callbacks require their Inputs, States, and Output to be present in the layout
- Callbacks require all Inputs and States to be rendered on the page
- All callbacks must be defined before the server starts
- Callback definitions don't need to be in lists

## Add a `callback` for the line chart dropdown

When the dropdown is used and a selection made, display the chart for the selected option.

Input: dbc.Select with id="line-select", when a "value" is selected

Output: html.Div with id="chart-display", append to this element using the "children=" attribute

Chart function: use charts.line_chart(selected_value) to generate a 'figure', then create a
dcc.Graph() component that uses the figure e.g.
`graph = dcc.Graph(figure=charts.line_chart(selected_value))`

Together the callback would look like this:

```python
@app.callback(
    Output("chart-display", "children"),
    [Input("line-select", "value")],
)
def display_line_chart(selected_value):
    graph = dcc.Graph(figure=charts.line_chart(selected_value),
                      id=f"{selected_value}-chart"
                      )
    return graph
```

The callback must be added after the app.layout.

Check the app runs and that you can select different charts.

Do you get an error "Callback error updating `chart-display.children`" that suggested you passed the
wrong value to the `line_chart()` function? This is due to the selector initially having an empty
value. To prevent the error, at the start of the function use [
`dash.exceptions.PreventUpdate`](https://dash.plotly.com/advanced-callbacks).

```python
@app.callback(
    Output("chart-display", "children"),
    [Input("line-select", "value")],
)
def display_line_chart(selected_value):
    if not selected_value:
        raise dash.exceptions.PreventUpdate

    graph = dcc.Graph(figure=charts.line_chart(selected_value),
                      id=f"{selected_value}-chart")
    return graph
```

## Add a callback for the checkbox selector

The code is not given to you. Try to work this out yourself.

- **Input**: dbc.Checklist with id="checklist-barchart" and has a list of selected values.

- **Output**: `html.Div` with `id="chart-display"`, append to this element using the `"children="`
  attribute.
  You already have an `Output` that targets this `Div`, so you need
  to [allow duplicate outputs](https://dash.plotly.com/duplicate-callback-outputs). To do this add
  `allow_duplicate=True` to the Output in all the callbacks it is used in e.g.

    ```python
    @app.callback(
        Output("chart-display", "children", allow_duplicate=True),
        Input("line-select", "value")
    )
    ```
  You also need to add
  [Dash(prevent_initial_callbacks="initial_duplicate")](https://dash.plotly.com/duplicate-callback-outputs#setting-allow_duplicate-on-duplicate-outputs)
  on the app

    ```python
    app = dash.Dash(
        prevent_initial_callbacks="initial_duplicate",
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        ],
    )
  ```

- **Function**: The function accepts the list of selected values and creates one or more bar
  charts using these selected values. Return all the charts as a list.

## Add a callback for the initial chart selection

- **Input**: Input("select-chart", "value")
- **Output**: Output("chart-display", "children")
- **Output**: Output("selectors", "children"). Find the Div in row_one of the layout that has your
  selectors and make sure it has an id, if not add one. e.g.

```python
row_one = dbc.Row(
    [
        dbc.Col(html.Div(children=[
            # selectors go here
        ], id="selectors"), width=4),
        dbc.Col(html.Div("Charts"), width=8),
    ]
)
```

[Multiple outputs reference](https://dash.plotly.com/basic-callbacks#dash-app-with-multiple-outputs)

The **function logic** for this is:

- If the line chart is selected, then create the dbc.Select with the id="line-select" and add it to
  the selectors Div.
- If the bar chart is selected, then create the dbc.Checklist with the id="checklist-barchart" and
  add it to the selectors Div.
- If the map chart is selected, then display the chart in the "chart-display". Nothing needs to be
  added to the selectors Div.
- If no selection is made, no charts should be displayed and no selectors added.

You can move the code you created last week to create the line chart and bar chart selectors into
this function and remove the creation of them from the initial layout. Another option would be to
turn the variables into a function that you can then use e.g.

```python
def create_linechart_select():
    return dbc.Select(
        id="line-select",
        options=[
            {"label": "Sports", "value": "sports"},
            {"label": "Events", "value": "events"},
            {"label": "Counties", "value": "countries"},
            {"label": "Participants", "value": "participants"},
        ],
    )
```

I modified my first row to look like this:

```python
row_one = dbc.Row(
    [
        dbc.Col(children=[
            chart_select,  # The initial selector to choose the chart, this is always present
            html.Div(children=[], id="selectors")
            # A div to add the extra selectors dependent on chart-type
        ], width=4),
        dbc.Col(html.Div("Charts", id="chart-display"), width=8),
    ]
)
```

Try to write the solution yourself so that you understand the logic.

My solution looks like this:

```python
@app.callback(
    Output("chart-display", "children", allow_duplicate=True),
    Output("selectors", "children"),
    Input("select-chart", "value"),
)
def update_chart_display(chart_type):
    """ Updates the chart display and selectors based on the selected chart-type
    
    Args:
        chart_type (str): one of "line", "map", "bar" else empty

    Returns:
        graphs (list), selectors (list): graphs is a list of chart components, selectors is a list of selectors
        
        NB The order of the variables returned matches the order of the Outputs in the callback decorator
    """
    if not chart_type:
        raise dash.exceptions.PreventUpdate

    selectors = []
    graphs = []

    if chart_type == "line":
        line_select = create_linechart_select()
        selectors.append(line_select)
    elif chart_type == "bar":
        barchart_checklist = create_barchart_checklist()
        selectors.append(barchart_checklist)
    elif chart_type == "map":
        figure = charts.scatter_map()
        graphs.append(dcc.Graph(figure=figure, id="scatter-map"))
    else:
        raise dash.exceptions.PreventUpdate

    return graphs, selectors
```

If you run the app you will see an error `ID not found in the layout`. This is because you
are now trying to register callbacks for the line chart and the bar chart which are no longer in the
initial layout as you deleted them when you created the function above. This issue is explained with
the solution in the [callback 'gotchas'](https://dash.plotly.com/callback-gotchas).

Add `app.config.suppress_callback_exceptions = True` after the `app=Dash()` code.

Ultimately, you could combine the previous two callbacks with this into a single callback.

## App at the end of week 3

You should now have an app where the dropdowns and checkboxes work and display the selected
charts.

The code is getting quite long. You could consider restructuring it, for example, you could
structure the single app.py into `app.py` with the app instance and config and code to run the app,
`layout.py` with the layout, and `callbacks.py` with the callbacks.

See suggestions here: https://community.plotly.com/t/dash-callback-in-a-separate-file/14122/16 or
look through the [Dash sample apps code](https://github.com/plotly/dash-sample-apps/tree/main/apps).

Next week will add the question/answer feature to the app.

## (Optional) Challenge add a card

Modify the map so that when you click on a Paralympics event, a Bootstrap card is displayed that
has extra details about the event such as start date, end date, or any of the other details
available.

You can do this by accessing the `hoverData` for the map points.

There is an example in [hover_card_example.py](../../src/dash_app/hover_card_example.py), see if
you can apply something similar to the Paralympics map.

[Next activity](4-end.md)


# 3. Dash layout

## Using HTML in Dash

You will not write pure HTML files.
The [Dash HTML Components](https://dash.plotly.com/dash-html-components) API "provides pure Python
abstraction around HTML, CSS, and JavaScript. Instead of writing HTML or using an HTML templating
engine, you compose your layout using Python with the Dash HTML Components module (dash.html)"

The HTML tags supported by Dash
are [listed here](https://dash.plotly.com/dash-html-components#full-elements-reference).
An [HTML reference](https://www.w3schools.com/html/) is also useful to understand the attributes of
each tag.

The example given in the Dash documentation:

```python
from dash import html

html.Div([
    html.H1('Hello Dash'),
    html.Div([
        html.P('Dash converts Python classes into HTML'),
        html.P("This conversion happens behind the scenes by Dash's JavaScript front-end")
    ])
])
```

This equates to the following HTML:

```html

<div>
    <h1>Hello Dash</h1>
    <div>
        <p>Dash converts Python classes into HTML</p>
        <p>This conversion happens behind the scenes by Dash's JavaScript front-end</p>
    </div>
</div>
```

HTML elements can have properties such as a CSS `class` to apply styles, and `id` to uniquely
identify an element on a page. An example in Dash: 

```python
from dash import html

html.P("Some into text.", className="lead", id="intro")
```

This equates to:

```html
<p class="lead" id="intro">Some intro text</p>
```

## Create a Dash app project in your IDE

1. Create a new Python project in your IDE (VS Code, Pycharm).
2. Add .gitnore, README.md and pyproject.toml (covered in COMP0035)
3. Create and activate a Python virtual environment.
4. Install `pip install dash dash-bootstrap-components`
5. Create an `src` directory
6. Inside the `src` directory, create a Python package for the app code e.g. `paralympics`
7. Inside the `paralympics` package create a Python file for the app e.g. `app.py`
8. Inside the `paralympics` package create a folder called `assets`
9. Install the code itself as an editable package (relies on pyproject.toml) `pip install -e .`

You will have a project folder that looks like this:

```text
project_folder_name/
 ├── .venv/
 ├── src/
     └── paralympics
        ├── __init__.py
        ├── app.py
        └── assets/
├── .gitignore
├── pyproject.toml
├── README.md
```

## Create the Dash app and layout

Use the [Dash documentation](https://dash.plotly.com/layout) for more detailed explanations and
detail on the Plotly Dash
components.

### Create the Dash app and layout container

Steps for this activity:

1. Add the imports for Dash, dash.html and Dash bootstrap components (dbc).
2. Create a basic Dash app, configured to use Bootstrap via Dash Bootstrap Components.
3. The HTML to create the page layout is added using `app.layout =`.
4. Add code to run the app. The app by default runs on http://127.0.0.1:8050/

Copy and paste this into your `app.py` and run the app:

```python
# Imports for dash, Dash.html and Dash bootstrap components (dbc)
import dash
import dash_bootstrap_components as dbc
from dash import html

# Create an instance of the Dash app, define the viewport meta tag and the external stylesheet
app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)

# Add an HTML layout to the Dash app, for Bootstrap you place the layout in a container
# Wrap the layout in a Bootstrap container
app.layout = dbc.Container(children=[
    # Add the HTML layout components in here
    # Add a "hello world" message
    html.P("Hello, World!"),
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
```

### Create the layout

Steps for this activity:

1. Define a variable that creates the components for the first row
2. Define a variable that creates the components for the second row
3. Add the two variables within the dbc.Container in the `app.layout`

You may need to refer to:

- [Dash layout documentation](https://dash.plotly.com/layout)
- [Dash bootstrap components layout documentation](https://www.dash-bootstrap-components.com/docs/components/layout/)
- [Bootstrap grid system documentation](https://getbootstrap.com/docs/5.3/layout/grid/)
- [Dash HTML components reference](https://dash.plotly.com/dash-html-components) for attributes for
  each HTML component

The suggested layout is:

<img alt="Paralympics app grid" src="../img/grid.png" style="width: 30%"/>

- Row 1 with 2-columns:
    - Column 1 spans 4-columns and contains selectors
    - Column 2 spans 8-columns and displays the charts
- Row 2 spans the full 12-columns and will contain the questions

A few points about using dash.html elements in this activity:

- A `Div` is an HTML "division" element and is primarily used as a container to create sections or
  divisions in a web page. This is useful as you can target the `Div` to apply styles, or locate
  sections on the page.
- `dash.html` components have keyword attributes. By default, the first attribute is a property
  called "children". This is special, and so long as you specify the children first, you do not have
  to include the `"children="` keyword.

    ```python
    # Children is a special attribute and if used as the first attribute does not need to be named
    html.H1(children='Hello Dash')
    # is the same as 
    html.H1('Hello Dash')
    
    # Children can also be nested components in a list '[]'. For example:
    html.Div(children=[
        html.H1('A first heading'),
        html.P('A bit more text after the heading')
    ])
    ```
- DBC components use the attribute `class_name=` to apply Bootstrap classes to a component, whereas
  Dash HTML and Core components use the attribute `className=`.

#### Create a variable for each row

DBC grid system uses three components: Container (`dbc.Container()`, Row (`dbc.Row`) and Column (
`dbc.Col`).

Place the Rows within a Container.

Place the Columns within a Row.

Place any content inside a Column.

Each row spans a conceptual 12 columns.

Row 1 has 2-columns:

- Column 1 spans 4-columns and contains selectors
- Column 2 spans 8-columns and displays the charts

You already have a Container for the page layout.

Defining each row as a variable allows you to more easily move the code to a separate function or
module; you might want to do this to keep the code easier to read.

The code for the first row is shown below.

Write the code for the second row yourself. Add the code for row two yourself.

Add the code to your `app.py`. If you left the app running while you added the new code, then it
should update itself in the browser when you save.

```python
import dash_bootstrap_components as dbc

# App code omitted

row_one = dbc.Row(
    [
        dbc.Col(html.Div("Selectors", id="selectors"), width=4),
        dbc.Col(html.Div("Charts", id="chart-display"), width=8),
    ]
)

app.layout = dbc.Container(children=[
    row_one,
])
```

### Add components to the layout

Next week you will create charts. The charts will include:

- A line chart with a dropdown to select variants ("sports", "events", "counties", "participants")
- A bar chart showing the change in male/female participants in summer and winter Paralympics. This
  has a checkbox selector for Winter and/or Summer.
- A map with points showing where each of the Paralympics has been held. This displays statistics
  about each event when hovered over the map points.

There will also be a selector that allows you to decide which of these charts to show.

Steps for this activity:

1. Define the dropdown selector to choose the chart
2. Define the dropdown selector for the line chart
3. Define the checkbox selector for the bar chart
4. Add the selectors to Row 1 Column 1 in the layout

You could use [Dash core components](https://dash.plotly.com/dash-core-components) for the
selectors, and apply Bootstrap styles using the `class_name=` attribute.

As we are using DBC, then instead use
the [DBC components](https://www.dash-bootstrap-components.com/docs/components/).

#### Dropdown

A dropdown is an [HTML
`<select>` element](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/select).
HTML select allows you to specify:

- if you allow one option or multiple options to be selected
- whether to have a default selected option
- what the value of the selected option is
- whether a select has to be made, or if it can be left blank

Dash's [dcc.Dropdown](https://dash.plotly.com/dash-core-components/dropdown) supports single or
multiple selection.

DBC's [dbc.Select](https://www.dash-bootstrap-components.com/docs/components/input/) does not
support multiple selection. Use the Dash version if you need this capability.

To syntax to create a `dbc.Select` is:

```text
select = dbc.Select(
    id="select",
    options=[
        {"label": "Option 1", "value": "1"},
        {"label": "Option 2", "value": "2"},
    ],
)
```

Using the example above as guidance, add code before the row variables code in your `app.py`:

1. Create a dbc.Select for the chart chooser. Add a suitable id. The options and values are:

    ```
    options=[
        {"label": "How have the number of sports, events, counties, participants changed?", "value": "line"},
        {"label": "How has the number of male and female participants changed?", "value": "bar"},
        {"label": "Where have the paralympics been hosted?", "value": "map"},
    ],
   ```
2. Create a dbc.Select for the line chart with a suitable id. The options and values are:
   "sports", "events", "counties", "participants".
3. Create a [dbc.Checklist](https://www.dash-bootstrap-components.com/docs/components/input/) for
   the bar chart selector with options for Winter and Summer. Use the 'choose a bunch' example on
   the linked page, you will need to scrolldown to the RadioItems and Checklist section of the page.
4. Add the select and checkbox elements as `children` of the `html.Div` in the first row, column
   one, of the layout.

Check the app still runs after saving your changes.

## Add a navbar

You don't really need a navbar for the design of this app, however, you will use it to add a
logo and title that spans the top of the page.

This activity uses the dbc.Navbar from
the [navbar](https://www.dash-bootstrap-components.com/docs/components/navbar/) documentation.

Steps:

1. Define the navbar as a variable using dbc.Navbar(). The navbar will contain a row with an
   html.Img for the logo and dbc.NavbarBrand for the name.
2. Add the navbar into the layout container before row 1

There are logos you can use in `docs/week2`. Save them in the `assets` directory of your app
package.

The html.Img syntax is like this: `html.Img(src=app.get_asset_url("paralympic_logo.png"))`

Create a variable for the navbar. The following is based on the DBC navbar documentation; you can
change it as you wish:

```python
navbar = dbc.Navbar(
    children=[
        dbc.Container(
            children=[
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row([
                        dbc.Col(html.Img(src=app.get_asset_url("mono-logo.webp"), height="40px")),
                        # dbc components use class_name=
                        dbc.Col(
                            dbc.NavbarBrand("Paralympics research app", class_name="navbar-brand")),
                    ],
                        align="center",
                    ),
                    href="#",
                    style={"textDecoration": "none"},
                ),
            ],
            fluid=True
        ),
    ],
    color="black",
    dark=True,
)
```

Add the `navbar` variable to the `app.layout`.

Check the app still runs.

The app looks basic right now, this will improve as you add charts next week.

You can experiment and change the colour theme, add a title, change the gutter, add images, etc. to
the layout.

### Further layout concepts

For this example the above Row and Col definitions are enough. For your own coursework you may
need to read up on other options.

1. Layout

   Explore the DBC documentation if you want to specify widths for different screen sizes; use
   offsets; specify order; adjust the gutters (space between columns); adjust horizontal or vertical
   alignment; or stack components.

2. Multi-page app

   This is documented in the [Dash documentation](https://dash.plotly.com/urls) using the concept of
   Dash Pages. You will also need to add navigation, refer to the
   DBC [nav](https://www.dash-bootstrap-components.com/docs/components/nav/)
   and [navbar](https://www.dash-bootstrap-components.com/docs/components/navbar/) documentation.

3. Themes

   The paralympics app is currently using the default theme specified when you created the app
   instance using `external_stylesheets=[dbc.themes.BOOTSTRAP]`. Explore alternative
   themes [here](https://www.dash-bootstrap-components.com/docs/themes/). You don't have to use DBC
   and Bootstrap, you can specify other open source CSS using the `external_stylesheets` attribute.

4. Selectors

   Dash and DBC support other selectors such as sliders, radio items, date pickers, forms, etc.
   Review their documentation if you want to use other types to select data in your coursework app.

### Additional sources of information

[Charming Data YouTube](https://www.youtube.com/@CharmingData/videos) channel has lots of Dash
videos.

[Plotly Dash course](https://www.youtube.com/playlist?list=PLYD54mj9I2JevdabetHsJ3RLCeMyBNKYV)
Plotly's own video tutorial series

[Dash open curriculum](https://github.com/open-resources/dash_curriculum/blob/main/tutorial/part1/chapter3.md)

[Dash Community forum](https://community.plotly.com/c/python/25?utm_source=dash_docs&utm_medium=documentation&utm_content=sidebar&_gl=1*bsajnh*_gcl_au*MTA5NTk2Njg1NC4xNzYzMTMxNzY0*_ga*MTQzOTY4MzE1NC4xNzYzMTMxNzY0*_ga_6G7EE0JNSC*czE3NjgzODI1NDUkbzEyJGcwJHQxNzY4MzgyNjEzJGo2MCRsMCRoMA..)
is a good source for help with specific questions not covered in the official documentation

[Sample Dash apps in GitHub](https://github.com/plotly/dash-sample-apps/tree/ebabf377d3be3d08752d53dfd04d1a59d7d164f1) –
some may use Plotly Enterprise, so check before using the code

[Live server with Dash sample apps](https://dash.gallery/Portal/) – some may use Plotly Enterprise,
so check before using

[Next activity](4-dash-structure.md)

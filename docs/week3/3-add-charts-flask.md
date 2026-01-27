# 3. Adding charts to the Flask app

## Setup

Ensure that you have plotly installed e.g. `pip list` shows what you have installed and
`pip install plotly` to install if you don't have it.

## Introduction

Last week you created the overall page layout and app structure and should have files similar to
this, with HTML template files for each of the pages.

![Flask app files](../img/flask-files.png)

If you completed the app structure activity, then you will now have the code to create the app
in the `__init__.py` like this:

```python
from flask import Flask

from paralympics.config import DevConfig


def create_app(config_class=DevConfig):
    """Create and configure the Flask application.

    Args:
        config_class (type): Configuration class used to configure the app. Defaults to DevConfig.
    Returns:
        flask.Flask: Configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    from paralympics.main import bp
    app.register_blueprint(bp)

    return app
```

With routes in another file (`main.py` in the screenshot) like this:

```python
from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/locations')
def locations():
    return render_template('locations.html')


@bp.route('/participants')
def participants():
    return render_template('participants.html')


@bp.route('/trends')
def trends():
    return render_template('trends.html')
```

In this activity you will add the charts you created in activity 2 to the templates and routes for
the locations (map), participants (bar chart) and trends (line chart) pages.

## Add the map chart

This is the simplest as there are no selectors, you will only add the chart to the template.

### 1. Modify the route

Modify the route to return the chart:

1. Create a variable and use the charts.scatter_map() functions
2. Convert the figure with its associated Plotly JavaScript using the plotly `to_html()` method.
   Their documentation explains how
   to [add it to add a chart to Jinja template](https://plotly.com/python/interactive-html-export/).

    ```python
    from paralympics.charts import scatter_map
    
    # Inside the route function, include:
    fig = scatter_map()
    fig_for_jinja = {"fig": fig.to_html(full_html=False, include_plotlyjs=True)}
    ```

   `include_plotlyjs=True` passes the Plotly JavaScript with the file, so adds about 3MB, this
   ensures the chart can load without an internet connection. Read the documentation for how to
   reference a CDN version of the JavaScript instead.

3. Pass the `map_for_jinja` to the template when you return render_template, e.g.
   `return render_template('locations.html', fig_html=fig_for_jinja)`

### Modify the template

You need to access the `fig` attribute from the `fig_html=map_for_jinja` you passed using
`render_template` to the template.

Add it as a Jinja variable inside the 'content' block:

`{% block content %} Add a Jinja variable here for the fig! {% endblock %}`

To protect the app from malicious HTML/JS being entered by a user to a web app, Jinja automatically
escapes any HTML. When automatic escaping is enabled, everything is escaped by default except for
values explicitly marked as safe. Those can be marked in the template by using the `| safe` filter.

The code will look like this:

```jinja
{% extends 'base.html' %}

{% block title %}Locations{% endblock %}

{% block content %}
    
    {{ fig_html.fig | safe }}
    
{% endblock %}
```

Make sure the data\mock_api app is still running.

Run the Flask app, navigate to the 'locations' page and view the chart.

## Repeat for the other two chart pages

Using the above approach, add similar code to the other two chart templates and routes.

For now, pass in a fixed value when you create the charts, e.g.

```python
from paralympics.charts import line_chart, bar_chart

# For the line chart route (trends)
line = line_chart("sports")

# For the bar chart route (participants)
bar = bar_chart("winter")
```

I did not add a grid layout to my `base.html` template in week 2. Instead, I edited my templates
for the trends and participants to include a 1-row, 2-column layout. The dropdown/checkbox go
in the first column, the chart in the second. For example:

```html
{% extends 'base.html' %}

{% block title %}Trends{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-3">
            <p>selector</p>
        </div>
        <div class="col-md-9">
            <p>chart</p>
            {{ fig_html.fig | safe }}
        </div>
    </div>
</div>
{% endblock %}
```

## Add the dropdown selector for the trends/line chart page

As JavaScript is not covered in the course, this solution 'mostly' avoids JavaScript by using the
FlaskWTF library.

[FlaskWTF](https://flask-wtf.readthedocs.io/en/1.2.x/form/) is a Flask extension
of [WTForms](https://wtforms.readthedocs.io/en/3.2.x/), a popular library for creating forms.

Install it, e.f. `pip install flask-wft`

The steps are:

1. Define the form as a FlaskForm class with a select field.
2. Update the template to add the form:

    - add the form with the select field
    - when a choice is made in the dropdown it submits the form as an HTTP POST request.
3. Update the route.

    - Create an instance of the form using the class defined in step 1
    - When the Flask route receives the POST request, find the selected value from the request.
    - Use the value to pass to the method that creates the chart.
    - Convert the created Plotly charts to HTML/JavaScript
    - Pass the form and the chart to the template to render the page

### 1. Create the form with a select

- Create a new python module, e.g. forms.py.
- Import FlaskForm from flask_wtf.
- Define a form that inherits the FlaskForm class.
- Add a select field with:
    - the options and their values for the dropdown
    - the choice is required (validator)
    - the Bootstrap class for a select
    - a line of JavaScript that enables the form to be submitted when the select choice is made,
      rather than requiring a "submit" button

The code is:

```python
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired


class TrendSelectForm(FlaskForm):
    selected_type = SelectField("Select the data to show in the chart",
                                choices=[('countries', 'Countries'), ('events', 'Events'),
                                         ('participants', 'Participants'), ('sports', 'Sports')],
                                # options and values for the dropdown
                                default="countries",
                                validators=[DataRequired(), ],  # validation rule
                                render_kw={"class": "form-select",  # Bootstrap class
                                           "aria-label": "Select the data to show in the chart",
                                           "onchange": "this.form.submit()"  # Javascript
                                           },
                                )
```

### 2. Add the form to the template

An [HTML form has attributes](https://www.w3schools.com/html/html_forms_attributes.asp) that
determine what happens when it is submitted.

For forms with a large amount of data, or sensitive data, use a 'POST' method.

For this example, either POST or GET works.

You also need to specify the URL to call when the form is submitted. You want to use the same
route which in the case of my code is `main.trends` as the blueprint name is main:

```python
bp = Blueprint('main', __name__)
```

Your URL may be different if you don't have a blueprint, or you may have called the route's function
something different to `trends`.

To get the URL for the route, use a Jinja variable `{{ }}` that contains the Flask `url_for()`
function.

The form fields are added as Jinja variables using the form select attribute name.

```html

<form method="post" action="{{ url_for('main.trends') }}">
    {{ form.selected_type }}
</form>
```

The full template will look something like this:

```html
{% extends 'base.html' %}

{% block title %}Trends{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-12 col-md-3">
            <form method="post" action="{{ url_for('main.trends') }}">
                {{ form.selected_type }}
            </form>
        </div>
        <div class="col-12 col-md-9">
            {{ fig_html.fig | safe }}
        </div>
    </div>
</div>
{% endblock %}
```

## 3. Update the route for the trends/line chart page

- Create an instance of the form
- If the form passes the validation rule, i.e. a choice was made in the select then get the selected
  value from the form
- Otherwise, use a default value, 'events'
- Pass the value to the `line_chart()` function
- Pass the form in the `render_template()` function

```python
@bp.route('/trends', methods=['GET', 'POST'])
def trends():
    # Create an instance of the form
    form = TrendSelectForm()

    # Check the form passes the validation rules on the form fields
    if form.validate_on_submit():
        # Get the value of the selected_type field from the form
        selected_type = form.selected_type.data
    else:
        # Default to countries
        selected_type = "countries"

    # Create the line chart Plotly figure    
    fig = line_chart(selected_type)

    # Convert the figure to HTML containing any necessary Plotly JavaScript
    fig_for_jinja = {"fig": fig.to_html(full_html=False, include_plotlyjs=True)}

    # Pass the form and the chart HTML/JS to the template to render the page
    return render_template('trends.html', fig_html=fig_for_jinja, form=form)
```

Run the app and check the page functions as expected.

## Add the checkbox selector for the participants/bar chart page

The steps are:

1. Define the form as a FlaskForm class with a checkbox field.
2. Update the route.
3. Update the template to add the form.

### 1. Create the form class with checkboxes

This time the form is more complex. Checkboxes are a single field, so to ensure that at least one
or both are selected requires custom validation and the use of JavaScript.

The suggestion in the code below is to use a WTForms SelectMultipleField and render it as a
checkbox list:

```python
class ParalympicsTypeForm(FlaskForm):
    paralympics_types = SelectMultipleField(
        "Select one or both types of Paralympics",
        choices=[("winter", "Winter Paralympics"), ("summer", "Summer Paralympics")],
        option_widget=CheckboxInput(),
        widget=ListWidget(prefix_label=False),
        validators=[Length(min=1, message="Select at least one topic.")],
        render_kw={"class": "form-check-input", },
    )
    submit = SubmitField("Generate selected charts")
```

### 2. Update the route

In this route, none, one or two charts may be created.

- Create an instance of the form using the class.
- When the Flask route receives the POST request, find the selected list of values from the request.
- Create a list variable to contain the HTML/js for the charts.
- For each of the values, create a bar chart, convert to plotly and append to a list of charts
- Pass the list of charts and the form to the page
- Instead of a default chart, display the page with only the form and no charts on GET or if the
  form validation fails.

The code would look like this:

```python
@bp.route('/participants', methods=['GET', 'POST'])
def participants():
    form = ParalympicsTypeForm()
    if form.validate_on_submit():
        paralympics_types = form.paralympics_types.data
        figs = []
        for p_type in paralympics_types:
            fig = bar_chart(p_type)
            fig_for_jinja = {"fig": fig.to_html(full_html=False, include_plotlyjs=True)}
            figs.append(fig_for_jinja)
            return render_template('participants.html', figs=figs)
    # If the page is a GET request, or there is a form error, then return the page without charts
    return render_template('participants.html')
```

### 3. Update the template

Modify the template to:

- display only the multi-checkbox selector
- render one or two charts from the list of chart HTML/js if present

To display the multi-checkbox selector, use Jinja expression `{% for %} {% endfor %}` to loop
through the checkboxes and add them to the form.

```html
<form method="post" action="{{ url_for('main.participants') }}">
    {{ form.hidden_tag() }}
    {{ form.paralympics_types.label(class="form-label") }}
    {% for subfield in form.paralympics_types %}
        <div class="form-check">
            {{ subfield(class="form-check-input") }}
            {{ subfield.label(class="form-check-label") }}
        </div>
    {% endfor %}
    {{ form.submit() }}
</form>
```

The logic to render the charts also uses Jinja syntax. If there are any figures, then loop through
the list and add each to the layout:

```jinja
{% if figs %}
    {% for f in figs %}
        {{ f.fig | safe }}
    {% endfor %}
{% endif %}
```

The full template will look something like this:

```html
{% extends 'base.html' %}
{% block title %}Participants{% endblock %}
{% block content %}
    <div class="container-fluid mt-4">
        <div class="row">
            <div class="col-md-3">
                <form method="post" action="{{ url_for('main.participants') }}">
                    {{ form.hidden_tag() }}
                    {{ form.paralympics_types.label(class="form-label") }}
                    {% for subfield in form.paralympics_types %}
                        <div class="form-check">
                            {{ subfield(class="form-check-input") }}
                            {{ subfield.label(class="form-check-label") }}
                        </div>
                    {% endfor %}
                    {{ form.submit() }}
                </form>
            </div>
            <div class="col-md-9">
                {% if figs %}
                    {% for f in figs %}
                        {{ f.fig | safe }}
                    {% endfor %}
                {% endif %}
            </div>
        </div>
    </div>
{% endblock %}
```

## Next week

In next week's activities you will also create a form for the question/answer feature.

The activity will also cover other aspects of forms:

- CSRF protection
- Jinja macro helpers
- Further validation
- Providing help and feedback on form errors to the user
- Populating form values from a REST API query
- Passing values to a REST API to save in a database

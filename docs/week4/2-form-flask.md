# 2. Adding a form to a Flask app

## Before you start

Make sure you have the latest versions of the following files from
the [tutorials repository](https://github.com/nicholsons/comp0034-tutorials-2025/tree/master/src/data):

- `data.py` the ParalympicsData class has moved out of mock_api.py to this module
- `mock_api.py` updated to include more routes
- `paralympics.db` this has questions and responses in the database

Make sure the API is running. Run in Python `src/data/mock_api.py`.

The API by default will be available at http://127.0.0.1:8000

## Overview

This activity gets multiple choice questions from the database via the REST API, captures a user's
response and checks if the answer is correct.

It uses a form to capture the response from the student.

To do this you will create:

- a form class
- a page template
- a Flask route

## Create a form class

You can create an HTML form in Flask, however a common method is to use
the [WTF](https://wtforms.readthedocs.io/en/3.2.x/) library with
the [FlaskWTF](https://flask-wtf.readthedocs.io/en/1.2.x/) extension.

To use you install FlaskWTF which by default also installs WTF e.g. `pip install -U Flask-WTF`

If you completed the week 3 activities, then you already have this installed and have used it.

Create a form class with a RadioField.

The RadioField's label will be the question text.

The RadioField's options will be the four potential responses that are stored in the database.

You will get the values for the question text and the responses in the route code.

```python
from flask_wtf import FlaskForm
from wtforms import RadioField
from wtforms.validators import DataRequired


class QuizForm(FlaskForm):
    """ A form with 1 question as a radio field """
    question = RadioField("",
                          choices=[],
                          coerce=int,
                          validators=[DataRequired()],
                          )
    submit = SubmitField("Submit response", render_kw={"class": "btn btn-primary"})
```

## Code to get the data from the REST API

Use the python 'requests' library to make HTTP requests and access the JSON from the response.

The code is like this:

```python
import requests

response = requests.get(
    f"http://127.0.0.1:8000/question")  # Capture the response from a request to an API URL
response.raise_for_status()  # In case of an error
json_data = response.json()  # Get the JSON from the HTTP response
```

I created some helper functions for getting the data. You don't have to do this.

```python
import requests

API_BASE_URL = "http://127.0.0.1:8000/question"


def _get_number_questions():
    """ Helper to get the number of questions available"""
    q_resp = requests.get(f"{API_BASE_URL}question", timeout=2)
    q_resp.raise_for_status()
    questions = q_resp.json()
    return len(questions)


def _get_question(qid):
    """ Helper to get the question"""
    q_resp = requests.get(f"{API_BASE_URL}/question/{qid}", timeout=2)
    q_resp.raise_for_status()
    q = q_resp.json()
    return q


def _get_responses(qid):
    """ Helper to get the questions and responses for a given question id"""
    r_resp = requests.get(f"{API_BASE_URL}/response/search?question_id={qid}", timeout=2)
    r_resp.raise_for_status()
    r = r_resp.json()
    return r
```

## Update the index route to pass the data to display the initial form

The route needs to support GET for the initial display of the page with the question, and POST to
handle the submitted form.

Create an instance of the form.

Get the values from the REST API for the question and the potential responses.

Pass the form and the values to the Jinja template.

```python
@bp.route("/", methods=["GET", "POST"])
def index():
    """ Page that displays a multiple choice question """

    # Create an instance of the form
    form = QuizForm()

    # Get the question and responses for the question (question with id 1 from the database)
    qid = 1
    question = _get_question(qid)
    responses = _get_responses(qid)

    # Populate form radio label and choices
    form.question.label.text = question["question_text"]
    form.question.choices = [(r["id"], r["response_text"]) for r in responses]

    return render_template("index.html", form=form, qid=qid)
```

## Update the index template to render the form

You can manually define each field in the form.

A common practice is to use Jinja macros to render the fields. These behave like functions that
you can call in the template and avoid you repeating boilerplate code. If you search you will find
examples you can copy and adapt
e.g., [Miguel Grinberg's file](https://blog.miguelgrinberg.com/post/dynamic-forms-with-flask).

The following does not use the macros.

The Jinja template receives for form object.

You can access the fields as follows:

- `form.question.label` the label has the question text.
    - `form.question` this has the radio, you need to access the subfields, if you iterate through
      question you get something like:

      ```html
      <input id="question-0" name="question" required type="radio" value="1">
      <input id="question-1" name="question" required type="radio" value="2">
      <input id="question-2" name="question" required type="radio" value="3">
      <input id="question-3" name="question" required type="radio" value="4">
      ```
- `form.submit` the submit button

Your template may look different to mine but this is how I implemented it:

```html
{# Form submit using post to the index route in the Flask app #}
<form action="{{ url_for('main.index') }}" method="post">

    {# Required for CSRF unless this has been explicitly disabled #}
    {{ form.csrf_token }}

    <fieldset class="row mb-3">

        {# The question text #}
        <legend class="col-form-label" id="questionNumber">{{ form.question.label }}</legend>

        <div class="col-sm-10">
            {# Loop through the question to get the options and their labels to display the text #}
            {% for subfield in form.question %}
            <div class="form-check">
                {{ subfield(class="form-check-input", type="radio") }}
                {{ subfield.label(class="form-check-label") }}
            </div>
            {% endfor %}
        </div>

    </fieldset>

    {# The submit button #}
    {{ form.submit() }}

</form>
```

Run the app now and the form should display.

## Update the route to handle the form submission logic, the "POST" route

You can have more than one route definition for a route.

Update the route to also allow it to be given an optional "question id", `qid`. The first time
the page is called it will start at question 1.

The solution below uses [Flask flash messaging](https://flask.palletsprojects.com/en/stable/patterns/flashing/). Flash messaging displays a message the next time a
URL is called. To enable Flask flash messages to be displayed on any page, update your base
template with the following. Add it in the body, e.g. at the top after the navbar.

```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <p class="alert alert-{{ category }}">{{ message }}</p>
        {% endfor %}
    {% endif %}
{% endwith %}
```

Read the comments in the code to understand the logic being applied. 

```python
@bp.route("/", methods=["GET", "POST"])
@bp.route("/<int:qid>", methods=["GET", "POST"])
def index(qid=1):
    """ Page that displays one question at a time

    If user visits '/', qid defaults to 1. If user visits '/3', qid=3.

    Quiz flow:
    - Correct -> go to next question
    - Incorrect -> stay on current question
    - After last question answered correctly -> completion message, back to start
    """

    # Create an instance of the form
    form = QuizForm()

    # Logic to handle which question the user is on
    number_questions = _get_number_questions()

    if qid < 1 or qid > number_questions:
        flash("Oops, that question does not exist!")
        return redirect(url_for("main.index"))

    # Get the question and responses for the current question
    question = _get_question(qid)
    responses = _get_responses(qid)

    # Populate form (choices must be set before validate_on_submit)
    form.question.label.text = question["question_text"]
    form.question.choices = [(r["id"], r["response_text"]) for r in responses]

    if form.validate_on_submit():
        # Logic to check if the response is correct
        selected_id = form.question.data
        selected_resp = next((r for r in responses if r.get("id") == selected_id), None)
        is_correct = bool(selected_resp and selected_resp.get("is_correct"))
        if is_correct:
            # If last question, complete; else advance to the next question
            if qid == number_questions:
                flash("Well done! You completed the questions!", "success")
                return redirect(url_for("main.index", qid=1))
            else:
                return redirect(url_for("main.index", qid=qid + 1))
        else:
            # Stay on the same question
            flash("Try again!", "warning")
            return redirect(url_for("main.index", qid=qid))

    return render_template("index.html", form=form, qid=qid)
```

Add something similar to your own code.

[Next activity](3-form-with-data-flask.md)
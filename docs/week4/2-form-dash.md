# 2. Adding a form to a Dash app

## Before you start

Make sure you have the latest versions of the following files from the [tutorials repository](https://github.com/nicholsons/comp0034-tutorials-2025/tree/master/src/data):

- `data.py` the ParalympicsData class has moved out of mock_api.py to this module
- `mock_api.py` updated to include more routes
- `paralympics.db` this has questions and responses in the database

The API by default will be available at http://127.0.0.1:8000

## Overview

This activity gets multiple choice questions from the database via the REST API, captures a user's
response and checks if the answer is correct.

Rather than use an HTML form, in Dash you attach callbacks to input components. You can still use
Bootstrap styling by using the inputs from dash-bootstrap-components e.g., `dbc.Input`.

You can define the inputs and then group as a [
`dbc.Form()`](https://www.dash-bootstrap-components.com/docs/components/form/) to achieve the
overall form layout, though
this is not essential.

You do not want the form to submit until all the inputs are selected. This is achieved by using
[State](https://dash.plotly.com/basic-callbacks#dash-app-with-state). State allows you to read the
value of an input component, but only when the user is finished entering all of their information in
the form rather than immediately after it changes.

## Add the question/answer functionality

One question at a time will be presented to the user with a `Submit` button.

The first question will be shown when the page is loaded.

If answer correctly, they move to the next question, if not, they keep repeating until it is
correct. Repeat for all questions then end.

There will be two callbacks.

- one will add a question to the layout
- one will handle the logic to check if the question is correct and manage progression

#### Add helper functions

You need to repeat code to get data from the REST API and to create the question and responses.

Add these helper functions, either in your `app.py` or create a new module and import them.

```python
import requests  # add this import to the top of the code not in the middle!


def create_question(q: dict):
    """
    Constructs a list of Dash components for presenting a question and its possible responses,
    including a radio button group for response selection and a submit button.

    Args:
    q (dict): A dictionary containing details of the question such as its ID and text. Must have the keys:
              - "id" (str | int): A unique identifier for the question.
              - "question_text" (str): The question text to display.
    Returns:
         A list of Dash components, including:
             - A label for displaying the question text.
             - A hidden paragraph element containing the question ID.
             - A radio button group for selecting a response.
             - A line break element.
             - A submit button for submitting the response.
    """
    responses = get_responses(q["id"])
    options = [{"label": r.get("response_text", ""), "value": r.get("id")} for r in responses]
    radio = dbc.RadioItems(id="question-radio", options=options, value=None)
    submit_btn = dbc.Button("Submit answer", id="submit-btn", n_clicks=0, color="primary")
    return [
        html.Label(q.get("question_text", ""), id="question-label"),
        html.P(q.get("id", ""), id="question-id", hidden=True),
        radio,
        html.Br(),
        submit_btn,
        html.Br()
    ]


def get_number_questions():
    """ Helper to get the number of questions available"""
    q_resp = requests.get(f"http://127.0.0.1:8000/question", timeout=2)
    q_resp.raise_for_status()
    questions = q_resp.json()
    return len(questions)


def get_question(qid):
    """ Helper to get the question"""
    q_resp = requests.get(f"http://127.0.0.1:8000/question/{qid}", timeout=2)
    q_resp.raise_for_status()
    q = q_resp.json()
    return q


def get_responses(qid):
    """ Helper to get the questions and responses for a given question id"""
    r_resp = requests.get(f"http://127.0.0.1:8000/response/search?question_id={qid}", timeout=2)
    r_resp.raise_for_status()
    r = r_resp.json()
    return r
```

#### Update the layout for the question area

Make sure that your question area has:

- a Div where you can add the question/responses to be displayed
- a Div for feedback messages

This solution also uses [dcc.Store](https://dash.plotly.com/dash-core-components/store) to save the
number of the question that the person is on. This
will be used by the callbacks to decide which question to display. This is initially set to
`data=1` to display the first question.

To add the first question to the layout, use the helper functions to get the question and its
responses from the REST API and then create the dbc components for the RadioItems.

My code looks like this:

```python
row_two = dbc.Row(
    [
        dbc.Col(children=[
            html.Hr(),
            html.H2("Questions"),
            # Store the question num. Start with 1.
            # storage_type="session" means the index persists per tab;
            # set to "memory" to reset on reload, or "local" to persist across tabs.
            dcc.Store(id="q_index", data=1, storage_type="session"),
            html.Div(id="question", children=create_question(get_question(1))),  # First question
            html.Div(id="result"),  # For messages/feedback
        ])
    ]
)
```

### Create the callback that creates a question

The first question is already in the second row.

For subsequent questions, you need a callback to replace this.

The callback will have:

- `Output`: the children of the question `Div` e.g.`html.Div(id="question")`
- `Input`: the question id stored in `dcc.Store(id="q_index", data=1, storage_type="session")`

The function should:

- Take the question index of the current question
- Get the total number of questions
- Get the question index, so long as this is less than the total number of questions available then
  display the question

My solution is:

```python
@app.callback(
    Output("question", "children"),  # rendered question block
    Input("q_index", "data"),  # current index
    prevent_initial_call=True,  # don't run on load
)
def render_question(index):
    """ Takes the question id and renders the question component in the layout

    Args:
        index (int): the question id

    Returns:
        question (html.Div): the question component
        """
    if not index:
        raise PreventUpdate

    try:
        num_q = get_number_questions()
    except Exception as e:
        return [html.Div(f"Unable to load questions. {e}", className="alert alert-danger")]

    # If past the last question, clear the block
    if index > num_q:
        return []

    try:
        q = get_question(index)
    except Exception as e:
        return [html.Div(f"Unable to load question. {e}", className="alert alert-danger")]

    return create_question(q)
```

### Create the callback that handles the progression logic when an answer is submitted

This callback has:

1. Two `Output`s:

    - the `dcc.Store` to update the question number to the next one if their answer is successful
    - the `Div(id="result")` to append a message with any feedback

2. An `Input`:

    - the `Submit` button

3. Two `State`s:
    - the question id from the `Store`
    - the selected radio item to allow the user to make changes until the button is clicked

The logic when the button is clicked is:

- check that a response is selected, if not they need to select one
- if a response is selected, check if it is correct
- if the response is correct, go to the next question unless it is the last question in which case
  they have finished
- if the response is incorrect they need to try again

The code might look like this:

```python
@app.callback(
    Output("q_index", "data"),  # updated index (1-based)
    Output("result", "children"),  # feedback message
    Input("submit-btn", "n_clicks"),  # submit click
    State("q_index", "data"),  # current index
    State("question-radio", "value")  # selected response id
)
def handle_submit(n_clicks, index, selected_response_id):
    """ Handles the question progress and any feedback message

    Args:
        n_clicks (int): if the button was clicked or not
        index (int): the index of the question from the dcc.Store
        selected_response_id (str): the response id from the selected radio

    Returns:
        q_index (int): the selected question id
        result (str): a feedback message
        """
    if not n_clicks:
        raise PreventUpdate

    # Require a selection
    if selected_response_id in (None, "", []):
        return index, [html.Div("Please select an answer.", className="alert alert-info")]

    # Evaluate answer
    try:
        responses = get_responses(index)
    except Exception as e:
        return index, [html.Div(f"Unable to load responses. {e}", className="alert alert-info")]

    selected = next(
        (r for r in responses if str(r.get("id")) == str(selected_response_id)),
        None,
    )

    # Get the number of questions
    try:
        num_q = get_number_questions()
    except Exception as e:
        return index, [html.Div(f"Unable to load questions. {e}", className="alert alert-danger")]

    if selected and selected.get("is_correct"):
        # Finish if last question
        if index >= num_q:
            return num_q, [
                html.Div("Questions complete, well done!", className="alert alert-success")]
        # Otherwise advance
        next_index = index + 1
        return next_index, ""
    else:
        # Incorrect: stay on the same index
        stay_index = index
        return stay_index, [html.Div("Please try again!", className="alert alert-info")]
```

Run the app and check it works.

## Ideas to extend the solution

The solution above is rudimentary. You could try to enhance it, e.g.:

- allow the questions to be restarted
- capture their responses and calculate a score
- capture their result and save it to the database (you may need a new table in the database)

[Next activity](3-form-with-data-dash.md)


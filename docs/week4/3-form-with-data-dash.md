# 3. Using a form to submit data to the REST API (Dash)

This activity will add a new admin feature to the app to allow a teacher to add new
questions and responses.

This is added as a [tab](https://dash.plotly.com/dash-core-components/tabs) for ease, though you
could transform the app from a single page to a multipage app and add this as a separate page.

## Restructure the layout to create two tabs

Following the [dcc.Tabs](https://dash.plotly.com/dash-core-components/tabs)
and [dbc.Tabs](https://www.dash-bootstrap-components.com/docs/components/tabs/)documentation,
restructure the app to two tabs e.g.:

```python
app.layout = dbc.Container(children=[
    navbar,
    dcc.Tabs([
        dcc.Tab(label='Paralympics dashboard and questions', children=[
            lead,
            row_one,
            row_two
        ]),
        dcc.Tab(label='Teacher admin', children=[
            # Question form will go here
            html.Div(id="form-message")
        ])
    ])
], fluid=True)
```

## Define the 'form' to add a new question

Dash does not require you to add a form to contain the inputs, though for Bootstrap styling purposes
you may want to group them within a `dbc.Form()`

Add code within your layout that is similar to the following.

To reduce the length, I added a function to generate the four response options.

```python
def add_responses_to_new_question(number):
    """ Helper function to add responses to a new question

    Args:
        number (int): The number of response options to generate

    Returns:
        rows (List[]): A list of dbc components to add to UI
        """
    rows = []
    for n in range(number):
        rows.append(
            dbc.Row([
                dbc.Col(dbc.Input(id=f"response_text_{n}", required=True)),
                dbc.Col(html.Div([
                    dbc.Checkbox(id=f"is-correct_{n}", label="Correct response?", value=False),
                    html.Br()
                ])
                ),
            ])
        )
    return rows
```

My form became:

```python
html.Div(children=[
    html.H2("Create a multiple choice question"),
    dbc.Form([dbc.Label("Question text"),
              dbc.Textarea(
                  id="question_text",
                  placeholder="Enter the question text",
                  required=True
              ),
              html.Hr(),
              html.H5("Add the four potential responses, indicate which is correct"),
              html.Div(children=add_responses_to_new_question(4)),
              dbc.Button("Add question", id="new-question-submit-button", color="primary"),
              ])
])
```

### Processing the submitted form

1. Validate the values:
   - One and only one response must be correct
   - Response text and question text must not be empty. This is applied at the HTML level using `required=True`. It could also be added in the callback.
2. Save the question using POST request to http://127.0.0.1:8000/question and pass the JSON as the payload
    ```python
    response = requests.post("http://127.0.0.1:8000/question", payload=question_json, timeout=2)
    response.raise_for_status()
    question_id = response.json()["id"]
    ```
3. If the question POST is successful, the response returns JSON that include the id of the newly created question
4. Use the question id for the `question_id` values for each response


The callback uses the Submit button as the Input. 

The Output will be the `html.Div(id="form-message")`

To ensure the form inputs can be captured only when the Submit is pressed, use State.

As the form has 9 different inputs, you can avoid listing them all like this. I also show how I 
access the values from the states and use that to create JSON:

```python
@app.callback(
    Output("form-message", "children"),
    Input("new-question-submit-button", "n_clicks"),
    State("question_text", "value"),
    # states for the 4 response text inputs
    [State(f"response_text_{i}", "value") for i in range(4)],
    # states for the 4 checkboxes
    [State(f"is-correct_{i}", "value") for i in range(4)],
)
def process_question_form(n_clicks, question_text, *states):
    if not n_clicks:
            raise PreventUpdate
    
        # unpack variable-length *states
        response_texts = states[:4]  # first 4 states
        correctness_flags = states[4:]  # last 4 states
    
        # Generate JSON for the question and responses
        question = {"question_text": question_text}
        responses = [
            {"response_text": response_texts[i], "is_correct": correctness_flags[i]}
            for i in range(4)
        ]
```

### Validation

Validate the values:
- One and only one response must be correct
- Response text and question text must not be empty. This is applied at the HTML level using `required=True`.

There is no single approach.

You could leave the 'must not be empty' to the HTML validator.

For completeness, I've included both validation rules in my solution:

```python
    if not n_clicks:
        raise PreventUpdate

    # unpack variable-length *states
    response_texts = states[:4]  # first 4 states
    correctness_flags = states[4:]  # last 4 states

    # Generate JSON for the question and responses
    question = {"question_text": question_text}
    responses = [
        {"response_text": response_texts[i], "is_correct": correctness_flags[i]}
        for i in range(4)
    ]

    # Validation
    errors = []

    if not question["question_text"] or not question["question_text"].strip():
        errors.append(html.P("Question text is required."))

    for idx, r in enumerate(responses, start=1):
        if not r["response_text"] or not r["response_text"].strip():
            errors.append(html.P(f"Option {idx} must have text."))
    correct_count = sum(1 for r in responses if r["is_correct"])

    if correct_count == 0:
        errors.append(html.P("Please select exactly one correct response (none selected)."))
    elif correct_count > 1:
        errors.append(html.P("Please select exactly one correct response (multiple selected)."))

    # Return the validation errors
    if errors:
        return errors
```

### Save the question and responses

To save the question, use a POST request to the REST API. You pass the JSON for the question in the
request payload.

POST the new question. If successful, the response will contain the id of the row that was just
created in the database.

Use that it to add the `question_id=new_id` to each of the response options.

This is my solution:

```python
    # Use the API to save the question to the database
    payload = question
    try:
        response = requests.post(f"{API_BASE_URL}/question", json=payload)
        response.raise_for_status()

        # Get the id of the newly saved question from the response
        question_id = response.json()["id"]
        
        # Use the API to save the question's response options to the database
        for idx, r in enumerate(responses, start=1):
            r["question_id"] = question_id
            resp = requests.post(f"{API_BASE_URL}/response", json=r)
            resp.raise_for_status()
        return "Question saved successfully."

    except Exception as exc:
        return html.P(f"Error saving question: {exc}")
```

Use the form to add a new question.

If the question saved successfully then when you start the question tab again it should include
the new question.

[Tutor code](4-end.md)
# 3. Using a form to submit data to the REST API (Streamlit)

This activity will add a new admin section to the app to allow a teacher to add new
questions and responses.

It adds a new page for the teacher so takes the app from a single to multipage app.

## Move from a single to multipage app

There are two approaches to creating
a [multipage app](https://docs.streamlit.io/develop/concepts/multipage-apps/overview) in Streamlit:

- a simple method using a /pages directory that automatically creates a sidebar navigation uses the
  Python file page names to generate the page names
- a more customisable method using `st.Page` and `st.navigation`

This activity uses the first method.

Create a new folder named `pages`.

Add a new file in the directory: `/pages/teacher_admin.py`

The app.py that has the entrypoint for the streamlit app acts as the home page. Any pages in the
`/pages` folder are treated as an additional page in the app.

Names in the navigation are created based on the file names so you may want to rename app.py to
paralympics_dashboard.py.

For more control over navigation and names refer to the more customisable approach in the Streamlit
documentation. Other options and concepts are covered in the documentation that you may want to
refer to e.g. to understand how the `st.session_state` is shared across pages.

The [documentation](https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app) gives
the steps to convert a single page app to a multipage app.

## Create a form that allows a teacher to add a new question with four possible responses

In the new `teacher_admin.py` set the page title using `st.page_config()`

Create a form using `st.form("form_name")`.

With the form,
add [widgets for the inputs](https://docs.streamlit.io/develop/api-reference/widgets):

- [`st.text_input()`](https://docs.streamlit.io/develop/api-reference/widgets/st.text_input) with a
  `key="question_text`. `question_text` is the name of
  the database table column you want to save the question to.
- four `st.text_input()` for the potential responses, each with an [
  `st.checkbox()`](https://docs.streamlit.io/develop/api-reference/widgets/st.checkbox).
  Each needs to have a unique key.
- [
  `form_submit_button()`](https://docs.streamlit.io/develop/api-reference/execution-flow/st.form_submit_button)

Try to write the code yourself rather than just copying my solution.

## Add the form processing logic

On submit:

1. Apply validation rules
    - all fields must be complete.
    - one and only one checkbox must be selected as the correct answer.

2. Save the question_text as a new question in JSON format using the HTTP POST route. If successful
   this returns JSON that give you the 'id' of the newly created question row in the database.
3. Save the 4 responses using JSON for each where `question_id=` is the id returned in the above
   step, `response_text` is the response
   text from the form, and `is_correct` is the value for that response option in the form.

The code can be added into the execution flow of the script, or you can write a function and call
that function from the submit button. I used the latter e.g.
`st.form_submit_button("Save Question", on_click=proc`. I then created a function with
the logic in the following subsections. You can use either approach.

### Validation

If using the function approach, you will need to get the form values from the st.session_state using
the keys, e.g.

```python
def process_form() -> None:
    # Get the form values from the session state
    question_text = st.session_state.question_text
    response_text_1 = st.session_state.response_text_1
    response_text_2 = st.session_state.response_text_2
    response_text_3 = st.session_state.response_text_3
    response_text_4 = st.session_state.response_text_4
    is_correct_1 = st.session_state.is_correct_1
    is_correct_2 = st.session_state.is_correct_2
    is_correct_3 = st.session_state.is_correct_3
    is_correct_4 = st.session_state.is_correct_4
```

If you are adding the validation within the `with form` part of the script then you don't need to
access `session_state`.

Streamlit does not allow you to apply HTML level validation so you cannot simply apply the
'required' attribute to the text input. Instead, validate after the user clicks the button e.g.

```python
import streamlit as st

name = st.text_input("Name")

if st.button("Submit"):
    if not name.strip():
        st.error("Name is required.")
    else:
        st.success(f"Submitted: {name}")
```

You can iterate all the fields and capture the errors to a list e.g. `errors = []` and
`errors.append()` and then return all the errors using a for loop such as:

```python
if errors:
    for e in errors:
        st.error(e)
```

### Save the question and responses

To save the question, use a POST request to the REST API. You pass the JSON for the question in the
request payload.

POST the new question. If successful, the response will contain the id of the row that was just
created in the database.

Use that it to add the `question_id=new_id` to each of the response options.

This is my solution:

```python
  # Send to the API using the JSON data
payload = question
try:
    response = requests.post(f"{API_BASE}/question", json=payload)
    response.raise_for_status()
    st.success("Question saved successfully.")

    # Get the id of the newly saved question from the response
    question_id = response.json()["id"]

    for idx, r in enumerate(responses, start=1):
        r["question_id"] = question_id
        resp = requests.post(f"{API_BASE}/response", json=r)
        resp.raise_for_status()

except Exception as exc:
    st.error(f"Error saving question: {exc}")
```

Note that I had already created the JSON for the question and responses from the session_state as
I'm using the function approach. Your code may be different so you can't simply copy and paste my
code into yours.

```python
question = {"question_text": st.session_state.question_text}
responses = [
    {"response_text": st.session_state.response_text_1,
     "is_correct": st.session_state.is_correct_1},
    {"response_text": st.session_state.response_text_2,
     "is_correct": st.session_state.is_correct_2},
    {"response_text": st.session_state.response_text_3,
     "is_correct": st.session_state.is_correct_3},
    {"response_text": st.session_state.response_text_4,
     "is_correct": st.session_state.is_correct_4},
]
```

Use the form to add a new question with options.

If the question saved successfully then when you start the question page again it should include
the new question.

However, if you cached the value that counted the number of questions in the database then you
need to also update that. You can clear a function's cache with `function_name.clear()` or clear the
entire cache with `st.cache_data.clear()`.

[Tutor code](4-end.md)
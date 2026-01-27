# 3. Streamlit layout

## Create a new project in your IDE

1. Create a new Python project in your IDE (VS Code, Pycharm).
2. Add .gitnore, README.md and pyproject.toml (covered in COMP0035)
3. Create and activate a Python virtual environment.
4. Install `pip install streamlit`
5. Create an `src` directory
6. Inside the `src` directory, create a Python package for the app code e.g. `paralympics`
7. Inside the `paralympics` package create a Python file for the app e.g. `app.py`
8. Inside the `paralympics` package create a hidden folder by naming it `.streamlit`, the exact
   naming is important so please create the name as shown.
9. Inside the `.streamlit` folder create a file called `config.toml`, again make sure you name it as
   exactly as shown
10. Install the code itself as an editable package (relies on pyproject.toml) `pip install -e .`

You will have a project folder that looks like this:

```text
project_folder_name/
 ├── .venv/
 ├── src/
     └── paralympics
        ├── __init__.py
        ├── app.py          # Main streamlit app script
        └── .streamlit/     
            └── config.toml # Streamlit config e.g. to alter colours and styles
├── .gitignore
├── pyproject.toml
└── README.md
```

## Define the layout

In a streamlit app the layout is defined
using streamlit commands. The options support many of the same options available in Bootstrap but
use streamlit commands which have their own styling.

Grid layouts typically use 12-column grids. Streamlit supports the use of columns. These are defined
using a ratio of column size, rather than numbers of columns spanned.

Containers can be used to hold multiple elements. Popovers, tabs, sidebars,
and more are supported by Streamlit. There are also third-party options for layout. These are all
listed in the [layout documentation](https://docs.streamlit.io/develop/api-reference/layout).

For example, the proposed layout is:

- Row 1 with 2-columns:
    - Column 1 spans 1/3 of the page and will contain the chart selectors
    - Column 2 spans 2/3 of the page and displays the charts
- Row 2 spans the full width and will contain the questions/answers

This can be achieved in streamlit
using [columns (st.columns)](https://docs.streamlit.io/develop/api-reference/layout/st.columns).
Streamlit recommends the `with` notation to add elements to any container (includes columns):

```python
import streamlit as st

st.set_page_config(page_title="Paralympics", layout="wide")

# Row 1: two columns
# use [1,1] for equal widths or e.g. [1,3] for 1:3
left_col, right_col = st.columns([1, 3])

with left_col:
    st.subheader("Selectors")

with right_col:
    st.subheader("Charts")

# Row 2: full-width (spans both columns)
st.divider()  # Added to show the separation visually, not required
full_width = st.container()

with full_width:
    st.subheader("Questions")
    st.write("Answer the questions using the charts to help you.")
```

Alterntively you could use the `st.sidebar` for the left column.

Add the code above to `app.py`

Run the app from the terminal in your IDE using `streamlit run src/paralympics/app.py`

## Adding elements to the layout

The first column will contain:

1. Dropdown to select the chart to view
2. Dropdown for the line chart to select which variable to display: "sports", "events",
   "countries", "participants"
3. A checkbox selector for the bar chart showing the change in male/female participants in summer
   and winter Paralympics: options for Winter and/or Summer.

The second column will display the selected chart:

1. A line chart with trends indicating the number of sports, events, counties, or participants.
2. A bar chart showing the change in male/female participants in summer and winter Paralympics.
3. A map with points showing where each of the Paralympics has been held. This displays statistics
   about each event when the map points are selected.

Charts will be created and added next week.

The second row will contain the homework questions with boxes for the responses.

You can use [streamlit commands](https://docs.streamlit.io/develop/api-reference) or any of the
available [third-party components](https://streamlit.io/components).

### Add elements to the Paralympics layout

Add the following to the layout.

For the left column you will need two [
`st.selectbox`](https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox) and two [
`st.pills`](https://docs.streamlit.io/develop/api-reference/widgets/st.pills).

I suggest pills rather than checkbox as we want to allow users to select one or both, whereas the
checkbox would need to be two separate elements in streamlit.

The syntax for `st.selectbox` for the first dropdown:

```python
select_chart = st.selectbox("Choose a chart:",
                            ("Trends in number of sports, events, counties, participants",
                             "Participants by gender",
                             "Paralympics locations"),
                            index=None,
                            placeholder="Select chart to view..."
                            )
```

- Add a second select box for choosing "sports", "events", "countries", "participants".
- Add `st.pills` for Winter and Summer (see example 1 in
  the [documentation](https://docs.streamlit.io/develop/api-reference/widgets/st.pills))

Remove the placeholder text `st.subheader("Selectors")`.

Leave the chart column empty. This will be covered next week.

Add an [`st.form`](https://docs.streamlit.io/develop/concepts/architecture/forms) for the quiz
questions. A form is used for this most elements in streamlit cause the script to be rerun when a
user makes an input. For the questions, we want the students to keep the questions and answers
open as they view the charts and only submit all their responses when they are ready to. A form in
streamlit allows for this.

The form should include four questions with four text input boxes, a text input for their name, and
a submit button.

Here is an example with one text input and a submit button:

```python
with question_container:
    st.write("Answer the questions using the charts to help you.")
    with st.form("questions"):
        question_one = st.text_input("Question one?", "Enter your answer here")
        st.form_submit_button("Submit your answers")
```

## Conditionally show/hide the chart selectors

Currently, both `selectbox`es and the `pills` are shown. You only want the second `selectbox` and
`pills` to
be shown if the relevant choice is made in the first `selectbox`.

The logic is:

- Initially display only the first `selectbox`, others should be hidden
- If "Trends in number of sports, events, counties, participants" is selected, show the first and
  second `selectbox`
- If "Participants by gender" is selected, show the first `selectbox` and the pills only
- If "Paralympics locations" is selected, show only the first `selectbox` only

You can use Python conditional logic to achieve this. The first is done for you, add the code for
the second option yourself. No code is needed for the third as there is nothing extra to display:

```python
with left_col:
    select_chart = st.selectbox("Choose a chart:",
                                ("Trends in number of sports, events, counties, participants",
                                 "Participants by gender",
                                 "Paralympics locations"),
                                index=None,
                                placeholder="Select chart to view...")

    # Conditional rendering based on the option chosen in select_chart
    if select_chart == "Trends in number of sports, events, counties, participants":
        select_trend_type = st.selectbox("Choose the feature to display:",
                                         ["Sports", "Events", "Countries", "Participants"])
```

## Styling

The app is not using Bootstrap or other third-party CSS for styling. There are some changes that
you can make to fonts and colours.

Note that you can use third-party style sheets or styles. For example, add CSS in the app.py script
using `st.markdown`. I would not recommend doing so for the coursework as it is more complex to
maintain and doesn't contribute to the marks.

```python

import streamlit as st

# Inject custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
        color: #333333;
    }
    .stSelectbox label {
        color: #FF4B4B;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)
```

Themes as defined as a configuration option in a `config.toml` file. See
the [theme documentation](https://docs.streamlit.io/develop/concepts/configuration/theming).

Explore theme options by adding them to the config.toml file e.g.:

```toml
base="dark"
primaryColor="darkSeaGreen"
textColor="slateBlue"
baseRadius="full"
```

You may need to stop and restart the app to see the theme changes.

## References and links

Use the references and example apps to explore other features that can be added to the layout.

Multipage apps and navigation are supported.

- [Streamlit API reference](https://docs.streamlit.io/develop/api-reference/layout)
- [Streamlit concepts - layout](https://docs.streamlit.io/get-started/fundamentals/main-concepts#layout)
- [Streamlit multipage apps](https://docs.streamlit.io/develop/tutorials/multipage)
- [Streamlit app gallery](https://streamlit.io/gallery)
- [Example streamlit app](https://github.com/dataprofessor/population-dashboard/blob/master/streamlit_app.py)

[Next activity](4-streamlit-structure.md)
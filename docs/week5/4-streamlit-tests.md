# 4. STREAMLIT: Streamlit testing API

Streamlit provides its own test API
and [tutorial](https://docs.streamlit.io/develop/concepts/app-testing). You will need to use refer
to their tutorial.

Streamlit provides a test class, AppTest. This runs the app in Python, not in a browser, so you
will not be able to test HTML, only the Streamlit Python components.

For Streamlit apps, you may need a compbination of Streamlit and Playwright tests to test the
interface components.

## Overview of test commands

Import the AppTest class.

Create and run a test app using `at = AppTest.from_file("app.py").run()`

```python
from streamlit.testing.v1 import AppTest

at = AppTest.from_file("app.py").run()
```

To locate elements on the page, Streamlit supports:

- By index, e.g. get all the buttons on the page, they are ordered according to where they appear on
  the page. Refer to using their position (starts at 0)
- By key, this uniquely identifies an element
- By container, e.g. `at.sidebar.checkbox` returns a sequence of all checkboxes in the sidebar

You then access attributes of the elements. All elements have the `.value` property which is the
content. Other attributes depend on the type of element, e.g. a selectbox would have `.options`

You can simulate steps that require state using `at.session_state["some_name"] = "some_value"`

## Write a test that checks the page loaded

Create a new test module in the `tests` directory.

Add a test that checks for a `st.title` or `st.header` on your page.

- Create and run the test app
- Find the first header or title
- Assert that the value is equal to the text of your header or title

You could also assert that no error occured to check the app runs OK: `assert not at.exception`

Try to write your own. Mine is below.

```python
def test_questions_header():
    """
    GIVEN a test app
    WHEN the page is requested
    THEN there should be a header with the text "Questions"
    """
    # Load the Streamlit app from file and run it
    app_file = Path(__file__).parent.parent.joinpath("src", "paralympics",
                                                     "paralympics_dashboard.py")
    at = AppTest.from_file(app_file).run()
    # App ran without error
    assert not at.exception
    # Access the header value and assert it is "Questions"
    assert at.header[0].value == "Questions"
    # Alternatively, assert that at least one header has the work question, case in-sensitive
    assert any("question" in h.value.lower() for h in at.header), "No header contains 'question'"
```

To run a single test: `pytest tests/test_paralympics_st.py::test_questions_header`

## Interact with elements

Although these tests are not browser tests, you can still set values for elements and use
sequences of actions. Refer to
the [cheat sheet](https://docs.streamlit.io/develop/concepts/app-testing/cheat-sheet) for examples.

Note that Streamlit AppTest does not currently support chart elements so you cannot assert for
the presence of a chart, only the selectors.

Complete the second selector for the test below then run the test:

```python
from streamlit.testing.v1 import AppTest

APP_FILE = Path(__file__).parent.parent.joinpath("src", "paralympics", "paralympics_dashboard.py")


def test_line_chart_selectors():
    """
    GIVEN a test app
    WHEN the line chart is chosen
    AND the sports data is chosen
    THEN the chosen options should be displayed
    """
    # running test app
    at = AppTest.from_file(APP_FILE).run()

    # the line chart is chosen from the selector
    at.selectbox[0].set_value("Trends").run()
    assert at.selectbox[0].value == "Trends"

    # the sports data is chosen from the selector
    at.selectbox[1].set_value("Sports").run()
    assert at.selectbox[1].value == "Sports"
```

Note on testing multipage apps: If you test a multipage app, be aware that even if you stitch to the
page using `switch_page()` or load the page directly to AppTest, the script still runs all pages so 
your element indexing may not be as you expect.






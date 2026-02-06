# 3. Writing Playwright tests

The approach is the same for all three app platforms, though you will need to check the ids of
elements on your app page and adapt the code below to suit your app.

Note that for Streamlit apps, locating elements can be more complex as the elements do not always 
have the properties that you might expect. Streamlit have Playwright tests for their own code which 
may be useful to look at: https://github.com/streamlit/streamlit/tree/develop/e2e_playwright

## Create a test module

Create a directory named `tests` in the root of the project.

Within the `tests` directory, create a new module that starts with `test_` e.g.,
`test_paralympics.py`

Remember that [pytest](https://docs.pytest.org/en/stable/explanation/goodpractices.html) recognises
common patterns for file, folder and test case names.

## Test that the first page is loaded

Decide what you can assert to verify the home page is loaded e.g.

- the value of the page title
- some content in the body

Then write the test.

- Give the test case an appropriate name
- Import the Page fixture. This fixture maintains test isolation and takes care of setup and
  teardown.
- Use `page.goto` to the URL of your server.
- Optionally, locate an element within the page e.g. `page.locate("body")` finds the `<body>` tag.
- Import the `expect` method from Playwright. Use the Playwright assertion to check the value of
  the element you decide to test for e.g.

    - `expect(page).to_have_title("Paralympics")`
    - `expect(page.locator("body")).to_be_visible()`
    - `expect(page.locator("body")).to_be_attached()`

An example is given below, though try to write your own rather than just copying this.

Run your test from the terminal in the IDE e.g.
`pytest --headed -v tests/test_paralympics.py::test_page_has_body`

Did it pass?

```python
# Imports from Playwright
from playwright.sync_api import Page, expect


# The Page fixture and app_server fixture are parameters for the method
def test_page_has_body(page: Page, app_server):
    """
    GIVEN a server URL (app_server fixture yields the URL)
    WHEN the 'home' page is requested
    THEN the home page body should be displayed
    """
    # Use the page to go to the URL, in this case the app_server fixture yield the URL
    page.goto(dash_app_server)
    expect(page.locator("body")).to_be_visible()
    # For Streamlit use: expect(page.locator("body")).to_be_attached() or expect(page).to_have_title("Paralympics Dashboard") 
```

## Test that a line chart is generated

In this test, use Playwright to navigate to the dropdown that chooses the chart, choose the line
chart and then check that the chart is present.

To check that the chart is present you can check for the presence of "js-plotly-plot", which is
usually included in a plotly chart HTML/js, using
`await expect(page.locator(".js-plotly-plot")).to_be_visible()`

1. Give the test case an appropriate name
2. Use `page.goto` to the URL of your server (or route URL if in Flask).
3. In your app code, find the `id` for dropdown that lets you choose the question for the charts,
   and find the value of the option for the line chart. Omit this step in Flask as you have a route
   for each chart instead of the selector.
4. Use `page.locate("#the-id-of-your-select")` to find the dropdown and combine this with
   the [action](https://playwright.dev/python/docs/input) to select an option e.g.
   `page.locator("#select-chart").select_option("line")`
5. Find the `id` for the second dropdown that select the type of data for the line chart and the
   value of the option for `sports`
6. Use the `page.locate().selection_option()` to select the sports option
7. Use an assertion that shows the chart has displayed

My code is as follows, but this may not work if you just copy and paste. Check the logic and ids
used in your app.

```python
def test_line_chart_displays(page: Page, dash_app_server):
    # GIVEN a server URL
    page.goto(dash_app_server)
    # WHEN the 'home' page is requested AND the line chart is chosen
    page.locator("#select-chart").select_option("line")
    # AND the sports data is chosen
    page.locator("#line-select").select_option("sports")
    # THEN a plotly line chart should be visible
    expect(page.locator(".js-plotly-plot")).to_be_visible()
```

Streamlit version of this is:

```python
def test_line_chart_displays(page: Page, app_server):
    # WHEN the home page is selected
    page.goto(app_server)

    # AND the line chart is chosen from the chart selector
    chart_select = page.get_by_test_id("stSelectbox").filter(has_text="Choose a chart:")
    selectbox_input = chart_select.locator("input")
    selectbox_input.click()
    selectbox_input.fill("Trends")
    selectbox_input.press("Enter")

    # AND the sports data is chosen from the second selector
    chart_select = page.get_by_test_id("stSelectbox").filter(has_text="Choose feature:")
    selectbox_input = chart_select.locator("input")
    selectbox_input.click()
    selectbox_input.fill("Sports")
    selectbox_input.press("Enter")

    # THEN a plotly line chart should be visible
    expect(page.locator(".js-plotly-plot")).to_be_visible()
```

Now try and add a test for each of the other two charts.

Challenge:
use [parameterisation](https://docs.pytest.org/en/stable/how-to/parametrize.html#parametrize-basics)
to test for the 3 variants of the line chart 'sports', 'events', 'participants'

## Test that the quiz moves to the next question when a correct answer is submitted

Use Playwright codegen to navigate to a question, select a correct response, and press submit.

- Run the REST API and the Dash/Flask/Streamlit app.
- In the IDE terminal enter
  `playwright codegen http://127.0.0.1:8050` `:8050` is the Dash default port, change this to
  your app's port.
- Navigate to question section. Answer the first question correctly.
- Press 'stop recording' on the codegen menu that appears over the browser.
- Use the find locator icon and then click on something in the second question. The playwright
  inspector will give you the locator.

Use the code from codegen to help you write a test.

Stop the two apps from running after you have the code from codegen, and before you run the test
code.

This is my test, it may not work for your app!

```python
def test_answer_question_correct(page: Page, dash_app_server):
    """
    GIVEN a server URL
    WHEN the 'home' page is requested
    AND the answer to a question is selected and submitted and is correct
    THEN a new question should be displayed
    """
    page.goto(dash_app_server)
    page.get_by_role("radio", name="Lillehammer").check()
    page.get_by_role("button", name="Submit answer").click()
    expect(page.get_by_text("How many participants were")).to_contain_text("?")
```

There is a flaw in this test, for example, what if the first or second question text changes?
Improve the reliability of the test, e.g. find the value of the label for the question and check
that it changes? Use a different [assertion](https://playwright.dev/python/docs/test-assertions)?

Streamlit solution:
```python
def test_answer_question_correct(page: Page, app_server):
    """
    GIVEN a server URL
    WHEN the 'home' page is requested
    AND the answer to a question is selected and submitted and is correct
    THEN a new question should be displayed
    """
    page.goto(app_server)
    initial_q = page.get_by_text("In which winter Paralympics were").text_content()
    page.get_by_text("Lillehammer").click()
    page.get_by_test_id("stBaseButton-secondaryFormSubmit").click()
    next_q = page.get_by_text("How many participants were").text_content()
    assert initial_q != next_q  # pytest assertion
```

## Test creating a new question succeeds

You should now be able to attempt this as you have the knowledge needed.

My solution below is for my Dash app. You need to find the ids, or other locators, for your app.
Try the Codegen tool if you don't know which locators you can use.

```python
def test_new_question_submitted(page: Page, app_server):
    """
    GIVEN a server URL
    WHEN the home page is requested and the Teacher admin tab is selected (<a role="tab">Teacher admin</a>)
    AND textarea with id="question_text" has the text for a new question entered
    AND response_text_0, response_text_1, response_text_2 and response_text_3 are completed
    AND one of is_correct_0, is_correct_1, is_correct_2 and is_correct_3 is True
    AND "new-question-submit-button" is clicked
    THEN if the requests to the REST API with a new question and 4 responses are successful, a
    response should be displayed to the 'id="new-question-submit-button" 
    with text "Question saved successfully.".
    """
    page.goto(app_server)
    page.get_by_role("tab").get_by_text(re.compile("teacher admin", re.IGNORECASE)).click()
    page.locator("#question_text").fill("New question")
    page.locator("#response_text_0").fill("A is correct")
    page.locator("#response_text_1").fill("B is incorrect")
    page.locator("#response_text_2").fill("C is incorrect")
    page.locator("#response_text_3").fill("D is incorrect")
    page.locator("#is_correct_0").check()
    page.locator("#new-question-submit-button").click()
    expect(page.locator("#form-message")).to_contain_text("Question saved successfully.")
```

Note for Streamlit I found it easier to tab to each input on the form instead:

```python
def test_new_question_submitted(page: Page, app_server):
    page.goto(f"{app_server}/teacher_admin")
    question_text = page.get_by_role("textbox", name="Enter the question")
    question_text.click()
    question_text.fill("A new question.")
    question_text.press("Tab")
    page.keyboard.type("A is correct")
    page.keyboard.press("Tab")
    page.keyboard.press("Space")  # Toggle (check) the checkbox
    page.keyboard.press("Tab")
    page.keyboard.type("B is incorrect")
    page.keyboard.press("Tab")
    page.keyboard.press("Tab")
    page.keyboard.type("C is incorrect")
    page.keyboard.press("Tab")
    page.keyboard.press("Tab")
    page.keyboard.type("D is incorrect")
    page.keyboard.press("Tab")
    page.keyboard.press("Tab")
    page.get_by_role("button", name="Save Question").click()
    expect(page.get_by_text("Question saved")).to_contain_text("Question saved")
```

## Going further

1. Try to think of some more tests and write them.

There are many more tests you could write e.g., what happens when the wrong data is entered in
the new question form? What happens when someone presses submit on the question/answer feature
before making a choice? etc.

2. Investigate the [mock API](https://playwright.dev/python/docs/mock) features of Playwright

Try to implement this for one of the tests that uses REST API integration, e.g.

- the question/answer features makes GET requests
- the teacher admin add new question makes POST requests

## Next activity

The next activity is specific to each framework.

[Next activity Dash](4-1-dash-selenium.md)

[Next activity Flask](4-flask-test-client.md)

[Next activity Streamlit](4-streamlit-tests.md)
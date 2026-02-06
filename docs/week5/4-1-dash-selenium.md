# 4.1. DASH: Selenium webdriver

**This is an alternative to Playwright. If you plan to use Playwright then skip this.** 

Do not create Selenium and Playwright tests for the coursework, they are alternatives, so writing 
both will not increase the marks awarded.

## Introduction

These examples use the Selenium webdriver and the ChromeDriver.

The driver allows you to navigate the web page and carry out actions such as clicking, selecting,
entering data in forms etc.

You then use pytest assertions to compare values of those elements against an expected value.

Documentation you may need:

- [Selenium documentation with examples](https://www.selenium.dev/documentation/webdriver/)
- [Selenium API reference](https://selenium-python.readthedocs.io/api.html)
- [Dash duo API functions (shorthand for some of the Selenium functions)](https://dash.plotly.com/testing#browser-apis)
- [HTML tag reference](https://www.w3schools.com/tags/default.asp)

## Dash duo functions versus Selenium Webdriver functions

Dash has shorthand API functions for some Selenium webdriver functions, but not all. The syntax
differs to the Selenium function. You can use either version of the functions in your code.

An example of the two variants to find a `<h1>` tag:

- `dash_duo.driver.find_element(By.TAG_NAME, "h1")` uses the driver followed by the Selenium
  function
- `dash_duo.find_element("h1")` is the dash_duo shorthand function

## How to find an element on a page

Selenium WebDriver targets elements on the page. Dash uses the word 'component' rather than element.
This refers to something defined on the web page such as an HTML heading, an image, etc.

There are ways to identify (locate) elements on the page:

- by their HTML id
- by their CSS class or selector
- by HTML tag name
- by finding an element relative to another element
- by XPATH

See references for more detail:

- [Selenium locator strategies](https://www.selenium.dev/documentation/webdriver/elements/locators/)
- [Selenium methods to find elements](https://www.selenium.dev/documentation/webdriver/elements/finders/)

As an `id` has to be unique on an HTML page, this is the most convenient method. Use this where
possible.

For example:

```python
from selenium.webdriver.common.by import By

# Get the element with the id "fruit" using the Selenium function
fruit = dash_duo.driver.find_element(By.ID, "fruit")

# Using the Dash function alternative uses CSS selectors, so "#" before the id name denotes it is an ID
fruit = dash_duo.find_element("#fruit")
```

The Dash browser API finds elements by their CSS selector. These are:

- `#id` to find an element with an id, e.g. `#line-chart` to find an element with `id='line-chart'`
- HTML TAG to find en element by its HTML tag name e.g. `p` to find all `<p>` elements
- `.class` to find an element by CSS class name, e.g. `.alert` to find all elements with a
  `class="alert"` (or className="alert" in Dash).

Using either API you can find either a single element `find_element`, or all elements that match a
condition on a page `find_elements`.

## Concept: Waits

Test code may execute faster than the browser responds.

When you use Selenium functions to navigate the page and interact with elements, you may need to
wait for the page to respond or update before you can continue.

There are two types of waits in Selenium:

- explicit [waits](https://www.selenium.dev/documentation/en/webdriver/waits/)
  for [an expected condition](https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html?highlight=expected)
  to be true, e.g., until a particular element is displayed.
- implicit [waits](https://www.selenium.dev/documentation/webdriver/waits/#implicit-waits) that wait
  for a specific period.

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Implicit wait for 2 seconds
driver.implicitly_wait(2)

# Wait for 10 seconds until the element with ID of "myElement" is present on the web page
# General syntax for explicit wait: WebDriverWait(driver, timeout=int_in_seconds).until(some_condition)
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "myElement")))
```

The Dash API also offers specific [wait functions](https://dash.plotly.com/testing#browser-apis).

## Use an assertion on a value of the located element

Used the webdriver to find an element and capture a value from it to use in an assertion.

Examples of the values you can get from the webdriver to use in assertions:

```python
# Get browser information
title = driver.title
url = driver.current_url
# Get information about an element e.g. 
value = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']:first-of-type").is_selected()
# Get text content from an element
text = driver.find_element(By.CSS_SELECTOR, "h1").text
```

### Write a test to check content on the page

This assumes you have a `H2` heading on the page, if you don't then find something else to assert
the presence of.

The dash_duo fixture both runs the app server and creates a webdriver. You don't need to write
a fixture for this.

```python
from dash.testing.application_runners import import_app


def test_h2_text_equals(dash_duo):
    """
    GIVEN the app is running (dash_duo runs the app and provides a webdriver)
    WHEN the home page is available
    THEN the first h2 element should have the text 'Charts'
    """
    # Start the server
    app = import_app(app_file="paralympics.app")
    dash_duo.start_server(app)

    # Uses a Dash API function to wait for a h2 element on the page
    dash_duo.wait_for_element("h2", timeout=4)

    # Find all H2 elements on the page
    h2_els = dash_duo.find_elements("h2")

    # Assert that the first h2 heading text is "Charts"
    assert h2_els[0].text == "Charts"
```

Run the test.

## Interacting with elements on a web page

[Selenium documentation: Interactions](https://www.selenium.dev/documentation/webdriver/elements/interactions/)

Basic commands for interacting include click(), send_keys(), clear(), select().

For example, to complete and submit a form with a first-name field:

```python
from selenium.webdriver.common.by import By

# Find the element
first_name = driver.find_element(By.name, "first-name")
# Enter the text "Charles"
first_name.send_keys("Charles")
# Fina and click on the form submit button
driver.find_element(By.TAG_NAME, "input[type='submit']").click()
```

### Write a test that when the line chart displays

The test specification is:

```text
GIVEN a server
WHEN the selector with id=`select-chart` is found and the option with value=`line` selected
AND the selector with id=`line-select` is visible and the option with value=`sports` selected
THEN a plotly chart with the css class `.js-plotly-plot` should be present
```

You may have different ids in your layout so check your own code.

The following is partially completed solution, finish the code then run the test:

```python
def test_line_chart_displays(dash_duo):
    # Start the server
    app = import_app(app_file="paralympics.app")
    dash_duo.start_server(app)

    # Choose the 'line' chart type
    dash_duo.wait_for_element("#select-chart", timeout=4)
    dash_duo.find_element("#select-chart option[value='line']").click()

    # Wait for the line-specific selector and choose 'sports'

    # Assert a Plotly chart is present


```

Implement the code and run the test.

## Concept: Action chains

The Actions API provides ActionChains. This allows you to 'chain', or add together, sequences of
interactions.

You may not need to use this in your tests. However, while [selenium interaction functions](https://www.selenium.dev/documentation/webdriver/elements/interactions/)
include click(), send_keys(), submit() and clear(); some interactions, such as `hover` are only
available in the [Actions API](https://www.selenium.dev/documentation/webdriver/actions_api/).

## Challenge: Write a test to for the teacher admin tab to create a new multichoice question

The test spec is:

```text
"""
    GIVEN a server URL
    WHEN the Teacher admin tab is selected (<a role="tab">Teacher admin</a>)
    AND textarea with id="question_text" has the text for a new question entered
    AND response_text_0 to response_text_3 are completed with text
    AND is_correct_0 is checked
    AND the button with id='new-question-submit-button' is clicked
    THEN the element with id='form-message' contains "Question saved successfully."
    """
```

[Next activity](4-2-dash-callbacks.md)
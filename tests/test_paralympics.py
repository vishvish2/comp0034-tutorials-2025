from pathlib import Path
from playwright.sync_api import Page, expect
from streamlit.testing.v1 import AppTest

at = AppTest.from_file("src/paralympics/app.py").run()
APP_FILE = Path(__file__).parent.parent.joinpath(
    "src", "paralympics", "app.py")


def test_questions_header():
    """
    GIVEN a test app
    WHEN the page is requested
    THEN there should be a header with the text "Questions"
    """
    # Load the Streamlit app from file and run it
    app_file = Path(__file__).parent.parent.joinpath("src", "paralympics",
                                                     "app.py")
    at = AppTest.from_file(app_file).run()
    # App ran without error
    assert not at.exception
    # Access the header value and assert it is "Questions"
    assert at.header[0].value == "Questions"
    # Alternatively, assert that at least one header has the work question,
    # case in-sensitive
    assert any("question" in h.value.lower() for h in at.header), \
        "No header contains 'question'"


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


# The Page fixture and app_server fixture are parameters for the method
def test_page_has_body(page: Page, app_server):
    """
    GIVEN a server URL (app_server fixture yields the URL)
    WHEN the 'home' page is requested
    THEN the home page body should be displayed
    """
    # Use the page to go to the URL, in this case the app_server fixture yield
    # the URL
    page.goto(app_server)
    expect(page).to_have_title("Paralympics Dashboard")

    # expect(page.locator("body")).to_be_visible()
    # For Streamlit use: expect(page.locator("body")).to_be_attached() or
    # expect(page).to_have_title("Paralympics Dashboard")


def test_line_chart_displays(page: Page, app_server):
    # WHEN the home page is selected
    page.goto(app_server)

    # AND the line chart is chosen from the chart selector
    chart_select = page.get_by_test_id("stSelectbox").filter(
        has_text="Choose a chart:")
    selectbox_input = chart_select.locator("input")
    selectbox_input.click()
    selectbox_input.fill("Trends")
    selectbox_input.press("Enter")

    # AND the sports data is chosen from the second selector
    chart_select = page.get_by_test_id("stSelectbox").filter(
        has_text="Choose feature:")
    selectbox_input = chart_select.locator("input")
    selectbox_input.click()
    selectbox_input.fill("Sports")
    selectbox_input.press("Enter")

    # THEN a plotly line chart should be visible
    expect(page.locator(".js-plotly-plot")).to_be_visible()

# 1. Intro to testing from the web browser

## Introduction

In COMP0035 you learned:

- test naming conventions
- using 'Given-When-Then' and 'Act-Arrange-Assert' to help to define a test case
- writing unit tests with pytest, including creating fixtures and the use of `conftest.py`
- running the tests on a continuous integration platform such as GitHub Actions
- report test coverage, i.e. the extent to which the tests exercise the application's source code

The focus of this tutorial is testing the typical sequences of actions a user would perform when
interacting with the app in a browser. This type of testing is often called integration testing,
system testing or browser testing.

In this approach, you write test code that interacts with your application as if it were a user in a
browser—navigating to pages, clicking buttons, entering text into forms, and so on. The browser
interactions return responses that you can inspect to make assertions.

To do this, you need additional software capable of automating a browser, alongside the test
library (pytest).

The course activities use Playwright for Python. An alternative is Selenium WebDriver, which some
students using Dash may prefer as it is included in the Dash documentation. Playwright can be used
for all three of the app frameworks.

## Install Playwright (or Selenium Webdriver)

You need install one of the following combinations in your virtual environment.

Playwright is suggested unless you prefer to use Selenium Webdriver.

- [Playwright (Python)](https://pypi.org/project/pytest-playwright/)

    1. Install the Playwright Python package: `pip install pytest-playwright` (Note:
       pytest-playwright installs pytest as a dependency.)
    2. Install the Playwright browser binaries: `playwright install`

- [Selenium webdriver](https://www.selenium.dev/documentation/webdriver/) + Chromedriver + pytest

    1. Install Selenium webdriver: `pip install selenium`
    2. Install pytest: `pip install pytest`
    3. Download and install [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/)

Selenium interacts with the browser, and ChromeDriver is the bridge that allows Selenium to drive
the Chrome browser. Drivers are available for other browsers. For the coursework please use
ChromeDriver to facilitate marking.

**Important**:
ChromeDriver is a standalone utility that must match:

- your operating system, and
- the version of Chrome installed on your computer.

You cannot install ChromeDriver using `pip install`; you must download the correct version manually
and place it somewhere on your system's PATH.

Every time Chrome is updated, you also need to update the ChromeDriver.

1. Find the version of Chrome you're using (in the Settings | About Chrome in the Chrome app)
2. Go to [the chromedriver downloads page](https://googlechromelabs.github.io/chrome-for-testing/)
3. Find the relevant **chromedriver** (take care not to choose just **chrome** by mistake), copy the
   URL.
4. Use the URL to retrieve a small zip file containing the version of ChromeDriver to use.
5. Extract the zipped folder to get the `chromedriver.exe` executable file
6. Place this `chromedriver.exe` file in a location that is in the `Path` of your operating system.

You may need to refer to the following:

- [Chromedriver documentation on referencing the driver location](https://developer.chrome.com/docs/chromedriver/get-started)
- [Chromedriver documentation on version selection](https://chromedriver.chromium.org/downloads/version-selection)
  explains options for installation.

_Note for Mac users_:

You may get a security warning preventing you from opening `chromedriver.exe`.

I solve by:

- open Finder
- right-click on `chromedriver.exe` and choose to open in Terminal.
- OK if asked "are you sure".
- Once you've opened and run it, stop it running.
- The permissions to open the file will now be set.
- You can now move the file, `usr/local/bin` is a common location for macOS.

## Enable your IDE to run pytest

You may need to configure your IDE to support running pytest tests, follow the relevant
documentation:

- [Pycharm help: Testing frameworks](https://www.jetbrains.com/help/pycharm/testing-frameworks.html)
- [Python testing in VS Code](https://code.visualstudio.com/docs/python/testing)

## General steps to write UI tests

The general approach is:

- run the data REST API in a thread
- run the front end app in a thread
- {Selenium} create an instance of a driver and use the driver to navigate to a URL in your app
- {Playwright} create an instance of Page and use it to navigate to a URL in your app
- carry out a sequence of interactions on the browser that mimic what a user would do
- find a value on the page that you can use in an assertion to confirm that the test passed

The following activities cover these steps.

[Next activity](4-2-test-app-url.md)

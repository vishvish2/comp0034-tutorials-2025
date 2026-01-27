# COMP0034 2025-26 tutorial activities

## Setup

1. Fork this repository to create a linked copy in your own GitHub account
2. Clone your fork to your IDE (VS Code, PyCharm)
3. Create and activate a virtual environment
4. Install the package dependencies e.g. `pip install -e .`

## Activities

It is intended that after the first week you will choose a web app framework to use and thereafter
follow the activities related to that framework.

Due to the different libraries required for each of the web app frameworks used in this course,
after the first week the source code for the apps is not maintained in this repository. There will 
be separate repos for each app.

Intended course structure:

1. Week 1 Application frameworks and basic app structure
2. Week 2 Layout, styling and navigation
3. Week 3 Creating charts
4. Week 4 Additional features
5. Week 5 Testing from the web browser (playwright or selenium webdriver)
6. Week 6 REST API and basic FastAPI app
7. Week 7 Models, schemas and routers
8. Week 8 Integration with the front-end app
9. Week 9 Testing
10. Week 10 No new content

## F.A.Q.
1. I am getting an error called 'SSL: CERTIFICATE_VERIFY_FAILED' on MacOS
   - Open Finder > Applications > Python 3.XX (could be 3.8, 3,12m etc.) > Install Cerfiticate.command
2. I am getting an error: 'RuntimeError: Unexpected error loading event data: Missing optional dependency 'openpyxl'.
   - Check that you have `openpyxl` installed and install if missing `pip install openpyxl`.
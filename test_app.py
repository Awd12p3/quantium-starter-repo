import os
from webdriver_manager.chrome import ChromeDriverManager

# Get the full path to the chromedriver executable
driver_path = ChromeDriverManager().install()
# Append the directory containing chromedriver to PATH
os.environ["PATH"] += os.pathsep + os.path.dirname(driver_path)
    

import pytest
from app import app

def test_header(dash_duo):
    # Start the server with the Dash app
    dash_duo.start_server(app)
    # Find the header element (the H1 element)
    header = dash_duo.find_element("h1")
    # Verify the header text is correct
    assert "Sales Data Visualiser" in header.text

def test_visualisation(dash_duo):
    # Start the server with the Dash app
    dash_duo.start_server(app)
    # Wait for the graph element to appear (the Graph component has id 'sales-line-chart')
    dash_duo.wait_for_element("#sales-line-chart", timeout=10)
    # Attempt to find the graph element
    graph = dash_duo.find_element("#sales-line-chart")
    # Verify the graph is present
    assert graph is not None

def test_region_picker(dash_duo):
    # Start the server with the Dash app
    dash_duo.start_server(app)
    # Wait for the region picker element (the RadioItems component with id 'region-radio')
    dash_duo.wait_for_element("#region-radio", timeout=10)
    # Attempt to find the radio element
    region_picker = dash_duo.find_element("#region-radio")
    # Verify the region picker is present
    assert region_picker is not None

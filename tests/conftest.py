import json

import pytest
from selenium import webdriver
from config.settings import BASE_DIR
from config.settings import ROOT_URL

"""
Selenium Test Automation Fixtures.

Contains Pytest fixtures for setting up auto tests.
"""


@pytest.fixture
def root_url():
    """
    Fixture for the root URL for tests.
    :return:
        str: The root URL.
    """
    return ROOT_URL


@pytest.fixture
def get_config_file_path():
    """
        Fixture for the path to the test configuration json file.
        :return:
            Path: The path to the test configuration file.
        """
    return BASE_DIR / 'config' / 'test_config.json'


@pytest.fixture(scope='session')
def config():
    """
    The fixture loads the configuration file for tests.
    :return:
        dict: Data from the configuration file.
    """
    with open(get_config_file_path()) as config_file:
        config = json.load(config_file)
    return config


def set_options(opts, config):
    """
    Helper function that sets options for the browser.

    :return: None
    """
    if config['mode'] == 'Headless':
        opts.add_argument('--headless=new')


@pytest.fixture
def browser(config):
    """
    Fixture for configuring a WebDriver instance.

    :return: None
    """
    if config['browser'] == 'Chrome':
        opts = webdriver.ChromeOptions()
        set_options(opts, config)
        driver = webdriver.Chrome(options=opts)
    elif config['browser'] == 'Firefox':
        opts = webdriver.FirefoxOptions()
        set_options(opts, config)
        driver = webdriver.Firefox(options=opts)
    else:
        raise Exception('Unknown type of browser')

    yield driver

    driver.quit()


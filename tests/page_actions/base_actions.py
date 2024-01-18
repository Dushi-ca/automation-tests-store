from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.common.action_chains import ActionChains


class BaseActions:
    """Initializing the BaseActions class using Selenium WebDriver and Base URL.

          Options:
          - driver: Selenium WebDriver instance
          - base_url (str): base URL"""
    def __init__(self, driver, base_url=None):
        self.driver = driver
        if base_url is None:
            raise Exception('Please provide url')
        self.base_url = base_url

        self.action_chain = ActionChains(driver)

    def find_element(self, locator, timeout_sec=10):
        """A method that allows you to search for page elements by passing a locator"""
        return WebDriverWait(self.driver, timeout_sec).until(EC.presence_of_element_located(locator))
        message = f'Can\'t find element by locator'

    def click_on(self, locator):
        """Finds a web element using a locator and performs a click"""
        self.find_element(locator).click()

    def navigate_to(self, url=''):
        """Navigates to the specified URL."""
        url_to = self.base_url + url
        self.driver.get(url_to)

    def get_title(self):
        """Gets the page title"""
        return self.driver.title

    def enter_text(self, locator, txt):
        """The method finds the element and enters the specified text"""
        self.find_element(locator).send_keys(txt)

    def wait_until_visibility_of_element_located(self, locator):
        """Waits until the element found by the locator becomes visible on the page"""
        WebDriverWait(self.driver, timeout=10).until(EC.visibility_of_element_located(locator))

    def wait_until_invisibility_of_element_located(self, locator, text):
        """Waits until an element with the specified text found using the locator becomes invisible on the page"""
        WebDriverWait(self.driver, timeout=10).until_not(EC.text_to_be_present_in_element(locator, text))

    def move_to_element(self, locator):
        """Moves the mouse pointer to the specified element found using the locator."""
        element = self.find_element(locator)
        self.action_chain.move_to_element(element).perform()


from tests.page_actions.base_actions import BaseActions
from tests.utils.locators import MainPageLocators


class MainActions(BaseActions):
    """ Definition the MainActions class, inheriting from BaseActions"""
    def __init__(self, driver, base_url=None):
        super(MainActions, self).__init__(driver, base_url=base_url)

    def go_to_catalog_page(self):
        self.move_to_element(MainPageLocators.PAGE_CATALOG)
        self.click_on(MainPageLocators.START_PURCHASE)

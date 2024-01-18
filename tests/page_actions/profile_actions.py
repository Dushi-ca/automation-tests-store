from tests.page_actions.base_actions import BaseActions
from tests.utils.locators import ProfilePageLocators


class ProfileActions(BaseActions):
    """ Definition the ProfileActions class, inheriting from BaseActions"""
    def get_cart_title_item(self):
        """
        Gets the title of the added item in the cart.

        :return: Added item text.
        """
        return self.find_element(ProfilePageLocators.added_item_title).text

    def remove_item_from_cart(self):
        """
        Method waits the element TRASH, clicks on the trash element to remove and
        waits for the item to become invisible to ensure the item is removed.

        :return: None
        """
        self.wait_until_visibility_of_element_located(ProfilePageLocators.TRASH)
        self.click_on(ProfilePageLocators.TRASH)
        self.wait_until_invisibility_of_element_located(ProfilePageLocators.CHECKOUT, "Checkout")

    def get_message_of_empty_cart(self):
        """
        Gets message of empty cart.

        :return: Item text in empty cart.
        """
        return self.find_element(ProfilePageLocators.EMPTY_CART).text

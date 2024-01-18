from bs4 import BeautifulSoup
from tests.page_actions.base_actions import BaseActions
from tests.utils.locators import CatalogPageLocators, BasePageLocators


class CatalogActions(BaseActions):
    """
    The CatalogActions class provides methods for performing actions on catalog pages:

    - getting card names, adding items to cart,
    - go to profile and cart pages
    - analysis of product names from the navigation panel.
    """
    def __init__(self, driver, base_url=None):
        super(CatalogActions, self).__init__(driver, base_url=base_url)
        self.base_url = base_url + '/index.php?route=product/category&path=18'

    def get_card_title(self):
        """Gets the title of the card on the catalog page."""
        return self.find_element(CatalogPageLocators.CARD_TITLE).text

    def add_item_to_cart(self):
        """Finds the card footer element on the catalog page and clicks to add the item to cart."""
        card_footer = self.find_element(CatalogPageLocators.CARD_FOOTER)
        card_footer.click()

    def go_to_profile_page(self):
        """Goes to the profile page using the locators to the profile page and login page."""
        self.click_on(BasePageLocators.PROFILE_PAGE)
        self.click_on(BasePageLocators.LOGIN_PAGE)

    def go_to_cart_page(self):
        """Goes to the cart page."""
        self.click_on(CatalogPageLocators.ADD_TO_CART)
        self.click_on(CatalogPageLocators.CART)

    def get_names_from_category(self, category_url):
        """
       Retrieves the titles of products from a specified category page.

       Parameters:
       - category_url (str): The URL of the category page to extract product titles from.

       Returns:
       list: A list containing the titles of products in the specified category.
             Returns an empty list if no products are found.
        """
        self.driver.get(category_url)
        self.driver.maximize_window()
        bs = BeautifulSoup(self.driver.page_source, 'html.parser')

        # find the product-layout class
        rows = bs.find_all('div', attrs={'class': 'product-layout'})

        products = []

        # if nothing is found then return an empty list

        if not rows:
            return products

        # if the class is found, then take the headers from the product card
        for row in rows:
            title = row.find('h4').text
            products.append(title)

        return products

# Функция парсит навбар, обнаруживая является ли элемент навбара дропдауном или ссылкой,
# в первом случае парсит дропдаун и добавляет ссылки на категории, во втором добавляет категорию
    def parse_navbar(self, root_url):
        """
       Parses the navbar on the page to extract product names from categories.

       Parameters:
       - root_url (str): The URL of the root page with the navigation bar.

       Returns:
       set: a set containing unique names of products from categories on the navbar.
        """
        self.driver.get(root_url)

        self.driver.maximize_window()

        bs = BeautifulSoup(self.driver.page_source, 'html.parser')

        navbar = bs.find('ul', attrs={'class': 'nav navbar-nav'})

        category_links = [el['href'] for el in navbar.find_all('a')]

        products = []

        for link in category_links:
            products += (self.get_names_from_category(link))
            products = set(products)
        return products
from selenium.webdriver.common.by import By


class BasePageLocators:
    LOGIN_PAGE = (By.LINK_TEXT, 'Login')
    PROFILE_PAGE = (By.LINK_TEXT, 'My Account')


class MainPageLocators:
    PAGE_CATALOG = (By.LINK_TEXT, 'Laptops & Notebooks')
    START_PURCHASE = (By.LINK_TEXT, 'Show All Laptops & Notebooks')


class CatalogPageLocators:
    CARD_TITLE = (By.TAG_NAME, 'h4')
    CARD_FOOTER = (By.XPATH, '''//button[@onclick="cart.add('47', '1');"]''')
    ADD_TO_CART = (By.ID, 'button-cart')
    CART = (By.LINK_TEXT, 'Shopping Cart')


class ProfilePageLocators:
    CHECKOUT = (By.CSS_SELECTOR, 'a.btn.btn-primary')
    EMPTY_CART = (By.XPATH, '//*[@id="content"]/p')
    TRASH = (By.XPATH, '//button[@data-original-title = \'Remove\']')
    added_item_title = (By.LINK_TEXT, 'HP LP3065')

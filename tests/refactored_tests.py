from tests.page_actions.main_actions import MainActions
from tests.page_actions.catalog_actions import CatalogActions
from tests.page_actions.profile_actions import ProfileActions
import os


def test_titles_are_correct(browser, root_url):

    main_page = MainActions(browser, root_url) # создаем объект класс MainPage, передаём браузер
    main_page.navigate_to()

    main_title = main_page.get_title()
    assert main_title == 'Your Store'

    main_page.go_to_catalog_page()

    catalog_page = CatalogActions(browser)
    catalog_title = catalog_page.get_title()
    assert catalog_title == 'Laptops & Notebooks'


def test_add_to_cart_and_remove(browser, root_url):
    catalog_page = CatalogActions(browser, root_url)
    catalog_page.navigate_to()

    card_title = catalog_page.get_card_title()
    catalog_page.add_item_to_cart()

    catalog_page.go_to_cart_page()

    profile_page = ProfileActions(browser)
    added_item_title = profile_page.get_cart_title_item()
    assert card_title == added_item_title

    profile_page.remove_item_from_cart()
    assert profile_page.get_message_of_empty_cart() == 'Your shopping cart is empty!'


def test_bs_navbar(browser, root_url):
    catalog_page = CatalogActions(browser, root_url)
    catalog_page.parse_navbar(root_url)

    file_path = os.path.relpath('products.txt')

    try:
        os.remove(file_path)
        print("File deleted successfully")
    except FileNotFoundError:
        print("File not found")

    try:
        with open(file_path, 'x') as file:
            file.write('\n'.join(catalog_page.parse_navbar(root_url)))
        print('Data is written to products.txt.')
    except Exception as e:
        print(f"An error occurred while writing to file: {e}")

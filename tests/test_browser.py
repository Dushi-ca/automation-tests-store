import concurrent
import time
from telnetlib import EC
import pytest
from pycparser.c_ast import ID
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import BASE_DIR
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from concurrent.futures import ThreadPoolExecutor

@pytest.fixture
def headless_chrome():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')

    browser = webdriver.Chrome(options=options)
    yield browser

    browser.quit()


def test_changing_size_window(browser, root_url):
    browser.get(root_url)
    browser.minimize_window()
    time.sleep(5)
    browser.close()


def _switch_to_another_handler(browser, original_page_handler):
    for window_handle in browser.window_handles:
        if window_handle != original_page_handler:
            browser.switch_to.window(window_handle)
            break


"""Extracting titles in product cards from HTML and writing to a file using Beautiful Soup"""


def test_beautiful_soap(browser, root_url):
    browser.get(root_url)
    browser.maximize_window()

    bs = BeautifulSoup(browser.page_source, 'html.parser') # browser.page_source передаёт всю html-страницу
    rows = bs.find_all('div', attrs={'class': 'product-thumb transition'})

    products = []

    for row in rows:
        title = row.find('h4').text
        products.append(title)

    try:
        with open('products.txt', 'x') as file:
            file.write('\n'.join(products))
    except FileExistsError:
        print("The file already exists")
    except FileNotFoundError:
        print("File doesn't exist")

    urls = [root_url, 'https://opencart.abstracta.us/index.php?route=product/category&path=33', 'https://opencart.abstracta.us/index.php?route=product/category&path=24']

    with webdriver.Chrome() as browser_instance:
        # Создание ThreadPoolExecutor с максимальным количеством потоков
        with ThreadPoolExecutor(max_workers=3) as executor:
            # Асинхронный вызов test_beautiful_soap для каждого URL
            future_to_url = {executor.submit(test_beautiful_soap, browser_instance, url): url for url in urls}

            # Получение результатов по мере завершения задач
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    future.result()  # Подождать завершения задачи и получить результат (если есть)
                    print(f"Scraping for {url} completed successfully.")
                except Exception as e:
                    print(f"Error scraping {url}: {e}")





def test_interaction_with_tabs_or_windows(browser, root_url):
    browser.get(root_url)
    browser.maximize_window()

    original_page_handler = browser.current_window_handle

    login_page_link = browser.find_element(By.ID, 'bitnami-banner')
    login_page_link.click()

    _switch_to_another_handler(browser, original_page_handler)

    login_title = browser.find_element(By.XPATH, '//div/h1').text
    assert login_title == 'This is a Cloud Image for OpenCart built by Bitnami.'

    browser.close()


def test_interactions(browser, root_url):
    browser.get(root_url)
    browser.maximize_window()
    browser.find_element(By.CLASS_NAME, 'fa.fa-user').click()
    browser.find_element(By.LINK_TEXT, 'Register').click()

    first_name = browser.find_element(By.ID, "input-firstname")
    first_name.send_keys('Anna')

    last_name = browser.find_element(By.ID, "input-lastname")
    last_name.send_keys('Ivanova')

    assert first_name.get_attribute('value') == 'Anna'
    assert last_name.get_attribute('value') == 'Ivanova'

    agreement = browser.find_element(By.NAME, 'agree')
    agreement.click()
    assert agreement.is_selected()

    agreement.click()
    assert agreement.is_selected() is False


def test_find_by_xpath(browser, root_url):
    browser.get(root_url)
    browser.maximize_window()

    el1 = browser.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/div/div[3]/button[1]')
    el2 = browser.find_element(By.XPATH, '//*[@id="top-links"]/ul/li[2]/a/span[1]')

    assert el1.text == "ADD TO CART"
    print("True")
    assert el2.text == "My Account"
    print("True")


def test_find_by_ccs_selectors(headless_chrome, root_url):
    headless_chrome.get(root_url)
    headless_chrome.maximize_window()

    el1 = headless_chrome.find_element(By.CSS_SELECTOR,
                               '.swiper-slide.text-center.swiper-slide-duplicate.swiper-slide-duplicate-active')
    el2 = headless_chrome.find_element(By.CSS_SELECTOR, '.btn.btn-default.btn-lg')

    el_list = [el1, el2]
    assert all(el is not None for el in el_list)

    try:
        # el1 = browser.find_element(By.CSS_SELECTOR, '.swiper-slide.text-center.swiper-slide-duplicate.swiper-slide-duplicate-active')
        # el2 = headless_chrome.find_element(By.CSS_SELECTOR, '.btn.btn-default.btn-lg')
        print("Item found")
    except NoSuchElementException:

        print("Item not found")


def test_add_to_cart_and_remove(browser, root_url):
    browser.get(root_url)
    browser.maximize_window()

    card_title = browser.find_element(By.LINK_TEXT, 'MacBook').text

    product_group = browser.find_element(By.XPATH, '''//button[@onclick="cart.add('43');"]''')
    product_group.click()

    browser.find_element(By.LINK_TEXT, 'Shopping Cart').click()

    added_item_title = browser.find_element(By.LINK_TEXT, 'MacBook').text
    assert card_title == added_item_title

    WebDriverWait(browser, timeout=3).until(EC.visibility_of_element_located((By.XPATH, '//button[@data-original-title = \'Remove\']')))
    browser.find_element(By.XPATH, '//button[@data-original-title = \'Remove\']').click()
    WebDriverWait(browser, timeout=3).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Continue')))
    message = browser.find_element(By.XPATH, '//div[@id=\'content\']/p').text
    assert message == 'Your shopping cart is empty!'


def test_titles_are_correct(browser, root_url):
    browser.get(root_url)
    browser.maximize_window()

    main_title = browser.find_element(By.CLASS_NAME, 'col-sm-4')
    assert main_title.text == 'Your Store'

    purchase_link = browser.find_element(By.ID, 'logo')
    purchase_link.click()


def test_locators(browser, root_url):
    browser.get(root_url)
    browser.maximize_window()

    try:
        empty_cart = browser.find_element(By.CLASS_NAME, 'text-center')
        print("Item found")

    except NoSuchElementException:
        print("Item not found")



    # ADD_TO_CART = browser.find_element(By.ID, 'button-cart')
    # ADD_TO_CART.click()
    # CART = browser.find_element(By.CLASS_NAME, 'hidden-xs.hidden-sm.hidden-md')
    # CART.click()
    # time.sleep(3)
    # page_catalog = browser.find_element(By.LINK_TEXT, 'Laptops & Notebooks')
    # action_chains = ActionChains(browser)
    # action_chains.move_to_element(page_catalog)
    # action_chains.perform()
    #
    # catalog_laptops_and_notebooks = browser.find_element(By.LINK_TEXT, 'Show All Laptops & Notebooks')
    # catalog_laptops_and_notebooks.click()
    #
    # WebDriverWait(browser, timeout=3).until(
    #     EC.visibility_of_element_located((By.TAG_NAME, 'h4')))
    # browser.find_element(By.TAG_NAME, 'h4').click()

    # card_title = browser.find_element(By.TAG_NAME, 'h4')
    # card_title.click()


    # main_title = browser.find_element(By.CLASS_NAME, 'col-sm-4')
    # assert main_title.text == 'Your Store'
    #
    # purchase_link = browser.find_element(By.ID, 'logo')
    # purchase_link.click()


# def test_add_to_cart_and_remove(browser, root_url):
#     browser.get(root_url)
#     browser.maximize_window()
#     card_title = browser.find_element(By.LINK_TEXT, 'MacBook').text
#     # button_group = browser.find_element(By.XPATH, "//*[text()='Add to Cart']")
#     content = browser.find_element(By.ID, 'content')
#     row = content.find_element(By.CLASS_NAME, 'row')
#     product_group = row.find_element(By.CSS_SELECTOR, ".product-layout.col-lg-3.col-md-3.col-sm-6.col-xs-12")
#     button_group = product_group.find_elements(By.TAG_NAME, 'button')
#     for button in button_group:
#         if button.find_element(By.XPATH, "//*[text()='Add to Cart']") is not None:
#             needed_button = button
#             break
#     needed_button.click()

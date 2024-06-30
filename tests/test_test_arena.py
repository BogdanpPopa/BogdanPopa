import time

import pytest
import random
import string

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from fixtures.chrome import chrome_browser
from pages.login_page import LoginPage

administrator_email = 'administrator@testarena.pl'
project_name_insert = 'Selenium_Bogdan_1'
project_prefix_insert = 'Bogdan'


@pytest.fixture
def browser(chrome_browser):
    chrome_browser.set_window_size(1080, 1920)
    chrome_browser.get('http://demo.testarena.pl/zaloguj')
    login_page = LoginPage(chrome_browser)
    login_page.attempt_login('administrator@testarena.pl', 'sumXQQ72$L')

    yield chrome_browser


def test_successful_login(browser):
    user_email = browser.find_element(By.CSS_SELECTOR, ".user-info small")
    assert administrator_email == user_email.text


def test_add_project(browser):
    project_name_insert_name = generate_random_string_project(10)
    project_prefix_insert_name = generate_random_string_prefix(5)
    admin_panel = browser.find_element(By.CSS_SELECTOR, ".icon_tools.icon-20").click()
    selector_add_project = "a.button_link[href='http://demo.testarena.pl/administration/add_project']"
    add_project = browser.find_element(By.CSS_SELECTOR, selector_add_project).click()
    project_name = (By.CSS_SELECTOR, "input[name='name']#name")
    browser.find_element(*project_name).send_keys(project_name_insert_name)
    project_prefix = (By.CSS_SELECTOR, "input[name='prefix']#prefix")
    browser.find_element(*project_prefix).send_keys(project_prefix_insert_name)
    project_description = (By.CSS_SELECTOR, "textarea[name='description']#description")
    browser.find_element(*project_description).send_keys(project_name_insert_name)
    cancel_button = (By.CSS_SELECTOR, "span.j_cancel_button > a")
    browser.find_element(*cancel_button).is_displayed()
    button_save = (By.CSS_SELECTOR, "input[name='save']#save")
    browser.find_element(*button_save).click()
    project_list = "a.button_link[href='http://demo.testarena.pl/administration/add_project']"
    time.sleep(2)
    browser.find_element(By.CSS_SELECTOR, ".activeMenu").click()
    time.sleep(2)
    browser.find_element(By.CSS_SELECTOR, "#search").send_keys(project_name_insert_name)
    browser.find_element(By.CSS_SELECTOR, "#search").send_keys(Keys.RETURN)
    time.sleep(5)
    first_cell = browser.find_element(By.CSS_SELECTOR, "table tbody tr:first-child td:first-child a")
    founded_project = first_cell.text

    assert founded_project == project_name_insert_name, f"Expected '{project_name_insert_name}', founded '{founded_project}'"
    time.sleep(5)


def test_add_message(browser):
    browser.find_element(By.CLASS_NAME, 'icon_mail').click()
    wait = WebDriverWait(browser, 10)
    text_input = (By.ID, 'j_msgContent')
    wait.until(EC.element_to_be_clickable(text_input))
    my_text = generate_random_string_project(10)
    browser.find_element(*text_input).send_keys(my_text)
    browser.find_element(By.ID, 'j_msgResponse-193').click()
    wait.until(lambda x: browser.find_elements(By.CLASS_NAME, 'message_content_text')[-1].text == my_text)
    assert browser.find_elements(By.CLASS_NAME, 'message_content_text')[-1].text == my_text


def generate_random_string_project(length=10):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def generate_random_string_prefix(length=5):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

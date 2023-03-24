import pytest
import requests
import os
from os.path import abspath, dirname, join

from selene import browser, be, have
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

XLSX_DOWNLOAD_LINK = 'https://freetestdata.com/document-files/xlsx/'  # [role="button" ][href*="100KB_XLSX"]
PDF_DOWNLOAD_LINK = 'https://laserscom.com/ru/products'  # [role="button"][href*="100KB_PDF"]
CSV_DOWNLOAD_LINK = 'https://freetestdata.com/wp-content/uploads/2021/09/Free_Test_Data_200KB_CSV-1.csv'  # [role="button" ][href*="200KB_CSV"]

BASE_DIR = dirname(dirname(abspath(__file__)))  # path to project root directory
RESOURCES_DIR = join(BASE_DIR, 'resources')  # path to save files

CSV_TEST_FILE_NAME = 'csv_test_file.csv'
# XLSX_TEST_FILE_NAME = 'xlsx_test_file.xlsx'
# PDF_TEST_FILE_NAME = 'pdf_test_file.pdf'


@pytest.fixture(scope='function', autouse=True)
def create_resources_for_tests():
    if not os.path.exists(RESOURCES_DIR):
        os.makedirs(RESOURCES_DIR)

    # setup selene browser for files download
    options = webdriver.ChromeOptions()  # создаем объект options на базе вэбдрайвера Selenium

    # dictionary that specify various preferences for the webdriver.
    prefs = {
        "download.default_directory": RESOURCES_DIR,
        "plugins.always_open_pdf_externally": True,
        "download.prompt_for_download": False
    }
    options.add_experimental_option("prefs", prefs)  # передаем в options значения из словаря prefs

    # create a new Chrome webdriver instance with specific options and a service object.
    # the resulting driver object can be used to control and automate the Chrome browser
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    browser.config.driver = driver  # настраиваем браузер selene на использование созданного драйвера
    browser.config.hold_browser_open = True

    response = requests.get(CSV_DOWNLOAD_LINK, allow_redirects=True)
    csv_file_path = join(RESOURCES_DIR, 'csv_test_file.csv')
    with open(csv_file_path, 'wb') as csv_test_file:
        csv_test_file.write(response.content)

    # browser.open(PDF_DOWNLOAD_LINK)
    # browser.element('[role=button][href*="100KB_PDF"]').should(be.clickable).click()

    browser.open(XLSX_DOWNLOAD_LINK)
    browser.element('[role="button" ][href*="100KB_XLSX"]').should(be.clickable).click()

    browser.open(PDF_DOWNLOAD_LINK)
    browser.all('.views-field-title .field-content a').element_by(have.exact_text('LDS-505-FP-10'))\
        .should(be.clickable).click()

    yield
    # удалить все файлы и директорию resources


def test_check_files_in_zip_archive():
    # проверить что в папке есть нужные файлы

    # записать в переменные имена файлов

    # cоздать для них контрольные данные

    # запаковать файлы в архив

    # проверить файлы по сформированным критериям

    pass

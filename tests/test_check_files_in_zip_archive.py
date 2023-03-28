import csv

import openpyxl
import pytest
import requests
import os
from os.path import abspath, dirname, join

from selene import browser, be, have
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from openpyxl import load_workbook
from PyPDF2 import PdfReader



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

    browser.open(PDF_DOWNLOAD_LINK)
    browser.all('.views-field-title .field-content a').element_by(have.exact_text('LDS-505-FP-10')) \
         .should(be.clickable).click()


    # TODO иногда зависает после окрытия ссылки и не кликает по кнопке
    browser.open(XLSX_DOWNLOAD_LINK)
    browser.element('[role="button" ][href*="100KB_XLSX"]').should(be.clickable).click()

    response = requests.get(CSV_DOWNLOAD_LINK, allow_redirects=True)
    csv_file_path = join(RESOURCES_DIR, CSV_TEST_FILE_NAME)
    with open(csv_file_path, 'wb') as csv_test_file:
        csv_test_file.write(response.content)

    yield
    # TODO раскоментировать
    # browser.close()
    # browser.quit()





def test_check_files_in_zip_archive():
    # определить число скачанных файлов
    downloaded_files_list = [f for f in os.listdir(RESOURCES_DIR)]
    downloaded_files_number = len(downloaded_files_list)

    # записать в переменные имена файлов
    # TODO раскоментировать
    downloaded_pdf_file_name = "".join([f for f in downloaded_files_list if f.endswith('.pdf')])
    downloaded_xlsx_file_name = "".join([f for f in downloaded_files_list if f.endswith('.xlsx')])

    # определить размер файлов
    # TODO раскоментировать
    downloaded_pdf_file_size = os.path.getsize(join(RESOURCES_DIR, downloaded_pdf_file_name))
    downloaded_csv_file_size = os.path.getsize(join(RESOURCES_DIR, CSV_TEST_FILE_NAME))
    downloaded_xlsx_file_size = os.path.getsize(join(RESOURCES_DIR, downloaded_xlsx_file_name))

    # cоздать для загруженных файлов контрольные данные
    """
    Для XLSX:
    - список листов книги downloaded_xlsx_file_sheet_names
    - --- название первого листа downloaded_xlsx_file_first_sheet_name
    - количество столбцов в перовом листе downloaded_xlsx_file_first_sheet_max_col
    - количество строк в первом листе вownloaded_xlsx_file_first_sheet_max_row
    - содержимое первой строки первой строки downloaded_xlsx_file_first_sheet_first_row_value
    - содержимое последнего столбца downloaded_xlsx_file_first_sheet_last_column_value
    """
    downloaded_xlsx_file = openpyxl.load_workbook(join(RESOURCES_DIR, downloaded_xlsx_file_name))
    downloaded_xlsx_file_first_sheet = downloaded_xlsx_file.worksheets[0]

    downloaded_xlsx_file_sheet_names = downloaded_xlsx_file.sheetnames
    downloaded_xlsx_file_first_sheet_max_col = downloaded_xlsx_file_first_sheet.max_column
    downloaded_xlsx_file_first_sheet_max_row = downloaded_xlsx_file_first_sheet.max_row
    downloaded_xlsx_file_first_sheet_b2_sell = downloaded_xlsx_file_first_sheet.cell(row = 2, column = 2).value

    # TODO remove
    # downloaded_xlsx_file_first_sheet_last_sell = downloaded_xlsx_file_first_sheet\
    #     .cell(row = downloaded_xlsx_file_first_sheet_max_row, column = downloaded_xlsx_file_first_sheet_max_col).value

    def get_xlsx_row_values(path, row):
        wb = openpyxl.load_workbook(path)
        first_sheet = wb.worksheets[0]
        row_values = [first_sheet.cell(row=row, column=col).value for col in range(1, first_sheet.max_column + 1)]
        return row_values

    downloaded_xlsx_file_first_sheet_first_row_value = get_xlsx_row_values(join(RESOURCES_DIR, downloaded_xlsx_file_name), 1)

    def get_xlsx_column_values(path, column):
        wb = openpyxl.load_workbook(path)
        first_sheet = wb.worksheets[0]
        column_values = [first_sheet.cell(column=column, row=r).value for r in
                         range(1, first_sheet.max_row + 1)]
        return column_values

    downloaded_xlsx_file_first_sheet_last_column_value = get_xlsx_column_values\
        (join(RESOURCES_DIR, downloaded_xlsx_file_name), downloaded_xlsx_file_first_sheet_max_col)

    # get control data from pdf file
    dowloaded_pdf_file_path = join(RESOURCES_DIR, downloaded_pdf_file_name)
    with open(dowloaded_pdf_file_path, 'rb') as pdf_file:
        pdf_file_reader = PdfReader(pdf_file)
        downloaded_pdf_file_number_pages = len(pdf_file_reader.pages)
        downloaded_pdf_file_first_page_text = pdf_file_reader.pages[0].extract_text()
        downloaded_pdf_file_last_page_text = pdf_file_reader.pages[downloaded_pdf_file_number_pages - 1].extract_text()
        downloaded_pdf_file_meta_title = pdf_file_reader.metadata.title

    # get control data from csv file
    downloaded_csv_file_path = join(RESOURCES_DIR,  CSV_TEST_FILE_NAME)
    def get_csv_row_value(csv_file_path, row_num):
        with open(downloaded_csv_file_path, 'rt') as csv_file:
            csv_file_reader = csv.reader(csv_file)
            for i, row in enumerate(csv_file_reader):
                if i == row_num - 1:
                    row_value = row
        return row_value
    downloaded_csv_file_row_3_value = get_csv_row_value(downloaded_csv_file_path, 2)
    print(downloaded_csv_file_row_3_value)






    # TODO downloaded_xlsx_file_name ==
    assert downloaded_xlsx_file_sheet_names == ['Sheet1']
    assert downloaded_xlsx_file_first_sheet_max_col == 6
    assert downloaded_xlsx_file_first_sheet_max_row == 3083
    assert downloaded_xlsx_file_first_sheet_first_row_value == ['SR.', 'NAME', 'GENDER', 'AGE', 'DATE ', 'COUNTRY']
    # TODO downloaded_xlsx_file_first_sheet_last_column_value ==











    # запаковать файлы в архив

    # проверить файлы по сформированным критериям

    # удалить все файлы и директорию resources


    # os.remove(join(RESOURCES_DIR, CSV_TEST_FILE_NAME))
    # os.remove(join(RESOURCES_DIR, downloaded_pdf_file_name))
    # os.remove(join(RESOURCES_DIR, downloaded_xlsx_file_name))
    # os.rmdir(RESOURCES_DIR)

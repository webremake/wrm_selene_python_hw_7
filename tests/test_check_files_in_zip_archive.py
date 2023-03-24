import pytest
import requests
import os
from os.path import abspath, dirname, join

'''
надо сделать одну фикстуру
prepare
'''

XLSX_DOWNLOAD_LINK = 'https://freetestdata.com/document-files/xlsx/'  # [role="button" ][href*="100KB_XLSX"]
PDF_DOWNLOAD_LINK = 'https://freetestdata.com/document-files/pdf/'  # [role="button" ][href*="100KB_PDF"]
CSV_DOWNLOAD_LINK = 'https://freetestdata.com/wp-content/uploads/2021/09/Free_Test_Data_200KB_CSV-1.csv'  # [role="button" ][href*="200KB_CSV"]

BASE_DIR = dirname(dirname(abspath(__file__)))  # path to project root directory
RESOURCES_DIR = join(BASE_DIR, 'resources')
if not os.path.exists(RESOURCES_DIR):
    os.makedirs(RESOURCES_DIR)

# define directory `resources` to save test files
# resources = os.path.join(os.path.dirname(__file__), "..", "resources")  # define directory to save test files

# os.path.dirname(__file__)  # директория текущего файла
# print(os.path.dirname(__file__))  # директория текущего файла

response = requests.get(CSV_DOWNLOAD_LINK, allow_redirects=True)

csv_file_path = join(RESOURCES_DIR, 'csv_test_file.csv')
with open(csv_file_path, 'wb') as csv_test_file:
    csv_test_file.write(response.content)



@pytest.fixture(scope='function', autouse=True)
def setup_browser_for_files_download():
    pass

@pytest.fixture(scope='function', autouse=True)
def prepare_files_and_check_data_for_test():

    yield
    # удалить все файлы и директорию resources
    pass



def test_check_files_in_zip_archive():
    # проверить что в папке есть нужные файлы

    # запаковать файлы в архив

    # проверить файлы по сформированным критериям

    pass

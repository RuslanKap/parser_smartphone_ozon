import time
from pathlib import Path
import csv
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException



PATH = Path(__file__).resolve().parent
PAGES = ['https://www.ozon.ru/category/smartfony-15502/?sorting=rating',
         'https://www.ozon.ru/category/smartfony-15502/?page=2',
         'https://www.ozon.ru/category/smartfony-15502/?page=2',
         ]

logging.basicConfig(level=logging.INFO, format= "%(asctime)s - [%(levelname)s] - %(message)s")



def session():
    """
    New sessions for all parsing iterations
    :return: new driver session
    To hide browser window - options.add_argument("--headless")
    """
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 "
        "Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless")
    driver = webdriver.Chrome(
        executable_path=r"PATH+'chromedriver.exe'",
        options=options)
    return driver


def get_link_data(page: str) -> None:
    """
    :param page: pages from PAGES, category - smartphones, rate sorting
    :return: product_links.txt with links
    """
    driver = session()
    driver.get(page)
    time.sleep(2)
    card = driver.find_elements(By.CLASS_NAME, 'kr5')
    links = []
    for i, lin in enumerate(card):
        link = lin.find_element(By.CLASS_NAME, 'k8n').get_attribute('href')
        links.append(link)
        time.sleep(0)
        logging.info(f'{i + 1} - add link')
    driver.close()
    with open('product_links.txt', 'a', encoding='utf-8') as f:
        for link in links:
            f.write(link + '\n')


def parse_links(link: str) -> list[str]:
    """
    Get data(name, os, os_version) for the all items in product_links.txt
    :param link: product_links.txt
    :return: name, os, os_version
    """
    driver = session()
    driver.get(link)
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2)")
    time.sleep(3)
    name_product = driver.find_element(
        By.XPATH,
        "//div[@data-widget='webProductHeading']//h1").text
    try:
        os_type = driver.find_element(
            By.XPATH,
            "//span[text()='Операционная система']//parent::dt//following-sibling::dd//a").text
    except NoSuchElementException:
        os_type = 'No Data'
    if name_product.count('Apple'):
        try:
            os_version = driver.find_element(
                By.XPATH,
                "//span[text()='Версия iOS']//parent::dt//following-sibling::dd//a").text
        except NoSuchElementException:
            try:
                os_version = driver.find_element(
                    By.XPATH,
                    "//span[text() = 'Версия iOS']//parent::dt//following-sibling::dd").text
            except NoSuchElementException:
                os_version = 'No Data'
    else:
        try:
            os_version = driver.find_element(
                By.XPATH,
                "//span[text()='Версия Android']//parent::dt//following-sibling::dd").text
        except NoSuchElementException:
            os_version = 'No Data'

    logging.info(f'name: {name_product}, os: {os_type}, os_ver: {os_version}')
    time.sleep(2)
    driver.close()
    return [name_product, os_type, os_version]


def main():
    for item in PAGES:
        get_link_data(item)
    with open('product_links.txt', 'r', encoding='utf-8') as f:
        for i, line in enumerate(f.readlines()):
            logging.info(f'№ {i + 1} запись обрабатывается, => {line}')
            data = parse_links(line)
            with open('data.csv', 'a', encoding='utf-8', newline='') as d:
                writer = csv.writer(d)
                writer.writerow(data)


if __name__ == '__main__':
    main()

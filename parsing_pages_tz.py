from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv


def get_source_html(url):
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        time.sleep(1)
        driver.switch_to
        driver.find_element(By.XPATH, '//*[@id="current-town-view-modal"]/div/div/div/button/span/i').click()
        try:
            cards = driver.find_elements(By.CLASS_NAME, 'product__brief')
            for i in range(len(cards)):
                y = i + 1
                try:
                    link = driver.find_element(By.XPATH, f'//*[@id="products-content"]/div[1]/div[{y}]/div/div[4]/a')
                except:
                    link = driver.find_element(By.XPATH, f'//*[@id="products-content"]/div[1]/div[{y}]/div/div[5]/a')
                link1 = link.get_attribute('href')
                print(y)
                print(link1)  

                with open('links.csv', 'a', encoding="utf-8", newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(
                            [link1]
                        )
        except Exception as _ex:
            print(_ex)    

    except Exception as _ex:
        print(_ex)
    finally:
        print('vse good')


def main():
    for i in range(1):
            get_source_html(
        url=f'https://chudodey.com/catalog/makiyazh/brovi/kraska-i-tinty')
if __name__ == '__main__':
    main()
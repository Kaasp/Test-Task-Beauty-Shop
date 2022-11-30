from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv


def get_source_html(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)
    lion = 1
    try:
        driver.find_element(By.XPATH, '//*[@id="current-town-view-modal"]/div/div/div/button/span/i').click()
        print('clicked')
        time.sleep(2)
        try:
            print('Starting')
            variants = driver.find_elements(By.XPATH, '//*[@id="product-block"]/div[2]/div[2]/div[3]/div/div[2]/div/span')
            if len(variants) == 0:
                raise Exception
            for i in range(len(variants)):
                driver.find_element(By.XPATH, f'//*[@id="product-block"]/div[2]/div[2]/div[3]/div/div[2]/div/span[{i+1}]/span').click()
                time.sleep(5)
                add_to_csv(driver, lion)
                
        except Exception as e:
            print(str(e))
            print('No additional items. Starting to scrap')
            lion = 2
            add_to_csv(driver, lion)
                
    except Exception as e:
        print(str(e))
        print('Unable to locate element: town-view-modal')
        
def add_to_csv(driver, lion):
    #Name
    try:
        name = driver.find_element(By.CLASS_NAME, 'product-detail__header').text
    except:
        print('Something goes wrong. Code: NAME')

    #Detais
    try:
        details_list = []
        details2_list = []
        details1 = driver.find_elements(By.XPATH, '//*[@id="product-block"]/div[2]/div[2]/div[1]/div/div[1]/dl/dt')
        details2 = driver.find_elements(By.XPATH, '//*[@id="product-block"]/div[2]/div[2]/div[1]/div/div[1]/dl/dd')
        for e in details1:
            details_list.append(e.text)
        for e in details2:
            details2_list.append(e.text)
        details_dictionary = dict(zip(details_list, details2_list))
    except:
        print('Something goes wrong. Code: DETAILS')

    #Article
    try:
        article = driver.find_element(By.XPATH, '//*[@id="product-block"]/div[2]/div[2]/div[2]').text
    except Exception:
        print('Something goes wrong. Code: ARTICLE')

    #Path
    try:
        full_path = []
        path1 = ''
        path = driver.find_elements(By.CSS_SELECTOR, '.breadcrumb')
        for e in path:
            full_path.append(e.text)
        full_path = full_path[0].split('\n')
        if len(full_path) >= 5:
            full_path.pop()
        path1 = '-'.join(str(i) for i in full_path)

    except Exception:
        print('Something goes wrong. Code: PATH')

    #Price
    try:
        current_price = driver.find_element(By.CLASS_NAME, 'product-detail__price').text
        try:
            old_price = driver.find_element(By.CLASS_NAME, 'old-price').text
        except Exception:
            old_price = '-'
    except Exception:
        print('Something goes wrong. Code: PRICE')

    #Photo
    try:
        photo_links = []
        if lion == 1:                 
            photos = driver.find_elements(By.XPATH, '//*[@id="product-block"]/div[2]/div[1]/div/div/button')
            for i in range(len(photos)):                  
                photo1 = driver.find_element(By.XPATH, f'//*[@id="product-block"]/div[2]/div[1]/div/div/button[{i+1}]/img').get_attribute('src')
                photo_links.append(photo1)
        elif lion == 2:
            photos = driver.find_elements(By.XPATH, '//*[@id="product-block"]/div[2]/div[1]/div/div/div[4]/div/div/button')
            for i in range(len(photos)):
               photo1 = driver.find_element(By.XPATH, f'//*[@id="product-block"]/div[2]/div[1]/div/div/div[4]/div/div/button[{i+1}]/img').get_attribute('src')
               photo_links.append(photo1) 
    except:
        print('Something goes wrong. Code: LINK')

    #Запись
    with open('test.csv', 'a', encoding="utf-8", newline='') as file:
                    writer = csv.writer(file, delimiter='\t')
                    writer.writerow(
                        [path1, name, details_dictionary, article, photo_links, current_price, old_price]
                    )
    print('VSE OK')


def main():
    f = open('links.csv', 'r', encoding='utf-8')
    for line in f:
            get_source_html(
        url=line)
if __name__ == '__main__':
    main()
    
    

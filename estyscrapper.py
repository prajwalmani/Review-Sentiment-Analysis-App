# Author :Prajwal Mani

from csv import writer
import re
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from bs4 import BeautifulSoup as bs 
import os 


browser=webdriver.Chrome(ChromeDriverManager().install())
def scrap():
    # Here i am just scrapping first 10 pages 
    for page in range(1,11):
        os.system("cls")
        print("we are in page {}".format(page))
        url='https://www.etsy.com/in-en/c/jewelry-and-accessories?ref=pagination&page={}'.format(page)
        browser.get(url)
        sleep(5)
        for productscount in range(1,60):
            nproduct=browser.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[3]/div[2]/div[2]/div[2]/div/div/ul/li[{0}]/div/a/div[1]/div/div/div/div/div/img'.format(productscount))
            nproduct.click()
            sleep(5)
            windows = browser.window_handles
            for handle in windows[1:]:
                browser.switch_to.window(handle)
                html_source=browser.page_source
                bssoup=bs(html_source,'html.parser')
                bssoup.encode("utf-8")
                reviews=bssoup.find_all('p',id=re.compile('^review-preview-toggle-\d+'))
                for rev in reviews:
                    text=[]
                    text.append(rev.getText())
                    with open('estyreviews.csv', 'a') as f:
                        writer_object = writer(f) 
                        try:
                            writer_object.writerow(text) 
                        except UnicodeEncodeError:
                            pass
                        f.close()
                sleep(5)
                browser.close()
                browser.switch_to.window(windows[0])
            sleep(5)

scrap()


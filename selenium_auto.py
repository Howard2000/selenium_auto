# coding: utf-8
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}

host = 'https://rom1504.github.io/clip-retrieval/'
url = 'https://rom1504.github.io/clip-retrieval/?back=https%3A%2F%2Fknn.laion.ai&index=laion5B-H-14&useMclip=false&query=gold+bracelet'

js1 = 'return document.querySelector("body > clip-front").shadowRoot.mode'
js2 = 'return document.querySelector("body > clip-front").shadowRoot.querySelector("#products").childElementCount'
js3 = 'document.querySelector("body > clip-front").shadowRoot.querySelector("#searchBar")'

def open_chrome_driver():
 
    driver = webdriver.Chrome()
 
    return driver

def open_url(driver,url):
 
    driver.get(url)

def wait_by_sec(s):
    
    time.sleep(s)

def check_img_num():

    js = 'return document.querySelector("body > clip-front").shadowRoot.querySelector("#products").childElementCount'
    n = driver.execute_script(js)
    return n

def scroll_down():

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(0.5)

def load_img(n):

    loaded = check_img_num()
    while loaded < n:
        scroll_down()
        loaded = check_img_num()

def save_img_to(path):

    f_caption = open(path+"/dataset/caption.txt",'w')
    n = check_img_num()
    for num in range(n):
        js4 = 'return document.querySelector("body > clip-front").shadowRoot.querySelector("#products > figure:nth-child('+str(num+1)+') > img.pic")'
        src = None
        caption = None
        ext = None
        try:
            pic = driver.execute_script(js4)
            src = pic.get_attribute("src")
            caption = pic.get_attribute("title")

            # title = caption.replace(' ', '_')
            ext = src.split('.')[-1]
            # filename = title+'.'+ext
        except Exception as e:
            print("Exception occured "+str(e))
            continue

        try: 
            img = requests.get(src,headers=header,timeout=5)
            f = open(path+"/dataset/"+str(num+1)+'.'+ext,'wb') 
            f.write(img.content)
            f.close()
            f_caption.write(str(num+1)+'.'+caption+'\n')
            print(img)
            print(caption)
        except Exception as e:
            print("Exception occured "+str(e))
        
    f_caption.close()

if __name__ == "__main__":

    path = os.getcwd()

    driver = open_chrome_driver()

    open_url(driver, url)

    wait_by_sec(10)

    number = int(input("number of images: "))

    load_img(number)

    save_img_to(path)


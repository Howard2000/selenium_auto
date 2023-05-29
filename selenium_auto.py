# coding: utf-8
import os
import time
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

def get_img_info(driver):
    n = check_img_num()
    list = []
    for num in range(n):
        js4 = 'return document.querySelector("body > clip-front").shadowRoot.querySelector("#products > figure:nth-child('+str(num+1)+') > img.pic")'
        src = None
        caption = None
        ext = None
        try:
            pic = driver.execute_script(js4)
            src = pic.get_attribute("src")
            caption = pic.get_attribute("title")
            temp = [caption, src]
            list.append(temp)
        except Exception as e:
            print("Exception occured "+str(e))
    return list

def check_img_size(img,size):
    img_size = img.size
    if (img_size[0]<size or img_size[1]<size):
        return False
    else:
        return True

def save_img_to(path,list):
    num=0
    
    # n = check_img_num()
    for img_info in list:
        
        src = img_info[1]
        caption = img_info[0]
        
        try: 
            response = requests.get(src,headers=header,timeout=5,stream=True)
            response.raw.decode_content = True
            img = Image.open(response.raw)
            
            ext = img.format
            if(check_img_size(img,512)):
                num+=1
            else:
                continue
            img.save(path+"/dataset/"+str(num)+'.'+ext)

            f = open(path+"/dataset/"+str(num)+".txt",'w')
            f.write(caption+'\n')
            f.close()
            
            print(caption)
        except Exception as e:
            print("Exception occured "+str(e))
        
    

def search_for_keywards(driver,key):
    js = 'return document.querySelector("body > clip-front").shadowRoot.querySelector("#searchBar")'
    search_bar = driver.execute_script(js)
    search_bar.send_keys(key)
    search_bar.send_keys(Keys.ENTER)

def set_search_filter():
    #set Aesthetic score to 9
    js = 'return document.querySelector("body > clip-front").shadowRoot.querySelector("#filter > label:nth-child(26) > select > option:nth-child(11)")'
    score_9 = driver.execute_script(js)
    score_9.click()

if __name__ == "__main__":

    path = os.getcwd()
    if not os.path.exists(path+"/dataset/"):
        os.makedirs(path+"/dataset/")

    driver = open_chrome_driver()

    open_url(driver, host)

    wait_by_sec(3)

    key_words = input("Enter key words: ")
    number = int(input("Enter search range: "))

    set_search_filter()
    search_for_keywards(driver, key_words)

    wait_by_sec(5)
    load_img(number)

    img_list = get_img_info(driver)

    # for it in img_list:
    #     print(it)
    
    save_img_to(path,img_list)


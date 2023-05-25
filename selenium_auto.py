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

path = os.getcwd()
print(path)
driver = webdriver.Chrome()
host = 'https://rom1504.github.io/clip-retrieval/'
url = 'https://rom1504.github.io/clip-retrieval/?back=https%3A%2F%2Fknn.laion.ai&index=laion5B-H-14&useMclip=false&query=gold+bracelet'
driver.get(url)
js1 = 'return document.querySelector("body > clip-front").shadowRoot.mode'
js2 = 'return document.querySelector("body > clip-front").shadowRoot.querySelector("#products").childElementCount'
js3 = 'document.querySelector("body > clip-front").shadowRoot.querySelector("#searchBar")'
shadow = driver.execute_script(js1)

print(shadow)

time.sleep(10)

n = driver.execute_script(js2)

while n < 300:
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(0.5)
    n = driver.execute_script(js2)

print(n)
time.sleep(3)
f_caption = open(path+"/dataset/caption.txt",'w')
for num in range(n):
    js4 = 'return document.querySelector("body > clip-front").shadowRoot.querySelector("#products > figure:nth-child('+str(num+1)+') > img.pic")'
    pic = driver.execute_script(js4)

    src = pic.get_attribute("src")
    caption = pic.get_attribute("title")

    # title = caption.replace(' ', '_')
    ext = src.split('.')[-1]
    # filename = title+'.'+ext

    try: 
        img = requests.get(src,headers=header)
        f = open(path+"/dataset/"+str(num+1)+'.'+ext,'wb') 
        f.write(img.content)
        f.close()
        f_caption.write(str(num+1)+'.'+caption+'\n')
        print(img)
        print(caption)
    except Exception as e:
        print("Exception occured"+e)
        
f_caption.close() 
# if __name__ == "__main__":


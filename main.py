# -*- coding: utf-8 -*-

from selenium import webdriver
from urllib.request import urlopen
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import urllib.request as dw
import os
from selenium.webdriver.common.by import By
import ssl
from requests import get
import pyautogui
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import keyboard
import glob

def img_download(imgUrl, file_name):

    response = get(imgUrl, stream=True)               # get request
    with open(file_name, "wb") as file:   # open in binary mode
        # file.write(response.content)      # write to file
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
        



def google_scroll(SCROLL_PAUSE_TIME,search):
    # search keyword
    elem = driver.find_element(By.NAME, "q")
    elem.send_keys(search)
    elem.send_keys(Keys.RETURN)

    # change image size is big
    try:
        pass
        time.sleep(3)
        driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[2]/c-wiz/div[1]/div/div[1]/div[2]/div[2]/div').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[2]/c-wiz/div[2]/div[2]/c-wiz[1]/div/div/div[1]/div/div[1]/div').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[2]/c-wiz/div[2]/div[2]/c-wiz[1]/div/div/div[3]/div/a[2]/div').click()
        time.sleep(2)
    except Exception as e:
        print(e)


    SCROLL_PAUSE_TIME = SCROLL_PAUSE_TIME

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            try:    
                driver.find_element(By.XPATH, '//*[@id="islmp"]/div/div/div/div/div[1]/div[2]/div[2]/input').click()
            except:
                break
        last_height = new_height

def url_retrieve(copied_xpath, total_image_count):
    images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
    print(f'{"*"*50}Crawlling started.{"*"*50}')
    count = 1
    con_count = 0
    TIME_LIMIT = 5
    for image in images:
        try:
            try:
                image.click()
            except:
                try:
                    driver.execute_script("arguments[0].click();", image)
                except Exception as e:
                    print(e)
                    continue

            file_name = f"{search}_{count}"
            if os.path.isfile(".\downloads\\" + file_name + ".jpg"):
                print(count, con_count + total_image_count)
                con_count += 1
                count += 1
                continue
            target_img = driver.find_element(By.XPATH,copied_xpath)
            # imgUrl = target_img.get_attribute('src')

            actions.move_to_element(target_img)
            actions.context_click().perform()

            # google image file download
            pyautogui.press('v')
            time.sleep(1.5)
            keyboard.write(file_name)
            time.sleep(1.5)
            pyautogui.press('enter')
            time.sleep(1.5)

            # 윈도우 기본 다운로드 폴더의 경로
            download_directory = os.path.expanduser('~/Downloads')

            # 파일 이름에 "a"가 포함된 파일을 찾기
            pattern = os.path.join(download_directory, f"{file_name}.*")  # 다운로드 폴더 내에서 "a"를 포함하는 파일 찾기

            # 파일 목록 얻기
            files = glob.glob(pattern)

            # 찾은 파일 출력
            for file in files:
                dst = r".\downloads\\" + file_name + ".jpg"
                os.replace(file, dst)

            print(f"Image saved: {search}_{count}.jpg")
            # we can not use enumerate function. because there are passed case.
            if (count == total_image_count + con_count):
                break
            else:
                count+=1
        except Exception as e:
            print(e)
            pass
    print(f'{"*"*50}Crawlling Completed.{"*"*50}')

if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context

    # save_dir
    if not os.path.exists('./downloads') :
        os.mkdir('./downloads')

    """
    ex )
    search_list = [
        ["keyword", num_of_downloads]
    ]
    """
    search_list = [["아디다스", 8000]]



    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument("--disable-proxy-certificate-handler")
    
    options.add_experimental_option('prefs', {
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
    'safebrowsing.enabled': True
    })  

    for search, total_image_count in search_list:
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")
        actions = ActionChains(driver)

        # 가끔씩 xpath가 바뀌는 경우가 있음 (구글에서 이미지 클릭했을 때 생기는 왼쪽 큰 이미지 xpath)
        copied_xpath='//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]'

        google_scroll(SCROLL_PAUSE_TIME=1, search=search)
        

        url_retrieve(copied_xpath=copied_xpath, total_image_count=total_image_count)
        driver.close()

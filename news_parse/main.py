# -*- coding: utf8 -*-
import datetime
import os
import pickle
import random
import sqlite3
import time

import pymysql
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

from config import login, password, PROXY

useragent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={useragent.chrome}")

proxies = {'https': f'http://{login}:{password}@{random.choice(PROXY)}'}

categories = ['personal_feed', 'koronavirus', 'politics', 'society', 'business', 'world', 'incident', 'culture',
              'computers', 'science', 'auto']
amount = 20  # int(input("Кол-во новостей: "))
ChromeDriver = "my_chromedriver"
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, ChromeDriver)
options.add_argument("--headless")
with webdriver.Chrome(executable_path=DRIVER_BIN, options=options, seleniumwire_options=proxies) as driver:
    driver.get(f"https://passport.yandex.ru/auth/welcome")
    for cookie in pickle.load(open(f"yandex_cookies", "rb")):
        driver.add_cookie(cookie)
    time.sleep(1)
    for item in categories:
        driver.get(f"https://yandex.ru/news/rubric/{item}")
        try:
            while len(driver.find_elements(By.CLASS_NAME, "mg-grid__col")) < amount:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            soup = BeautifulSoup(driver.page_source, "lxml")
        except:
            time.sleep(60)
            while len(driver.find_elements(By.CLASS_NAME, "mg-grid__col")) < amount:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            soup = BeautifulSoup(driver.page_source, "lxml")
        for i in range(1, amount + 1):
            try:
                cat = f"{item}"
                name_state = soup.find_all(class_="mg-grid__col")[i].find(class_="mg-card__title").find("a").text
                source = soup.find_all(class_="mg-grid__col")[i].find(class_="mg-card-source__source").find("a").text
                time_post = f'{datetime.datetime.today().strftime("%Y.%m.%d")} {soup.find_all(class_="mg-grid__col")[i].find(class_="mg-card-source__time").text}'
                a = '"'
                try:
                    photo = soup.find_all(class_="mg-grid__col")[i].find(class_="mg-card-media__image").find("img").get(
                        "src")
                except:
                    photo = list(
                        soup.find_all(class_="mg-grid__col")[i].find(class_="mg-card__media-block_type_image").get(
                            "style").split("url(")[-1])
                    del photo[-1]
                    photo = ''.join(photo)
                # print(f'{soup.find_all(class_="mg-grid__col")[i].find(class_="mg-card__title").find("a").get("href")}')
                driver.get(
                    f'{soup.find_all(class_="mg-grid__col")[i].find(class_="mg-card__title").find("a").get("href")}')
                soup1 = BeautifulSoup(driver.page_source, "lxml")
                link = soup1.find(class_="mg-story__title-link").get("href")
                try:
                    desc = soup1.find_all("span", class_='mg-snippet__text')
                except:
                    desc = soup1.find("span", class_='mg-snippet__text')
                desc1 = []
                for d in range(len(desc)):
                    for j in range(len(desc[d].find_all('span'))):
                        desc1.append(desc[d].find_all('span')[j].text)
                # print(
                #     f"\n{cat}\n{name_state}\n{source} {time_post}\n{link}\n{photo.replace(f'{a}', '').replace(')', '')}\n{''.join(desc1)}\n----------------------------")
                con = pymysql.connect(host='localhost',
                                      port=3306,
                                      user='1detailing',
                                      password='Y9lCTqy7qTvDZ7O',
                                      database='1detailing',
                                      )
                cur = con.cursor()
                cur.execute(
                    f"INSERT INTO news_pars (cat, name_state, source, time_post, link, photo, desc)  VALUES ('{cat}', '{name_state}', '{source}', '{time_post}', '{link}', '{photo.replace(f'{a}', '').replace(')', '')}', '{''.join(desc1)}')")
                con.commit()
                con.close()
            except Exception as ex:
                pass
        time.sleep(40)
# Название таблицы news
# 1) cat
# 2) name_state
# 3) source
# 4) time_post
# 5) link
# 6) photo
# 7) desc

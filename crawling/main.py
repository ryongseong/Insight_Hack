import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from driver import get_chrome_driver
import random
import json
import re

from utils import get_source

class Crawler:
    def start(self, search_name):
        try:
            print("🚶‍ url 크롤링 시작 🚶‍")
            driver = get_chrome_driver()

            self.get_product_urls(driver, search_name)
            file_path = './sources/outputs/youtube_{}.json'.format(search_name)
            json_data = get_source(file_path)

            # print("🏃‍ url 크롤링 종료 🏃‍")

            print("-----------------------")

            print("🏃‍ data 크롤링 시작 🏃‍")

            self.get_product_data(driver, json_data, search_name)

            print("🏃‍ data 크롤링 종료 🏃‍")

            return True
        except Exception as e:
            print(e)
            return False

    def scroll_down(self, driver):
        for _ in range(100):
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            #시간대기
            time.sleep(1)

    def get_product_urls(self, driver, search_name):
        product_urls = []

        target_url = "https://www.youtube.com/results?search_query={}".format(search_name)

        driver.get(target_url)
        time.sleep(3)
        self.scroll_down(driver)
        time.sleep(3)

        productList = driver.find_element(By.ID, 'contents')
        productThumbnail = productList.find_elements(By.TAG_NAME, 'ytd-item-section-renderer')

        for i in productThumbnail:
            pp = i.find_element(By.ID, 'contents')
            time.sleep(1)
            ppp = pp.find_elements(By.TAG_NAME, 'ytd-playlist-renderer')
            time.sleep(1)
            for item in ppp:
                div_tag = item.find_element(By.ID, 'content')
                a_tag = div_tag.find_element(By.CLASS_NAME, 'yt-simple-endpoint')
                href = a_tag.get_attribute('href')
                print(href)
                time.sleep(1)
                thumbnail_tag = driver.find_element(By.CLASS_NAME, 'yt-core-image.yt-core-image--fill-parent-height.yt-core-image--fill-parent-width.yt-core-image--content-mode-scale-aspect-fill.yt-core-image--loaded')
                thumbnail = thumbnail_tag.get_attribute('src')
                if href not in product_urls:
                    product_urls.append([href, thumbnail])
        data = [{
            'urls' : product_urls
        }]

        with open('./sources/outputs/youtube_{}.json'.format(search_name), 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        time.sleep(3)

    def get_product_data(self, driver, json_data, search_name):
        """
            ELEMENTS
        """

        title = 'title'
        description = 'yt-core-attributed-string--link-inherit-color'
        channel_name = 'ytd-channel-name'
        더보기버튼 = '//*[@id="expand"]'

        for data in json_data:
            product_urls = data["urls"]

            products = []
            if product_urls:
                for index, url in enumerate(product_urls):
                    print(f"{index+1}/{len(product_urls)}, current_url : {url[0]}")

                    try:
                        driver.get(url[0])
                        WebDriverWait(driver, 10)
                        time.sleep(5)

                        below = driver.find_element(By.TAG_NAME, 'ytd-watch-metadata')

                        p_title_outer = below.find_element(By.ID, title)
                        p_title = p_title_outer.find_element(By.TAG_NAME, 'yt-formatted-string').text

                        p_channel_name_outer = driver.find_element(By.TAG_NAME, channel_name)
                        p_channel_name = p_channel_name_outer.find_element(By.CLASS_NAME, 'yt-formatted-string').text

                        try:
                            driver.find_element(By.XPATH, 더보기버튼).send_keys(Keys.ENTER)
                            time.sleep(0.5)
                            p_description = driver.find_element(By.CLASS_NAME, description).text
                        except:
                            p_description = ""

                        product = {
                            "title" : p_title,
                            "channel_name" : p_channel_name,
                            "description" : p_description,
                            "thumbnail" : url[1],
                            "source_url" : url[0],
                        }
                        products.append(product)

                    except Exception as e:
                        print(e)
                
        with open('./sources/outputs/youtube_result_{}.json'.format(search_name+datetime.now().strftime('%Y-%m-%d')), 'w', encoding='utf-8') as json_file:
            json.dump(products, json_file, ensure_ascii=False, indent=4, default=str)

if __name__ == '__main__':
    search_name = input("검색어 입력: ")
    crawler = Crawler()
    crawler.start(search_name)
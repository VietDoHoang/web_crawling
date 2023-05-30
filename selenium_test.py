import os
import requests
import time
import random

from tqdm import tqdm
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_option = webdriver.ChromeOptions()
chrome_option.add_argument("start-maximized")
chrome_option.add_argument("__headless")
chrome_option.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(
    'chromedriver',
    options=chrome_option
)
# url = 'https://www.python.org/'
# driver.get(url)
# text= driver.find_element(
#     By.XPATH, # kiểu search
#     '/html/body/div/header/div/div[3]/p'
# ).text
# print(type(text))
# print(text)
# print(driver.page_source)
# khởi tạo folder nếu nó chưa có
root_dir = './vn_news_corpus'
os.makedirs(root_dir,exist_ok=True)
# số lượng page mong muốn
n_page = 1
article_id =0

for page_idx in range(n_page):
    # access to table page thoi_su in vietnamnet.vn
    main_url = f'https://vietnamnet.vn/thoi-su-page{page_idx}'
    driver.get(main_url)
    
    # get list url of articles
    news_lst_xpath = '//div[@class="topStory-15nd"]/div/div[1]/a'
    news_tags = driver.find_elements(
        By.XPATH,
        news_lst_xpath
    )
    news_page_urls = [
        news_tag.get_attribute('href') \
            for news_tag in news_tags
    ]
    # print(news_page_urls)
    
    for news_page_url in news_page_urls:
        # access to article page
        driver.get(news_page_url)
        time.sleep(1)
        
        # try to get main content tag
        main_content_xpath = '//div[@class="content-detail"]'
        try:
            main_content_tag=driver.find_element(
                By.XPATH,
                main_content_xpath
            )
        except:
            continue
        
        # ignore video article
        video_content_xpath='//div[@class="video-detail"]'
        try:
            video_content_tag = main_content_tag.find_element(
                By.XPATH,
                video_content_xpath
            )
            continue
        except:
            pass
        
        # get title h1 tag
        title=main_content_tag.find_element(
            By.TAG_NAME,
            'h1'
        ).text.strip()
        print(f'title {title}')
        # get abstract h2 tag
        abstract= main_content_tag.find_element(
            By.TAG_NAME,
            'h2'
        ).text.strip()
        print(f'abstract {abstract}')
        # get author name (span tag)
        try:
            author_xpath = '//span[@class="name"]'
            author = main_content_tag.find_element(
                By.XPATH,
                author_xpath
            ).text.strip()
        except:
            author=''
        # get paragraphs (all p tags in div "maincontent main-content")
        paragraphs_xpath = '//div[@class="maincontent main-content"]'
        paragraphs_tags = main_content_tag.find_elements(
            By.XPATH,
            paragraphs_xpath
        )
        paragraphs_lst = [
            paragraphs_tag.text.strip()\
                for paragraphs_tag in paragraphs_tags
        ]
        paragraphs = ' '.join(paragraphs_lst)
        #  combine title, abstract, authoor and paragraphs
        final_content_lst = [title,abstract,paragraphs,author]
        final_content = '\n\n'.join(final_content_lst)
        print(f'final_content {final_content}')
        
        # save artile to .txt file
        article_filename = f'article_{article_id:05d}.txt'
        article_savepath = os.path.join(
            root_dir,
            article_filename
        )
        
        article_id +=1
        with open(article_savepath,'w',encoding='utf-8') as f:
            f.write(final_content)
            
        # move back to previous page
        driver.back()
        

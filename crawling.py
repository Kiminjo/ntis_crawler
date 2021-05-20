# -*- coding: utf-8 -*-
"""
Created on Thu May 20 19:23:06 2021

@author: user
"""

import pandas as pd
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Crawling :
    def __init__(self, source, id, pw) :
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.source = source
        self.id = id
        self.pw = pw


    def call_new_window(self) :
        self.driver.get(self.source)
        
        
    def log_in(self) :
        self.driver.find_element_by_class_name('login').click()
        self.change_to_new_page()
        self.driver.find_element_by_class_name('id').send_keys(self.id)
        self.driver.find_element_by_class_name('pw').send_keys(self.pw)
        self.driver.find_element_by_class_name('btn_blue').click()
        self.change_to_original_page()
        
        
    def search_by_id(self, id_of_doc) :
        self.remove_previous_search()
        self.driver.find_element_by_id('searchWord').send_keys(id_of_doc)
        self.driver.find_element_by_id('searchWord').send_keys(Keys.ENTER)
        
        
    def get_company_information(self) :
        self.driver.find_element_by_class_name('announce').click()
        self.change_to_new_page()
        content = self.driver.find_elements_by_class_name('pre_line')
        content = [ele.text for ele in content]
        self.close()
        self.change_to_original_page()
        
        return content
        
    def remove_previous_search(self) :
        for i in range(10) :
            self.driver.find_element_by_id('searchWord').send_keys(Keys.BACKSPACE)

    def change_to_original_page(self) :
        self.driver.switch_to.window(self.driver.window_handles[0])
        
        
    def change_to_new_page(self) :
        self.driver.switch_to.window(self.driver.window_handles[1])
    
    def take_a_break(self) :
        time.sleep(random.randint(5, 15))
    
    def close(self):
        self.driver.close()
    
    
    
if __name__ == '__main__':
    source = open('source.txt', 'r').read()
    PERSONAL = open('personal.txt', 'r').readlines() 
    ID = PERSONAL[0]; PW = PERSONAL[1]
    repo_id = ['1415172846', '1425122290']
    
    crawler = Crawling(source, ID, PW)
    crawler.call_new_window()
    crawler.log_in()
    
    total_text = []
    for id in repo_id :
        crawler.search_by_id(id)
        contents = crawler.get_company_information()
        total_text.append(contents)
        crawler.take_a_break()
        
    crawler.close()
    
    database = pd.DataFrame(total_text, columns=['연구목표', '연구내용', '기대효과'])

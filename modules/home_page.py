import json
from selenium.webdriver.common.keys import Keys
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class homePage ():

    def __init__(self):
        self.data = None

    def setUpClass (self):
        self.driver = webdriver.Chrome (executable_path="C:/Chrome/chromedriver.exe")
        self.driver = implicitly_wait(10)
        self.driver.maximize_window()


    def connect(self,data_file):
        with open (data_file) as json_file:
            self.data = json.load(json_file)
    

    def get_data (self,sitename):
        for homePage in self.data['homepages']:
            if homePage['site_name'] == sitename:
                return homePage

    def get_all_data(self):
        return self.data
    
    



    
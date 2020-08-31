import pytest
import json
from selenium.webdriver.common.keys import Keys
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from PIL import Image, ImageChops, ImageStat
from io import BytesIO
import cv2
import os.path
from os import path
from modules.home_page import homePage


@pytest.fixture(scope='module')
def db ():
    db = homePage ()
    db.connect('data.json')
    print("DB")
    return db

@pytest.fixture(scope='module')
def driver ():
    driver = webdriver.Chrome(executable_path="C:/Chrome/chromedriver")
    yield driver
    driver.close ()
    driver.quit ()
    
    
def is_file_exists (filename):
    return path.exists(filename)

def take_screenshot_of_element (driver,element,filename):
    location = element.location
    size = element.size

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    png = driver.get_screenshot_as_png()
    im = Image.open(BytesIO(png)) # uses PIL library to open image in memory
    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save("images/"+filename) # saves new cropped image

def compare_images (image1_path, image2_path):

    original = cv2.imread("images/"+image1_path)
    duplicate = cv2.imread("images/"+image2_path)
    
    im1 = Image.open("images/"+image1_path)
    im2 = Image.open("images/"+image2_path)

    print ("CHECK DIFFERENCE")
    

    diff_img= ImageChops.difference(im1, im2)
    stat = ImageStat.Stat(diff_img)
    diff_ratio = sum(stat.mean) / (len(stat.mean) * 255)

    total = diff_ratio * 100 



    
    print("RATIO IS:",total)

    
    if original.shape == duplicate.shape:
        diff = cv2.subtract(original, duplicate)
        diff2 = cv2.subtract(duplicate, original)
        #print(diff2)
        
        
        b,g,r = cv2.split(diff)
        if total == 0 and cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
            print("The images are completley equal")
            os.remove("images/"+image2_path)
            pass
            
        else:
            print ("Both images are not equal")
            os.remove("images/"+image2_path)
            raise AssertionError ("Both images are not same:",image1_path)
    else:
        print ("Both images do not have a same size")
        os.remove("images/"+image2_path)
        raise AssertionError ("Both images do not have a same size:", image1_path)



def click_signIn_btn (driver,xpath):
    time.sleep(10)
    driver.find_element(by=By.XPATH, value=xpath).click()
    time.sleep(5)



    #with open ("data.json") as json_file:
     #   data = json.load(json_file)
    #    for i in range (len(db["homepages"])):
   #         print(data["homepages"][i]["site_name"])

def task_manager (db,driver, sitename):
    
    #Initialize variables
    sites_data = db.get_data (sitename)
    site_url = sites_data["site_url"]
    loginbtn_xpath = sites_data["loginbtn_xpath"]
    loginwindow_xpath = sites_data ["loginwindow_xpath"]
    original_filename = sites_data ["original_filename"]
    new_filename = sites_data["new_filename"]

    #Visit homepage and find login window
    driver.get(site_url)
    click_signIn_btn (driver,loginbtn_xpath)
    element = driver.find_element(by=By.XPATH, value=loginwindow_xpath)

    #Check local images, take screenshots and compare images
    if is_file_exists("images/"+original_filename):
        take_screenshot_of_element(driver,element,new_filename)
        compare_images(original_filename,new_filename)
    else:
        take_screenshot_of_element(driver,element,original_filename)
       
    pass


def test_task_manager (db,driver):
    
    json_data = db.get_all_data ()
    print (len(json_data["homepages"]))
    data = json_data["homepages"]

    for i in range (len(data)):
        site_name = data[i]["site_name"]
        task_manager(db, driver, site_name)
        
    #compare_images ("pfizerprofr_original.png","pfizerprofr_test.png")


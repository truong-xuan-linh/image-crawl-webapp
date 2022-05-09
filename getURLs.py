from lib2to3.pgen2 import driver
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

PATH = ".\geckodriver.exe"
options = Options()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Firefox(executable_path= PATH, options= options)

def getURLs(location_name):
    driver.get("https://www.google.com/search?q=" + location_name + "&source=lnms&tbm=isch") 

    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    with open("./get_google_urls.js", 'r') as jquery_js: 
        # 3) Read the jquery from a file
        jquery = jquery_js.read() 
        # 4) Load jquery lib
        a = driver.execute_script(jquery)
        # driver.execute_script('argument[0].click()')
    return a
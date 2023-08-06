from selenium import webdriver 
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
#driver = webdriver.Chrome(ChromeDriverManager().install())
def webaccess(str):
    driver =webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.get(str)
    sleep(5)

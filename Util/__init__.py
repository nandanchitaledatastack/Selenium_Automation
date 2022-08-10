from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

print("Initializing webdriver")
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(30)
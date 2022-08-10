from lib2to3.pgen2 import driver
from selenium import webdriver
import time
import unittest
from icecream import ic
from selenium.webdriver.common.by import By
import pandas as pd

from webdriver_manager.chrome import ChromeDriverManager

class LoginPage(unittest.TestCase):
    def setUp(self):
        self.driver = driver #webdriver.Chrome(ChromeDriverManager().install())

    def readData(self):
        # Load the xlsx file
        excel_data = pd.read_excel('UIInput.xlsx')
        # Read the values of the file in the dataframe
        self.data = pd.DataFrame(excel_data, columns=['username','password'])
        
    
    def testLogin(self):
        driver = self.driver
        try:
            driver.get("https://localhost:44346/")
            driver.maximize_window()
        except Exception as e:
            ic(e)
        else:
            print("Getting forntend UI Elements.")
            f_username = driver.find_element(By.ID,"username")
            f_password = driver.find_element(By.ID,"passeord")
            f_submit_btn = driver.find_element(By.CLASS_NAME,"btn")
            
            print("Clearing out input fields")
            f_username.clear()
            f_password.clear()
            
            self.readData()
                
            v_username = self.data['username'].values[0]
            v_password = self.data['password'].values[0]
            
            print("Passing values in input fields")
            f_username.send_keys(v_username)
            f_password.send_keys(v_password)
            
            print("Submit button click")
            f_submit_btn.click()
            
            time.sleep(5)
            
            print("Comparing URL After submit")
            current_url = driver.current_url
            expected_url = "https://localhost:44346/Reports/Report/Homepage"
            message = "Unable to login."
            
            try:
                self.assertEqual(current_url, expected_url, message)
                print("URL's matched")
            except Exception as e:
                ic(e)
            
            time.sleep(100)
            
    def tearDown(self):
        self.driver.quit()
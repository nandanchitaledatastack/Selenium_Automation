import time
import unittest
from icecream import ic

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select as select_elem
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pynput.keyboard import Key, Controller
from selenium.webdriver.common.action_chains import ActionChains

import os

import pandas as pd

import logging

from webdriver_manager.chrome import ChromeDriverManager

class NewRequest(unittest.TestCase):
    def setUp(self):
        '''
            Method to set up the driver
        '''
        # print("Setting up driver and logger")
        # logging.info("Setting up driver")
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        # logging.basicConfig(
        #     filename='Logs/newRequest_debug.log', 
        #     filemode='w', 
        #     format='%(name)s - %(levelname)s - %(message)s', 
        #     level=logging.INFO
        # )
        # logger = logging.getLogger()
        # logger.info("Logger Configured")
        # logger.log(logging.INFO, "Logger configured")
        # print("Logger configured")

    def readLoginData(self):
        '''
            Method to read data from excel sheet
        '''
        # Load the xlsx file
        excel_data = pd.read_excel('UIInput.xlsx', sheet_name = "login")
        # Read the values of the file in the dataframe
        self.loginData = pd.DataFrame(excel_data, columns=['username','password'])
        
    def readRequestInfoData(self):
        '''
            Method to read data from excel sheet
        '''
        # Load the xlsx file
        excel_data = pd.read_excel('UIInput.xlsx', sheet_name="initiate_request")
        # Read the values of the file in the dataframe
        self.requestInfoData = pd.DataFrame(excel_data, columns=['material_name','Material Description','To Be Used For','Reason For Adding', 'materialCategories', 'marketTypes', 'Locations', 'supplier', 'supplierEmployee', 'divisions', 'requestType', 'requestInfoDocumentDescription','supplierEmployeeSearchString','supplierSearchString','filepath', 'filename','modalComments'])
        
    
    def test_login(self):
        '''
            Method to login into application
        '''
        self.readLoginData()
        driver = self.driver
        try:
            driver.get("https://localhost:44346/")
            driver.maximize_window()
        except Exception as e:
            logging.error(e, exc_info=True)
        else:
            logging.info("Getting forntend UI Elements.")
            self.getLoginElements(driver)
            
            logging.info("Clearing out input fields")
            self.clearLoginElements()
                        
            login_data = {
                'username' : self.loginData['username'].values[0],
                'password' : self.loginData['password'].values[0]
            }
                
            logging.info("Passing values in input fields")
            self.performLoginActivity(login_data)
            
            logging.info("Submit button click")
            self.f_submit_btn.click()    
            
            # Validate Login        
            self.loginValidation(driver)
            
            # Open New Request Page
            self.openNewRequestPage(driver)
        
            self.getRequestInfoPageElements(driver)
        
            # Clear Request Info elements
            self.clearRequestInfoElements()
        
            self.readRequestInfoData()            
            request_info_data = {
                'material_name' : self.requestInfoData['material_name'].values[0],
                'materialDescription' : self.requestInfoData['Material Description'].values[0],
                'materialCategories' : self.requestInfoData['materialCategories'].values[0],
                'divisions' : self.requestInfoData['divisions'].values[0],
                'locations' : self.requestInfoData['Locations'].values[0],
                'requestType' : self.requestInfoData['requestType'].values[0],
                'toBeUsedFor' : self.requestInfoData['To Be Used For'].values[0],
                'reasonForAdding' : self.requestInfoData['Reason For Adding'].values[0],
                'supplier' : self.requestInfoData['supplier'].values[0],
                'supplierEmployee' : self.requestInfoData['supplierEmployee'].values[0],
                'requestInfoDocumentDescription' : self.requestInfoData['requestInfoDocumentDescription'].values[0],
                'supplierSearchString' : self.requestInfoData['supplierSearchString'].values[0],
                'supplierEmployeeSearchString' : self.requestInfoData['supplierEmployeeSearchString'].values[0],
                'filepath' : self.requestInfoData['filepath'].values[0],
                'filename' : self.requestInfoData['filename'].values[0],
                'requestInfoComments' : self.requestInfoData['modalComments'].values[0],
            }
            self.populateInput(driver, request_info_data, login_data)
            time.sleep(100)
        
    def openNewRequestPage(self,driver):
        try:
            driver.get("https://localhost:44346/Supplier/SupplierApproval")
        except Exception as e:
            logging.error(e, exc_info=True)            
    
    def getLoginElements(self, driver):
        self.f_username = driver.find_element(By.ID,"username")
        self.f_password = driver.find_element(By.ID,"passeord")
        self.f_submit_btn = driver.find_element(By.CLASS_NAME,"btn")
    
    def clearLoginElements(self):
        self.f_username.clear()
        self.f_password.clear()
    
    def performLoginActivity(self, login_data):
        v_username = login_data['username']
        v_password = login_data['password']
        self.f_username.send_keys(v_username)
        self.f_password.send_keys(v_password)
    
    def getRequestInfoPageElements(self, driver):
        time.sleep(5)
        self.f_materialName = driver.find_element(By.ID,"ipMaterialName")
        self.f_materialDescription = driver.find_element(By.ID,"ipMaterialDescription")
        self.f_materialCategories = Select(driver.find_element(By.ID,"materialCategories"))
        self.f_divisions = Select(driver.find_element(By.ID,"divisions"))
        self.f_requestType = Select(driver.find_element(By.ID,"requestType"))
        self.f_toBeUserdFor = driver.find_element(By.ID,"ipToBeUsedFor")
        self.f_reasonForAdding = driver.find_element(By.ID,"ipReasonForAdding")
        self.f_supplierSelect = driver.find_element(By.ID,"supplierSelect")
        self.f_supplierEmployeeSelect = driver.find_element(By.ID,"supplierEmployeeSelect")
        self.f_locations = driver.find_element(By.NAME, "locations")
        self.f_materialMarkets = driver.find_element(By.NAME, "marketTypes")
        # self.f_selectedLocation = driver.find_element(By.ID, "32")
        # self.f_selectedMarket = driver.find_element(By.ID, "1794")
        self.f_selectedLocation = self.f_locations.find_elements(By.NAME, "locations")
        self.f_selectedMarket = self.f_locations.find_element(By.XPATH, "//*[@id='1794']")
        self.f_requestInfoDocumentDescription = driver.find_element(By.ID,"ipSupplierRequestInfoDocumentDescription")
        self.f_fileInput = driver.find_element(By.XPATH, "//form[@id='supplierRequestInfo']//*[@id='supplierDocument']")
        self.f_requestInfoSubmitBtn = driver.find_element(By.ID, "addsupplierRequestInfoBtn")
        self.f_submitConfirmationModalUsername = driver.find_element(By.ID, "modalUsername")
        self.f_submitConfirmationModalPassword = driver.find_element(By.ID, "modalPassword")
        self.f_submitConfirmationModalComments = driver.find_element(By.ID, "modalComments")
        self.f_submitConfirmationModalSubmitBtn = driver.find_element(By.ID, "submitTransaction")
        
    def clearRequestInfoElements(self):
        self.f_materialDescription.clear()
        self.f_toBeUserdFor.clear()
        self.f_reasonForAdding.clear()
        
    
    def populateDataListInput(self, driver, input_element, data, selector_type, selector_element):
        input_element.send_keys(data)
        input_element.click()
        driver.implicitly_wait(2)
        v_datalist = driver.find_elements(selector_type,selector_element) #//form[@id='supplierRequestInfo']/*//*[@id='materialNameDataList']/option
        input_element.click()
        driver.implicitly_wait(2)
    
    def populateInput(self,driver, request_info_data, login_data):
        try:
            # select material
            # time.sleep(2)
            #v_materialNameDataList = driver.find_element(By.CSS_SELECTOR,"//*//*[@id='materialNameDataList']/option") #//form[@id='supplierRequestInfo']/*//*[@id='materialNameDataList']/option
            time.sleep(2)

            css_selector = "#supplierRequestInfo #materialNameDataList option"
            self.populateDataListInput(driver, self.f_materialName, request_info_data['material_name'], By.CSS_SELECTOR, css_selector)

            # self.f_materialName.send_keys(request_info_data['material_name'])
            # self.f_materialName.click()
            # driver.implicitly_wait(2)
            # v_materialNameDataList = driver.find_elements(By.CSS_SELECTOR,"#supplierRequestInfo #materialNameDataList option") #//form[@id='supplierRequestInfo']/*//*[@id='materialNameDataList']/option
            # self.f_materialName.click()
            # driver.implicitly_wait(2)

            # enter material description
            self.f_materialDescription.send_keys(request_info_data['materialDescription'])

            # select request type
            self.f_requestType.select_by_value(request_info_data['requestType'])

            # select material category
            self.f_materialCategories.select_by_visible_text(request_info_data['materialCategories'])

            # select material division
            self.f_divisions.select_by_value(request_info_data['divisions'])

            # select material location
            selectedLocation = "//form[@id='supplierRequestInfo']//*[@name='locations' and @value='{}']".format(request_info_data['locations'])
            self.f_selectedLocation = driver.find_element(By.XPATH, selectedLocation)
            self.f_selectedLocation.click()

            # select material market
            self.f_selectedMarket.click()

            # enter to be used for
            self.f_toBeUserdFor.send_keys(request_info_data['toBeUsedFor'])

            # enter reason for adding
            self.f_reasonForAdding.send_keys(request_info_data['reasonForAdding'])

            # select supplier 
            xpath_selector = "//form[@id='supplierRequestInfo']//*[@id='supplierdatalist']//option[contains(text(),'{}')]".format(request_info_data['supplierSearchString'])
            self.populateDataListInput(driver, self.f_supplierSelect, request_info_data['supplierSearchString'], By.XPATH, xpath_selector)
              
            # self.f_supplierSelect.send_keys(request_info_data['supplierSearchString'])
            # self.f_supplierSelect.click()
            # driver.implicitly_wait(2)
            # # supplierXPath = "//form[@id='supplierRequestInfo']//*[@id='supplierdatalist']//option[contains(text(),'{}')]".format(request_info_data['supplier'])
            # # v_supplierDataListOption = driver.find_element(By.XPATH, supplierXPath)
            # v_supplierDataListOption = driver.find_elements(By.CSS_SELECTOR,"#supplierRequestInfo #supplierdatalist option") #//form[@id='supplierRequestInfo']/*//*[@id='materialNameDataList']/option
            # self.f_supplierSelect.click()
            # time.sleep(5)
            
            #driver.implicitly_wait(2)    
        
            # self.f_supplierSelect.send_keys(request_info_data['supplier'])
            # self.f_supplierSelect.click()
            # #driver.implicitly_wait(2)
            # v_datalist_option = driver.find_elements(By.CSS_SELECTOR,"#supplierRequestInfo #supplierdatalist option") #//form[@id='supplierRequestInfo']/*//*[@id='materialNameDataList']/option
            # select_object = select_elem(v_datalist_option)
            # # select_object.select_by_value("ABC Test Material Supplier:8457")
            # #v_datalist_option.click()
            # self.f_supplierSelect.click()
            # time.sleep(5)
            # self.f_reasonForAdding.click()
            # time.sleep(5)
            # #driver.implicitly_wait(5)

            self.f_reasonForAdding.click()

            # select supplier employee 
            xpath_selector = "//form[@id='supplierRequestInfo']//*[@id='supplierEmployeedatalist']//option[contains(text(),'{}')]".format(request_info_data['supplierEmployeeSearchString'])
            self.populateDataListInput(driver, self.f_supplierEmployeeSelect, request_info_data['supplierEmployeeSearchString'], By.XPATH, xpath_selector)
              
            # self.f_supplierEmployeeSelect.send_keys(request_info_data['supplierEmployeeSearchString'])
            # time.sleep(5)
            # self.f_supplierEmployeeSelect.click()
            # driver.implicitly_wait(2)
            # v_supplierEmployeeDataList = driver.find_elements(By.CSS_SELECTOR,"#supplierRequestInfo #supplierEmployeedatalist option") #//form[@id='supplierRequestInfo']/*//*[@id='materialNameDataList']/option
            # self.f_supplierEmployeeSelect.click()
            # driver.implicitly_wait(2)   
            
            # self.f_supplierEmployeeSelect.send_keys(request_info_data['supplierEmployee'])
            # time.sleep(5)
            # self.f_supplierEmployeeSelect.click()
            # time.sleep(5)
            # #driver.implicitly_wait(2)
            # driver.find_elements(By.CSS_SELECTOR,"#supplierRequestInfo #supplierEmployeedatalist option") #//form[@id='supplierRequestInfo']/*//*[@id='materialNameDataList']/option
            # # supplierEmployeeXPath = "//form[@id='supplierRequestInfo']//*[@id='supplierEmployeedatalist']//option[contains(text(),'{}')]".format(request_info_data['supplierEmployee'])
            # # driver.find_element(By.XPATH, supplierEmployeeXPath).click()
            # self.f_supplierEmployeeSelect.click()
            # time.sleep(5)
            
            # action = ActionChains(driver)
            # self.f_supplierEmployeeSelect.send_keys(request_info_data['supplierEmployee'])
            # # self.f_supplierEmployeeSelect.click()
            # # time.sleep(5)
            # #driver.implicitly_wait(2)
            # # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "supplierEmployeeSelect"))).send_keys(Keys.DOWN).send_keys(Keys.ENTER)

            # # supplierEmployeeXPath = "//form[@id='supplierRequestInfo']//*[@id='supplierEmployeedatalist']//option[contains(text(),'{}')]".format(request_info_data['supplierEmployee'])
            # # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, supplierEmployeeXPath))).send_keys(Keys.DOWN).send_keys(Keys.ENTER)
            # # self.f_supplierEmployeeSelect.click()
            # supplierEmployeeXPath = "//form[@id='supplierRequestInfo']//*[@id='supplierEmployeedatalist']//option"
            # element = driver.find_element(By.XPATH, supplierEmployeeXPath)
            
            # action.move_to_element(element).click()
            # action.perform()
            
            # driver.execute_script("arguments[0].click();", element)
            # # self.f_supplierEmployeeSelect.click()
            # time.sleep(5)
            
            # self.f_reasonForAdding.click()
            # element = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.ID, "supplierEmployeeSelect"))
            # )
            # element.send_keys(request_info_data['supplierEmployeeSearchString'])
            # time.sleep(2)
            # driver.implicitly_wait(5)
            # keyboard = Controller()


            # time.sleep(2)
            
            # self.f_supplierEmployeeSelect.send_keys(Keys.DOWN)
            # # self.f_supplierEmployeeSelect.send_keys(Keys.ENTER)
            # keyboard.press(Key.enter)
            # keyboard.release(Key.enter)

            # time.sleep(5)
            #driver.implicitly_wait(2)
            
            # v_supplierEmployeeDataList = driver.find_element(By.XPATH,"//form[@id='supplierRequestInfo']//*[@id='supplierEmployeedatalist']//option[contains(text(),'Varsha Patel')]") #//form[@id='supplierRequestInfo']/*//*[@id='materialNameDataList']/option
            # self.f_supplierEmployeeSelect.click()
            # time.sleep(5)
            #driver.implicitly_wait(5)
            
            
                   
            # self.f_supplierEmployeeSelect.send_keys(request_info_data['supplierEmployeeSearchString'])
            # # self.f_supplierEmployeeSelect.click()
            # time.sleep(5)
            # # driver.implicitly_wait(2)

            # option_value = driver.find_element(By.XPATH,"//form[@id='supplierRequestInfo']//*[@id='supplierEmployeedatalist']//option[contains(text(),'Varsha Patel')]").get_attribute("value")
            # self.f_supplierEmployeeSelect.clear()
            # self.f_supplierEmployeeSelect.send_keys(option_value)

            # # v_supplierEmployeeOption.click()
            # # v_supplierEmployeeDataList = driver.find_element(By.XPATH,"#supplierRequestInfo #supplierEmployeedatalist option") #//form[@id='supplierRequestInfo']/*//*[@id='materialNameDataList']/option
            # # self.f_supplierEmployeeSelect.click()
            # time.sleep(5)
            # #driver.implicitly_wait(120)
    
            # File description
            self.f_requestInfoDocumentDescription.send_keys(request_info_data['requestInfoDocumentDescription'])
            
            # File input
            # self.f_fileInput.click()
            self.f_fileInput.send_keys(os.path.join(request_info_data['filepath'],request_info_data['filename']))

            self.f_requestInfoSubmitBtn.click()
            driver.implicitly_wait(2)
            self.f_submitConfirmationModalPassword.send_keys(login_data['password'])
            self.f_submitConfirmationModalComments.send_keys(request_info_data['requestInfoComments'])
            self.f_submitConfirmationModalSubmitBtn.click()
    
            driver.implicitly_wait(500)
            ic("Wait")
        except Exception as e:
            ic(e)
                
    def loginValidation(self,driver):
        current_url = driver.current_url
        expected_url = "https://localhost:44346/Reports/Report/Homepage"
        err_message = "Unable to login."
            
        try:
            self.assertEqual(current_url, expected_url, err_message)
            logging.info("URL's matched")
            # f_welcome_user = WebDriverWait(driver, 10).until_not(
            #     EC.presence_of_element_located((
            #         By.CLASS_NAME, "sessionUser"))
            # )
            # val = f_welcome_user.getAttribute("innerText")
            # ic(val)
        except Exception as e:
            logging.error(e, exc_info=True)
          
    def tearDown(self):
        self.driver.quit()
   
if __name__ == "__main__" :
    unittest.main()
    

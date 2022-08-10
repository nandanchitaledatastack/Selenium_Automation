from lib2to3.pgen2 import driver
from selenium import webdriver
import time
import unittest
from icecream import ic
from selenium.webdriver.common.by import By
import xlrd
from openpyxl import load_workbook
import pandas as pd
    

class Test:   
    def readRequestInfoData(self):
        '''
            Method to read data from excel sheet
        '''
        # Load the xlsx file
        excel_data = pd.read_excel('../UIInput.xlsx', sheet_name="Sheet3")
        # Read the values of the file in the dataframe
        self.requestInfoData = pd.DataFrame(excel_data, columns=['material_name','Material Description','To Be Used For','Reason For Adding', 'materialCategories'])
        
        ic(self.requestInfoData['material_name'].values[0])
        ic(self.requestInfoData['Material Description'].values[0])
        ic(self.requestInfoData['To Be Used For'].values[0])
        ic(self.requestInfoData['Reason For Adding'].values[0])
    
if __name__=="__main__":
    test = Test()
    test.readRequestInfoData()
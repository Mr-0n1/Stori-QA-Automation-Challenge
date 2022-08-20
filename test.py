#import argparse
#import sys
import HtmlTestRunner
from multiprocessing.connection import wait
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.opera import OperaDriverManager
import time

# initialize arguments and add arguments
"""parser = argparse.ArgumentParser()
parser.add_argument('--browser', help= "Browser to execute test cases.", type=str, default='firefox')
args = parser.parse_args()"""

url = "https://rahulshettyacademy.com/AutomationPractice/"

# alternative to parse arguments (they didn't work because of the unittest framework)
browser = input("Browser to execute tests: ")

class test_cases(unittest.TestCase):
    
    #setup browser
    def setUp(self):    
        
        match browser:
            case "chrome":
                self.driver = webdriver.Chrome(executable_path=r"Drivers/chromedriver.exe")
            case "firefox":
                self.driver = webdriver.Firefox(executable_path=r"Drivers/geckodriver.exe")
            case "opera":
                #self.driver = webdriver.Opera(executable_path=r"Drivers/geckodriver.exe")
                self.driver = webdriver.Opera(executable_path=OperaDriverManager().install())
        
        """if sys.argv[1] == 'firefox':
            self.driver = webdriver.Firefox(executable_path=r"Drivers/geckodriver.exe")
        elif sys.argv[1] == 'chrome':
            self.driver = webdriver.Chrome(executable_path=r"Drivers/chromedriver.exe")
        else:
            self.driver = webdriver.Firefox(executable_path=r"Drivers/geckodriver.exe")"""
        
        #self.driver = webdriver.Firefox(executable_path=r"Drivers/geckodriver.exe")

        
    # 1 - Open browser and url
    def test_open_url(self):
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(3)     
        
    # 2 - Suggestion Class Example
    def test_suggestion_class_example(self):
        driver = self.driver
        self.driver.get(url)
        self.driver.maximize_window()
        input_xpath = driver.find_element(By.XPATH, "//*[@id='autocomplete']").send_keys("Me")
        time.sleep(3)
        option_xpath = driver.find_element(By.XPATH, "//*[@id='ui-id-7']").click()
        time.sleep(3)
    
    # 3 - Dropdown Example
    def test_dropdown_example(self):
        driver = self.driver
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(2)
        drop_select = driver.find_element(By.XPATH, "//select").click()
        time.sleep(2)
        option_2 = driver.find_element(By.XPATH, "//option[3]").click()
        time.sleep(2)
        drop_select = driver.find_element(By.XPATH, "//select").click()
        time.sleep(2)
        option_2 = driver.find_element(By.XPATH, "//option[4]").click()
        time.sleep(3)
        
    # 4 - Switch Window Example
    def test_switch_window_example(self):
        driver = self.driver
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(2)
        #click switch button and change windows
        driver.find_element(By.XPATH, "//*[@id='openwindow']").click()
        #print(driver.current_window_handle)
        
        #change to the new window
        new_window =  driver.window_handles[1]
        driver.switch_to.window(new_window)
        time.sleep(5)
        #print(new_window)
        #print(driver.title)
        
        #begin test - check element (warranty) existence.
        try:
            #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "")))
            element = driver.find_element(By.XPATH, "/html/body/section[3]/div/div/div/div[5]/div/div[2]/div/div[2]")
            not_found = False
        except:
            not_found = True
        self.assertTrue((not_found != True), "FAILED TEST, ELEMENT NOT FOUND.")
        
        time.sleep(3)
        
    # 5 - Switch Tab Example
    def test_switch_table_example(self):
        #window setup and debug
        driver = self.driver
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(2)
        
        #Initiate task
        current_tab = driver.window_handles[0]
        driver.find_element(By.XPATH, "//*[@id='opentab']").click()
        new_tab = driver.window_handles[1]
        driver.switch_to.window(new_tab)
        #time.sleep(5)
        #print(driver.title)
        time.sleep(3)

        # scroll to element (by css selector)
        element = driver.find_element(By.CSS_SELECTOR, "div.courses-block:nth-child(12) > div:nth-child(1)")
        driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(3)
        
        # Take screenshot and save it
        driver.get_screenshot_as_file("switch_tab_example.png")
        print("|| SCREENSHOT SAVED!. ||")
        
        # Return to previous tab
        driver.switch_to.window(current_tab)
        print(driver.title)        
        
        time.sleep(3)
        
    # 6 - Switch to Alert Example
    def test_switch_to_alert_example(self):
        #window setup and debug
        driver = self.driver
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(2)
        
        # print the string and show alert text
        input = driver.find_element(By.XPATH, "//*[@id='name']").send_keys("Stori Card")
        time.sleep(3)
        alert = driver.find_element(By.CSS_SELECTOR, "#alertbtn").click()
        time.sleep(3)
        
        # Switch to alert and print text. then click accept.
        print(driver.switch_to.alert.text)
        driver.switch_to.alert.accept()
        
        time.sleep(3)
        
    # 7 - Web Table Example. (this was the most difficult for me)
    def test_web_table_example(self):
        #window setup and debug
        driver = self.driver
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(2)
        
        # Locate WebElement table and append every row in a list to handle
        courses_list = []
        courses = driver.find_element(By.CSS_SELECTOR, "table.table-display")
        #rows = courses.find_elements(By.CSS_SELECTOR, "tr")
        for row in courses.find_elements(By.CSS_SELECTOR, 'tr'):
            row_list = []
            for cell in row.find_elements(By.CSS_SELECTOR, 'td'):
                #print(cell.text)
                row_list.append(cell.text)
            courses_list.append(row_list)
        #print(courses_list)
        courses_list.pop(0)
        
        # Handle the new list and create another new with the selected courses.
        new_list = []
        for item in range(len(courses_list)):
            if courses_list[item][2] == '25':
                new_list.append(courses_list[item])            
        #print(new_list)
        
        # Show lenght of new list and the name of every course
        print("The number of courses which cost $25 are: ", len(new_list))
        print("-------------")
        
        for course in range(len(new_list)):
            print(new_list[course][1], ",")
        
        time.sleep(3)
    
    # 8 - Web Table Fixed.
    def test_web_table_fixed(self):
        #window setup and debug
        driver = self.driver
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(2)
        
        # locate table
        engineer_list = []        
        table = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/fieldset[2]/div[1]/table/tbody")
        for row in table.find_elements(By.CSS_SELECTOR, 'tr'):
            row_list = []
            for cell in row.find_elements(By.CSS_SELECTOR, 'td'):
                #print(cell.text)
                row_list.append(cell.text)
            engineer_list.append(row_list)        

        # print only names
        print("The names are : ")
        for item in range(len(engineer_list)):
            print(engineer_list[item][0], ",")
        time.sleep(3)
        
    # 9 - iFrame Example
    def test_iframe_example(self):
        #window setup and debug
        driver = self.driver
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(2)
    
        # Locate iFrame and switch, then get the text and handle it to a list
        frame = driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='courses-iframe']"))
        text = driver.find_element(By.XPATH, "//section[4]/div/div/div/div[2]/ul/li[2]")
        text = text.text
        text_list = text.split(" ")
        #print(text_list)
        
        # Iterate and print only odd indexes
        print("Printed only odd indexes of found text :")
        for index in range(len(text_list)):
            if index % 2 == 0 and index != 0: # parity of zero, What is that?
                print(text_list[index], ",")
        
        time.sleep(3)
    
    
    def tearDown(self):
        self.driver.quit()
    
if __name__ == '__main__':
    #print(sys.argv[1])
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='Reports'))
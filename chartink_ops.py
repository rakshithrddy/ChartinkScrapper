from config import Config as conf
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


class ChartInkOps:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome('./chromedriver.exe')
        self.scanner_names = []

    def login_to_chartink(self):
        self.driver.get(conf.chartink_link)
        time.sleep(2)
        
        #click on login button
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[5]/a').click()
        print('CLICKED LOG IN BUTTON')
        time.sleep(2)

        ## Enter username
        username = self.driver.find_element(By.NAME, 'email')
        username.send_keys(str(conf.chartink_link_user_name))
        print('Typed out username')
        time.sleep(1)

        # enter password
        passwd = self.driver.find_element(By.NAME, 'password')
        passwd.send_keys(conf.chartink_link_password)
        print('Typed out password')
        time.sleep(1)

        self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/form/div[4]/div/button').click()
        print('Clicked login button')
        time.sleep(1)

    def iterate_through_scans(self):
        try:
            counter = 2
            flag = True
            while flag:
                if self.driver.current_url != 'https://chartink.com/scan_dashboard':
                    self.driver.get('https://chartink.com/scan_dashboard')
                    time.sleep(1)

                    

                items = self.driver.find_elements(By.XPATH, f'/html/body/div[2]/div/div[2]/div[4]/div/table/tbody/tr[{counter}]/td[1]/a')
                if len(items) > 0:
                    scanner_name = items[0].text
                    print('Loading', scanner_name)
                    items[0].click()
                    time.sleep(5)

                    if scanner_name not in self.scanner_names:
                        self.scanner_names.append(scanner_name)
                        button = self.driver.find_elements(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[6]/div[1]/div/div[1]/div/button[3]')
                        button[0].click()
                        print('DOWNLOADING EXCEL')
                        time.sleep(5)
                        counter += 1
                    else:
                        flag = False
                else:
                    print("NO SCANS FOUND")
                    flag = False
        except Exception as e:
            print(e)
            self.iterate_through_scans()
    
    def filter_excels(self):
        print(self.scanner_names)


    def close_browser(self):
        self.driver.close()

    def main(self):
        self.login_to_chartink()
        self.iterate_through_scans()
        self.close_browser()
        self.filter_excels()
        


if __name__ == '__main__':
    obj = ChartInkOps()
    obj.main()

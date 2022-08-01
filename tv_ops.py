from selenium import webdriver
from config import Config as conf
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class TradingView:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome('./chromedriver.exe')
    
    
    def login_to_tv(self):
        self.driver.get(conf.tradingview_link)

        ### Find Login in  button and click
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[2]/div[3]/button[1]').click()
        time.sleep(2)

        ### find signin the submenu and click
        self.driver.find_element(By.XPATH, '/html/body/div[6]/div/span/div[1]/div/div/div/button[1]').click()
        time.sleep(2)

        ### find email button and click
        self.driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/div/div/div/div/div/div[1]/div[4]/div/span').click()
        time.sleep(2)

        ## Enter username
        username = self.driver.find_element(By.NAME, 'username')
        username.send_keys(str(conf.tradingview_user_name))
        time.sleep(1)

        # enter password
        passwd = self.driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/div/div/div/div/div/form/div[2]/div[1]/input')
        passwd.send_keys(conf.tradingview_password)
        time.sleep(1)

        # click on sigin button
        self.driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/div/div/div/div/div/form/div[5]/div[2]/button/span[2]').click()
        time.sleep(7)

    
    def clear_old_lists(self):
        deletable_lists = ['- long', '- short', '- double bottom', '- double top']
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[1]/div[1]/div[1]/div[1]/div/div/div[1]/div').click()
        time.sleep(2)

        items = self.driver.find_elements(By.XPATH, '/html/body/div[7]/div/span/div[1]/div/div')
        for item in items:
            print(f' {item.text} \n')
            break
            # if item.text in deletable_lists:
                
                # item.find_element_by_css_selector(css_selector='remove-button').click()
                # time.sleep(1)



    def close(self):
        self.driver.close()


if __name__ == '__main__':
    tv = TradingView()
    tv.login_to_tv()
    tv.clear_old_lists()

    tv.close()
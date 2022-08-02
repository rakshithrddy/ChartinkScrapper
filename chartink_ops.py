from config import Config as conf
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import re
import pandas as pd
import stat

class ChartInkOps:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome('./chromedriver.exe')
        self.scanner_names = []
        self.path_to_downloads = self._get_download_path()
        self.path_to_scans = os.path.join(self.path_to_downloads, 'Scans')
        
    def _get_download_path(self):
        """Returns the default downloads path for linux or windows"""
        if os.name == 'nt':
            import winreg
            sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                location = winreg.QueryValueEx(key, downloads_guid)[0]
            return location
        else:
            return os.path.join(os.path.expanduser('~'), 'downloads')

    def login_to_chartink(self):
        print('Loading main page')
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
    
    def _delete_old_files(self):
        print('DELETING OLD FILES')
        files = [f for f in os.listdir(self.path_to_downloads) if 'Technical Analysis Scanner' in f]
        for file in files:
            os.remove(os.path.join(self.path_to_downloads, file))
            print(f"File deleted: {file}")
        
        if not os.path.exists(self.path_to_scans):
            os.mkdir(self.path_to_scans)

        scans = [f for f in os.listdir(self.path_to_scans)]
        # os.chmod(file_name, stat.S_IWRITE)
        for scan in scans:
            os.remove(os.path.join(self.path_to_scans, scan))
            print(f"Scan Deleted: {scan}")

    def _read_new_files(self):
        print("WRITING SYMBOLS")
        download_path = self._get_download_path()
        files = [f for f in os.listdir(download_path) if 'Technical Analysis Scanner' in f]
        for file in files:
            data = pd.read_excel(os.path.join(download_path, file), skiprows=[0])
            data = data.replace('&', '_', regex=True)

            symbols = data['Symbol'].to_list()

            if len(symbols) > 0:
                with open(os.path.join(download_path + '/Scans/', file.split('.')[0] + '.txt'), 'w') as f:
                    f.write('\n'.join(symbols))
        print("COMPLETED WRITING SYMBOLS")

    def close_browser(self):
        self.driver.close()

    def main(self):
        self._delete_old_files()
        self.login_to_chartink()
        self.iterate_through_scans()
        self.close_browser()
        self._read_new_files()
        
if __name__ == '__main__':
    obj = ChartInkOps()
    obj.main()

# Web Scrapping Python-Selenium Library Obtaining  All Turkish Universities and Academic Staffs' Datas
You can get academic staff's past, education, thesis, fields in a .csv file and open it on Excel. 
(It's just for voluntary research, not for malicious or commercial purposes)

## How it works?
* You should install required Python libraries.
  ```python
  import requests
  from bs4 import  BeautifulSoup, NavigableString
  from selenium import webdriver
  from webdriver_manager.chrome import ChromeDriverManager
  from selenium.webdriver.chrome.options import Options
  import csv
  from selenium.webdriver.common.by import By
  ```
* You should give a path on line 10.
* Finally you should run 'yok-akademi-main.py' file.

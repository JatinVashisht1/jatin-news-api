from urllib import response
from selenium import webdriver
from selenium.webdriver.common.by import By
import News.constants as const
import os
from prettytable import PrettyTable
import requests

# from NewsScrapperBot.News.constants import BASE_URL_API

class News(webdriver.Edge):
    def __init__(self, driver_path = r"D:/desktop/Study/2nd Year/Sem4/Selenium FCC/edgedriver_win64", teardown = False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(News, self).__init__() # to instantiated the parent class
        
        # options = webdriver.ChromeOptions() # no EdgeOptionsAvailable :)
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        self.implicitly_wait(15)
        self.maximize_window() # to have a cleaner look when we will test the bot
        
    def __exit__(self, *args) -> None:
        if self.teardown:
            self.quit()
    
    def land_first_page(self):
        self.get(const.BASE_URL)
        
    def getNews(self):
        n = {}
        element = self.find_element(by=By.CLASS_NAME, value='lisingNews')
        element2= element.find_elements(by=By.CLASS_NAME, value='newsHdng')
        element3= element.find_elements(by=By.CLASS_NAME, value='newsCont')
        element4 = self.find_elements(by=By.CLASS_NAME, value= 'news_Itm-img')
        # element5 = element4.find_elements(by=By.CSS_SELECTOR, value= 'img[src]')
        
        
        collection = []
        collection2 = []
        collection3 = []
        
        for item in element2:
            collection.append([item.text])
        
        for item in element3:
            collection2.append([item.text])
        
        print(len(element4))
        for item in element4:
            element5 = item.find_element(by=By.CSS_SELECTOR, value= 'img[src]')
            # print(element5.get_attribute('src'))
            collection3.append(element5.get_attribute('src'))
            
        # '''
        table = PrettyTable()
        table.field_names = ["Title", "News"]
        for i in range(len(collection)):
            table.add_row([collection[i], collection2[i]])
            response = requests.post(const.BASE_URL_API + f"/news/{i}", {'title': collection[i], 'news': collection2[i], 'imageurl': collection3[i]})
            print(response)

        # print(table)
        
        # for i in range(len(element2)):
        #     n[element2[i].text] = element3[i].text
        
        # for item in n:
        #     print( f"\n{item} --- {n[item]}\n")
            
        # '''
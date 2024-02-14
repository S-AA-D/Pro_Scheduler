from selenium import webdriver
from selenium.webdriver.common.by import By
from checking import constants as CONST
from checking.email_sender import Email
import time
import os


class Checker(webdriver.Chrome):
    def __init__(self , tearDown = False):
        self.tearDown = tearDown

        os.environ['PATH']+=CONST.DRIVER_PATH
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach',True)
        options.add_experimental_option('excludeSwitches',['enable-logging'])
        super(Checker , self).__init__(options=options)
        self.implicitly_wait(90)

        self.data =[]

    def land_first_page(self):
        self.get(CONST.BASE_URL)
        self.maximize_window()
       

    def go_to_Exam(self):
        search_availability_btn = self.find_element(By.CSS_SELECTOR,'img[alt="Search Availability"]')
        search_availability_btn.click()

        sponsor_selector = self.find_element(By.ID , 'test_sponsor')
        sponsor_selector.send_keys('Saudi Commission for Health Specialities')
        
        program_selector = self.find_element(By.ID , 'testProgram')
        program_selector.send_keys('Saudi Licencing Examination')

        test_selector = self.find_element(By.ID , 'testSelector')
        test_selector.send_keys('Saudi Medical Licensing Exam')

        next_btn = self.find_element(By.ID , 'nextBtn')
        next_btn.click()

    #You can the city and country as you wish as well as the starting and ending date
    def location_and_date(self , location ="Riyadh, Saudi Arabia" , start_date='10/17/2023' , end_date="10/31/2023"):
        location = self.find_element(By.ID , 'searchLocation')
        location.send_keys("Riyadh, Saudi Arabia")

        s_date = self.find_element(By.CSS_SELECTOR , 'input[name="mydate"]')
        s_date.clear()
        s_date.send_keys(start_date)

        e_date = self.find_element(By.CSS_SELECTOR,'input[aria-describedby="endDateDescribedBy"]')
        e_date.clear()
        e_date.send_keys(end_date)

        time.sleep(2)
        next_btn = self.find_element(By.ID , 'nextBtn')
        next_btn.click()
        
    def check_availability(self):
        time.sleep(10)
        cond = True
        while cond:
            #Try to find the more sites button
            #If we didn't find it scroll down and try again
            try:
                more_sites_btn = self.find_element(By.ID , 'showMoreBtn')
                more_sites_btn.click()
                cond = False
            except:
                time.sleep(3)
                self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        time.sleep(30)

        #View all dates
        scroller = self.find_element(By.CSS_SELECTOR,'div[class*="mainContainer"]')
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);" , scroller)
        
        data =[]
        
        dates = self.find_elements(By.CSS_SELECTOR,'div[class$="marginBottom"]')
        for date in dates:
            location = date.find_element(By.CLASS_NAME,'small').get_attribute('innerHTML')
            
            #clean
            location = location.replace(
                '<strong _ngcontent-c','').replace('11','').replace('=""','').replace('>','')
            
            location = location.replace(""",
                        """,'').replace("""
                      """,'').replace('</strong','').replace('<span _ngcontent-c','').replace(
                '8','').replace('class="text-muted"','').replace('SAU','').replace('</span','').strip()
            

            days = date.find_elements(By.CSS_SELECTOR,'div[class$="card-default"]')

            for day in days:
                month = day.find_element(By.CSS_SELECTOR,'div[class$="month"]').find_element(By.CSS_SELECTOR,'div').get_attribute('innerHTML').strip()
                day_number = day.find_element(By.CLASS_NAME,'testCenterDay').find_element(By.CSS_SELECTOR,'strong').get_attribute('innerHTML').strip()
    
                
                data.append([location , month, day_number])
                '''day.click()
                            
                    

                #wait till time appear
                time.sleep(3)
                
                test_time = date.find_element(By.CSS_SELECTOR,'div[class$=testcenterTimeDate]').get_attribute(
                    'innerHTML')
                #clean 
                test_time = test_time.strip().replace('''
        ''',' ')'''
        
        self.filter_data(data=data)

    def filter_data(self , data : list):
        #remove old data
        for d in self.data:
            if not data.__contains__(d):
                self.data.remove(d)

        #update data 
        for d in data:
            if not self.data.__contains__(d):
                #send mail about a new appointment had been available
                mail = Email("Sender Email for notfication","Receiver Email for notfication","Email code")
                mail.send_mail(f"{d[1]}-{d[2]}",f"Location: {d[0]}\nDate: {d[1]}-{d[2]}")
                self.data.append(d)
        
            


    def refresh_page(self):
        self.refresh()


    #context protocole
    def __enter__(self):
        return self
    
    def __exit__(self,exc_type,exc_value,exc_traceback):
        if self.tearDown:
            self.close()
            self.quit()

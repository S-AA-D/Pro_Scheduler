from checking.checker import Checker
import time

with Checker() as bot:
    bot.land_first_page()
    count =0
    while True:
        time.sleep(15)
        try:
            bot.go_to_Exam()
            bot.location_and_date()
            bot.check_availability()
            
        except:
            bot.refresh()
            print(f'Exception {count} Hit!!')
            count+=1
    
       
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select
from selenium import webdriver
import datetime
import calendar
import time

def findDay(date):
    #convert month_number into month_name
    born = datetime.datetime.strptime(date, '%d %m %Y').weekday()
    return (calendar.day_name[born])

def xpath_string():
    #input value
    date_input_room = input("Room: ")
    date_input_hour = input("Hour: ")
    date_input_day = input("Day: ")
    date_input_month = input("Month: ")
    date_input_year = input("Year: ")
    date_input = (date_input_day+' '+date_input_month+' '+ date_input_year)
    week_day = findDay(date_input)
    month_name = calendar.month_name[int(date_input_month)]

    #concatenate values into complete xpath string
    x_path = ("//a[@title='"+date_input_hour+" "+week_day+", "\
    +month_name+" "+date_input_day+", "+date_input_year+" - "\
    +date_input_room+" - Main Library']")
    return x_path, date_input_day, date_input_month, date_input_year

def select_longest_time(driver):
    select = Select(driver.find_element_by_name('bookingend_1'))
    select.select_by_index(7)

def submit(driver):
    submit = driver.find_element_by_name('submit_times')
    submit.click()

def login(driver):
    #Username and password
    print("The library requires your net_id account in order to\n\
    reserve the room\n")
    net_id = input('Your net_id: ')
    net_id_position = driver.find_element_by_name('username')
    net_id_position.send_keys(net_id)
    password = input('Your password: ')
    password_position = driver.find_element_by_name('password')
    password_position.send_keys(password)

    #Submit
    submit = driver.find_element_by_name('submit').click()

def is_confirm(driver):
    reserve = driver.title
    while reserve != "Confirm your reservation details - University of Arizona Libraries - University of Arizona Libraries":
        time.sleep(1)
        reserve = driver.title
    return True

def locate_input_day(driver, input_day):
    button = driver.find_element_by_xpath('//button[@type="button"]')
    button.click()
    input_day_xpath = '//td[contains(text(), '+input_day+') and @class="day"]'
    choose_day = driver.find_element_by_xpath(input_day_xpath).click()

def main():
    #open library website
    driver = webdriver.Firefox()
    url = "https://libcal.library.arizona.edu/spaces?lid=801&gid=1394"
    driver.get(url)
    x_path, input_day, input_month, input_year = xpath_string()
    #retrieve, locate and click on the desired room
    times = 0
    locate_input_day(driver, input_day)
    time.sleep(2)
    while times < 6:
        x_path_click = driver.find_element_by_xpath(x_path).click()
        select_longest_time(driver)
        submit(driver)
        time.sleep(2)
        #check login
        login_title = driver.title
        if login_title == "CAS – Central Authentication Service":
            login(driver)
        #confirm reserve
        if is_confirm(driver) == True:
            reserve_submit = driver.find_element_by_xpath("//button[@type='submit']")
            reserve_submit.click()
        times += 1
        if times >= 1:
            driver.get(url)
            locate_input_day(driver, str(int(input_day)+times))
            #replace day
            x_path = x_path.replace(str(int(input_day)+times-1), str(int(input_day)+times))
            #replace day_week
            x_path = x_path.replace(findDay(str(int(input_day)+times-1)+' '+input_month+' '+input_year),
            findDay(str(int(input_day)+times)+' '+input_month+' '+input_year))
            time.sleep(2)

main()

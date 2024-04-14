import time 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from util.json_to_object import json_to_employee
from src.web_crawling_company import conversation 

def main():
    # Lựa chọn trình duyệt (ví dụ: Chrome)
    driver = webdriver.Edge()

    # Truy cập URL
    url = "https://www.linkedin.com/feed/"
    driver.get(url)

    # Chờ cho trang tải hoàn tất
    driver.implicitly_wait(10)
    driver.maximize_window()

    # login
    username_input_box = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "username")))
    username_input_box.clear()
    username_input_box.send_keys("1194030275.dnu@gmail.com")
    pw_element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "password")))
    pw_element.clear()
    pw_element.send_keys("Th@i1234!@#$", Keys.ENTER)

    time.sleep(2)

    # search for given topic
    search_bar = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[@id='global-nav-typeahead']/input")))
    search_bar.clear()
    search_bar.send_keys("fpt", Keys.ENTER)

    time.sleep(2)

    # click filter companies
    companies_filter = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='search-reusables__filters-bar']/ul/li[3]/button")))
    companies_filter.click()

    # click filter first option
    first_com = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[1]")))
    first_com.click()

    # click to employee
    employees = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[1]/section/div/div[2]/div[2]/div[1]/div[2]/div/div/div[2]/a")))
    employees.click()

    # list elements
    list_of_emp = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul")))

    html_str_of_list_of_emp = list_of_emp.get_attribute('innerHTML')


    conversation.send_message('''instructions = Your knowledge is get the data from a code HTML, change its HTML code into JSON format.
    So based on the HTML tag <a> please get the name of all employees and the employees link in href attribute
    Answer must be structured like this:
    [{
        "name": "$employee_name",
        "profile": "$employee_link"
    }]
    Please do that according to html code here:
    ''' + html_str_of_list_of_emp)

    employees = json_to_employee(conversation.last.text)

    for em in employees:
        print(f"name: {em.name} === profile: {em.profile}")

    # Đóng trình duyệt
    driver.quit()

    # def check_if_is_user():
        

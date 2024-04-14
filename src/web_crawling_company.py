import google.generativeai as genai
import os
import time 
import json
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from database_orm import TalentPool

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
driver = webdriver.Chrome()

class MeetAlfredTalentPool:

    def crawling_company():
        page = 1
        while page <= 100:
            url = f"https://www.linkedin.com/search/results/companies/?companyHqGeo=%5B%22104195383%22%5D&keywords=construction&origin=FACETED_SEARCH&page={page}&sid=Np2"
            page += 1
        driver.get(url)

        driver.implicitly_wait(10)
        driver.maximize_window()

        username_input_box = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "username")))
        username_input_box.clear()
        username_input_box.send_keys("nguyenletuyen9201@gmail.com")
        pw_element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "password")))
        pw_element.clear()
        pw_element.send_keys("", Keys.ENTER)

        time.sleep(2)

        # get list company
        company_list = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul")))
        company_list_html = company_list.get_attribute("outerHTML")
        print(company_list_html)
        # print
        print("~~~~SENDING REQUEST TO GEMINI~~~~")

        driver.quit()
        return company_list_html


    def crawling_list_candidate():
        talent_pool = []
        url = "https://app.meetalfred.com/campaign/details/leads/686545?trial-user=true"

        driver.get(url)

        driver.implicitly_wait(10)
        driver.maximize_window()

        free_trial_button = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "/html/body/section/div[2]/div[3]/div[2]/a")))
        free_trial_button.click()

        login_button = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[1]/a[2]")))
        login_button.click()

        email_input = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.NAME, "email")))
        email_input.clear()
        email_input.send_keys("tnguyenl@gsi-software.com")

        password_input = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.NAME, "password")))
        password_input.clear()
        password_input.send_keys("09022001", Keys.ENTER)

        activity_button = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div[1]/span/p/a/span/button")))
        activity_button.click()

        paging_button = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[3]/div[2]/div/div/div[2]/div")))
        paging_button.click()

        number_button = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[3]/ul/li[6]")))
        number_button.click()

        employee_table = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
        employee_data = employee_table.find_elements(By.TAG_NAME, "tr")
        for employee in employee_data[:2]:
            employee.click()

            name_talent = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div[1]/div[1]/a")))
            talent_linkedin = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div[1]/div[2]/div[1]/div[2]/p[2]/span/p/a")))
            position = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div[1]/div[1]/p")))

            talent_pool.append({
                "name_talent": name_talent.get_attribute("outerHTML"),
                "talent_linkedin": talent_linkedin.get_attribute("outerHTML"),
                "position": position.get_attribute("outerHTML")
            })

            close_button = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div[3]/span/button")))
            close_button.click()

        # employee_list_html = employee_data.get_attribute("outerHTML")

        time.sleep(2)

        driver.quit()
        return talent_pool


    def generate_json_linkined(company_list_html):
        generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048     
        }

        safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
        ]

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        conversation = model.start_chat(history=[
        # {
        #     "role": "user",
        #     "parts": ["aaa"]
        # },
        # {
        #     "role": "model",
        #     "parts": ["**Artificial Intelligence: The Transformative "]
        # }
        ])

        conversation.send_message('''instructions = Your knowledge is get the data from a code HTML, change its HTML code into JSON format.
        So based on the HTML tag <a> please get the name of compnay and the company link in href attribute
        Answer must be structured like this:
        [{
        "company_name": "$company_name",
        "company_link": "$company_link"                  
        }]
        Please do that according to html code here:
                                
        ''' + str(company_list_html))
        print("GEMINI:", conversation.last.text)


    def generate_json_employee(company_list_html):
        generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048     
        }

        safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
        ]

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        conversation = model.start_chat(history=[
        # {
        #     "role": "user",
        #     "parts": ["aaa"]
        # },
        # {
        #     "role": "model",
        #     "parts": ["**Artificial Intelligence: The Transformative "]
        # }
        ])

        conversation.send_message('''instructions = Your knowledge is get the data from a code HTML, drop HTML code and get only the data in HTML code. Return to me as JSON fomat.
        So based on the HTML tag <tr> please get the name of talent and the link of linkedin in href attribute and , based on the HTML tag <p> please get the position of talent.
        Answer must contain only structured like this:
        [{
        "fullname": "$fullname",
        "linkedin_path": "$linkedin_path",
        "position": $position                  
        }]
        Please do that according to html code here:
                                
        ''' + str(company_list_html))
        print("GEMINI:", conversation.last.text)
        return conversation.last.text


def main():
    employee_list_html = MeetAlfredTalentPool.crawling_list_candidate()
    print(employee_list_html)
    talent_pool = MeetAlfredTalentPool.generate_json_employee(employee_list_html)
    talent_pool = json.loads(talent_pool)
    for talent in talent_pool:
        TalentPool.instert_talent_pool(talent)
    get_talent_pool()


def get_talent_pool():
    talent_pool = TalentPool.select_talent_pool()
    print("talent_pool",talent_pool)

main()

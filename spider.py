import time
import csv
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# chromedriver will execute the program on our behalf
DRIVER_PATH = "/Users/xavier/Desktop/chromedriver 2"
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

# toronto district school board numbers are fed into the script here
idsFile = open("txt/toronto_school_ids.txt", "r")
ids = idsFile.read().splitlines()
idsFile.close()
# the years for which we want data
yearsFile = open("txt/years.txt", "r")
years = yearsFile.read().splitlines()
yearsFile.close()

print("Let's collect some data from the Ontario class size tracker!")
time.sleep(5)
print("Stand-by...")

# our spider will crawl from website to website collecting the data we need with the help of selenium
with open('data.csv', 'w', newline='') as csvfile:
    for i in range (0, len(ids)):
        school_id = ids[i]
        driver.get("https://www.app.edu.gov.on.ca/eng/cst/classSize2.asp?sch_no=" + school_id)
        time.sleep(5)

        name=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#right_column > h2"))).text
        print("School we are currently collecting data for: " + name)
        time.sleep(5)

        for j in range (0, len(years)):
            dropdown = Select(driver.find_element_by_name("schYR"))
            dropdown.select_by_value(years[j])
            search_button = driver.find_element_by_id("frmYearsSubmit")
            search_button.click()
            print("Collecting data for the year: " + years[j])
            table= WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "td > table")))
            time.sleep(5)

            # once we have made it to the website we want to scraper, we initiate python's csv writerow() function
            wr = csv.writer(csvfile)
            for row in table.find_elements_by_css_selector('tr'):
                wr.writerow(
                [ids[i]] +
                [name] +
                [years[j]] +
                [d.text for d in row.find_elements_by_css_selector('td')])

            time.sleep(5)

        driver.back()
    csvfile.close()

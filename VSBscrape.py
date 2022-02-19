from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
import smtplib


# Author: Simon Georgiades
# Date: 01/01/2022
# Pass in the term (in the format example: "Winter 2022"), the subject in capital letters (e.g.: MECH),
# and the course number (e.g.: "309")

def seatsavailability(t, s, c, e):
    term = t
    subject = s
    course = c
    email_input = e

    # Setting driver. To download geckodriver: https://github.com/mozilla/geckodriver/releases

    s = Service('/Users/georg/Documents/geckodriver')
    driver = webdriver.Firefox(service=s)

    # Setting URL and opening webpage

    url = "https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin"
    driver.get(url)

    # Finding username and password input field and login in

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="UserID"]')))

    username = driver.find_element(By.XPATH, '//*[@id="UserID"]')
    username.clear()
    username.send_keys('260929323')

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="PIN"]')))

    password = driver.find_element(By.XPATH, '//*[@id="PIN"]')
    password.clear()
    password.send_keys('sg7413')

    # Click login button

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mcg_id_submit"]')))
    driver.find_element(By.XPATH, '//*[@id="mcg_id_submit"]').click()

    # Click "Student Menu". There's a point before the XPATH because we're not at the initial URL

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, './html/body/div[3]/table[1]/tbody/tr[2]/td[2]/a')))
    driver.find_element(By.XPATH, './html/body/div[3]/table[1]/tbody/tr[2]/td[2]/a').click()

    # Click "Registration Menu"

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, './html/body/div[3]/table[1]/tbody/tr[2]/td[2]/a')))
    driver.find_element(By.XPATH, './html/body/div[3]/table[1]/tbody/tr[2]/td[2]/a').click()

    # Click "Step 2"

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, './html/body/div[3]/table[1]/tbody/tr[2]/td[2]/a')))
    driver.find_element(By.XPATH, './html/body/div[3]/table[1]/tbody/tr[2]/td[2]/a').click()

    # Select the term

    select = Select(WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, './html/body/div[3]/form/table/tbody/tr/td/select'))))
    select.select_by_visible_text(term)
    driver.find_element(By.XPATH, './html/body/div[3]/form/input[3]').click()

    # Selecting the subject

    select = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, './/*[@id="subj_id"]'))))
    select.select_by_value(subject)
    driver.find_element(By.XPATH, './html/body/div[3]/form/input[17]').click()

    # Selecting the class

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, './html/body/div[3]/table[2]/tbody/tr')))

    column1 = driver.find_elements(By.XPATH, './html/body/div[3]/table[2]/tbody/tr/td[1]')

    j = 0

    for i in column1:
        num = j + 3
        link = './html/body/div[3]/table[2]/tbody/tr[' + str(num) + ']/td[3]/form/input[30]'
        if i.text == course:
            driver.find_element(By.XPATH, link).click()
            break

        j += 1

    # Checking the seats for each row

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, './html/body/div[3]/form/table')))
    column_type = driver.find_elements(By.XPATH, './html/body/div[3]/form/table/tbody/tr/td[6]')
    column_seats = driver.find_elements(By.XPATH, './html/body/div[3]/form/table/tbody/tr/td[13]')

    num_of_rows = len(column_seats)

    # If the course is a lecture and there are seats available, do this

    availability = False

    for i in range(num_of_rows):
        if column_type[i].text == "Lecture" and int(column_seats[i].text) > 0:
            print(subject, course, "has", int(column_seats[i].text), "seats available")
            availability = True

        else:
            continue

    # Send an email if there is availability

    if availability == True:
        # Setting up emails and message to be sent
        sender_email = "mcgillcoursesnotifier@gmail.com"
        rec_email = email_input
        password = "heleneetphilippe"
        msg = subject + course + " has seats available"

        # Connecting to server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        print("Login success")

        # Sending email
        server.sendmail(sender_email, rec_email, msg)
        print("Email sent")


    else:
        print("No place available")

    driver.close()

import os

from socket import *

from selenium import webdriver
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from secrets import pw

import schedule
import time


def track_price():
    driver = webdriver.Chrome()
    driver.get("https://projects.thecity.nyc/2020_03_covid-19-tracker/")
    driver.execute_script("window.scrollTo(0, 600)")
    time.sleep(3)
    driver.save_screenshot('NYC_COVID19_Tracker.png')
    tested = driver.find_element_by_xpath('/html/body/main/article/div[2]/div[1]/div[1]').text
    confirmed = driver.find_element_by_xpath('/html/body/main/article/div[2]/div[1]/div[2]').text
    death = driver.find_element_by_xpath('/html/body/main/article/div[2]/div[1]/div[3]').text

    text = f"NYC Tested Cases: {tested}\n" \
           f"NYC Confirmed Cases: {confirmed}\n" \
           f"NYC Death Toll {death}"

    send_email(text)

    driver.close()


def send_email(m):
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("andrevb46@gmail.com", pw)

    try:
        mail = smtplib.SMTP('smtp.gmail.com')
    except:
        mail = smtplib.SMTP('smtp.gmail.com')

    msg = MIMEMultipart()  # create a message

    f = open("NYC_COVID19_Tracker.png", 'rb')
    image = MIMEImage(f.read())
    image.add_header('Content-Disposition', "NYC_COVID19_Tracker")
    f.close()
    msg.attach(image)

    # setup the parameters of the message

    recipients = ["renadhc057@gmail.com", "nomaan8268@gmail.com", "cmaheeb@gmail.com"]
    msg['From'] = "andrevb46@gmail.com"
    msg['To'] = ",".join(recipients)
    msg['Subject'] = "NYC COVID19 Tracker"
    # add in the message body
    msg.attach(MIMEText(m, 'plain'))
    # send the message via the server set up earlier.
    s.send_message(msg)

    s.quit()


track_price()

# schedule.every(2).minutes.do(track_price)
#
# while 1:
#     schedule.run_pending()
#     time.sleep(1)

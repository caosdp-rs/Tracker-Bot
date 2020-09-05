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
    driver.get("https://www.futbin.com/20/player/45369/Jonathan%20Ikon%C3%A9")
    driver.save_screenshot('PlayerImage.png')
    price = driver.find_element_by_xpath('//*[@id="ps-lowest-1"]').text
    print(price)

    #Convert price data type from string to float
    pr = price.replace(',', "") # '470,000' ---> '470000'
    num_price = float(pr) #float('470000') ---> 470000.00

    if num_price < 300000.00:
        text = f"Price went DOWN below 300k. Current FUTBIN price : {price} "
        send_email(text)

    # elif num_price > 790000.00:
    #     text = f"Price went UP above 780k. Current FUTBIN price : {price} "
    #     send_email(text)

    else:
        text = f"Current FUTBIN price : {price} "
        send_email(text)

    driver.close()


def send_email(m):
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("andrevb46@gmail.com", pw)

    msg = MIMEMultipart()  # create a message

    f = open("PlayerImage.png", 'rb')
    image = MIMEImage(f.read())
    # image.add_header('Content-Disposition', "Koeman88")
    f.close()
    msg.attach(image)

    # setup the parameters of the message

    recipients = "renadhc@gmail.com"
    msg['From'] = "andrevb46@gmail.com"
    msg['To'] = recipients
    msg['Subject'] = "Ikone Current Price"

    # add in the message body
    msg.attach(MIMEText(m, 'plain'))
    # send the message via the server set up earlier.
    s.send_message(msg)

    s.quit()


track_price()

schedule.every(10).minutes.do(track_price)

while 1:
    schedule.run_pending()
    time.sleep(1)

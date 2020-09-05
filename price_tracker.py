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
    driver.get("https://www.futbin.com/20/player/854/kylian-mbapp%C3%A9")
    driver.save_screenshot('PlayerImage.png')
    price = driver.find_element_by_xpath('//*[@id="ps-lowest-1"]').text
    print(price)

    # The bot heads over to the futbin player page, takes a screenshot, locates and retrieves the player price as text data.
    # Converts its data type from string to float. Performs a comparison check with the price point set by the user
    # Appends the image, price data, player info to an email and sends it to a list of the email addresses set by the user.
    # The automated script runs on a scheduler every X minutes. Time (X) is also set by the user.

    pr = price.replace(',', "")
    num_price = float(pr)

    if num_price > 40000.00:
        text = f"Price went ABOVE 40k. Current FUTBIN price : {price} "
        send_email(text)

    # elif num_price > 790000.00:
    #     text = f"Price went UP above 780k. Current FUTBIN price : {price} "
    #     send_email(text)

    # else:
    #     text = f"Current FUTBIN price : {price} "
    #     send_email(text)

    driver.close()


def send_email(m):
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.ehlo()
    s.starttls()
    s.login("andrevb46@gmail.com", pw)

    try:
        mail = smtplib.SMTP('smtp.gmail.com')
    except:
        mail = smtplib.SMTP('smtp.gmail.com')

    msg = MIMEMultipart()  # create a message

    f = open("PlayerImage.png", 'rb')
    image = MIMEImage(f.read())
    # image.add_header('Content-Disposition', "Koeman88")
    f.close()
    msg.attach(image)

    # setup the parameters of the message
    from_add = "andrevb46@gmail.com"
    recipients = "renadhc@gmail.com"
    msg['From'] = from_add
    msg['To'] = recipients
    msg['Subject'] = "Kylian Mbappe Current Price"
    print(msg)
    # add in the message body
    msg.attach(MIMEText(m, 'plain'))
    # send the message via the server set up earlier.
    s.sendmail(from_addr=from_add, to_addrs=recipients, msg=msg.as_string())

    s.quit()


track_price()

schedule.every(1).minutes.do(track_price)

while 1:
    schedule.run_pending()
    time.sleep(1)

import requests
from bs4 import BeautifulSoup
import smtplib
import time
import socket

# Function to get user input for sensitive information
def get_user_input(prompt):
    return input(prompt).strip()

# Get user input for URL
URL = get_user_input("Enter the Amazon product URL: ")

# Get user input for User-Agent header
user_agent = get_user_input("Enter your User-Agent (optional, press Enter to use default): ")
headers = {"User-Agent": user_agent} if user_agent else {}

# Get user input for email credentials
email_sender = get_user_input("Enter your email address: ")
email_password = get_user_input("Enter your email password: ")
email_receiver = get_user_input("Enter the recipient's email address: ")

# Set up the SMTP server
smtp_server = get_user_input("Enter your SMTP server (e.g., smtp.google.com): ")
smtp_port = int(get_user_input("Enter the SMTP port (e.g., 587): "))

# Set up the email message
subject = 'Price fell down!'
body = f'Check the following Amazon link: {URL}'
msg = f"Subject: {subject}\n\n{body}"

# Function to check the price and send email
def check_price():
    page = requests.get(URL, headers=headers)
    soup1 = BeautifulSoup(page.content, 'html.parser')
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    title = soup2.find(id="productTitle").get_text().strip()
    price = soup2.find(id="priceblock_ourprice").get_text()
    converted_price = float(price[1:4])

    if converted_price < 1000:
        send_email()

    print(price)
    print(title)

# Function to send email
def send_email():
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(email_sender, email_password)
    server.sendmail(email_sender, email_receiver, msg)
    server.quit()
    print("Email has been sent")

check_price()

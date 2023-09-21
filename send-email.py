#!/usr/bin/python3
#
# Author: Dung Pham
# Site: https://devopslite.com
# Use: this script used to send an email to a list of mail addresses with a html template
#########################################################################################

import smtplib
import ssl
import re
import configparser
import logging
from email.mime.text import MIMEText

def validate_email(email):
    # Regular expression to validate email address
    pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
    return re.match(pattern, email)

def get_config():
    # Read config.ini and return the SMTP configurations
    logging.info('Reading SMTP configurations from config.ini')
    config = configparser.ConfigParser()
    config.read('config.ini')

    try:
        config.get('SMTP', 'host')
        config.get('SMTP', 'port')
        config.get('SMTP', 'username')
        config.get('SMTP', 'password')
        config.get('SMTP', 'sender')
        config.get('SMTP', 'sender_name')
    except:
        logging.error("error in reading config.ini")
        return None

    logging.info('Finished reading SMTP configurations')
    return config['SMTP']

def get_email_list():
    # Read emails.txt and return a list of valid email addresses
    with open('emails.txt', 'r') as f:
        emails = f.readlines()
    valid_emails = [email.strip() for email in emails if validate_email(email)]
    return valid_emails

def send_email(to, subject, message, config):
    # Send email with HTML message to the specified recipient
    context = ssl.create_default_context()
    try:
        if config['port'] in ['587']:
            server = smtplib.SMTP(config['host'], config['port'])
            server.ehlo()
            server.starttls(context=context)
        elif config['port'] in ['465']:
            server = smtplib.SMTP_SSL(config['host'], config['port'])
        else:
            server = smtplib.SMTP(config['host'], config['port'])
            
        server.ehlo()
        server.login(config['username'], config['password'])

        msg = MIMEText(message, 'html')
        msg['Subject'] = subject
        msg['To'] = to
        msg['From'] = f"{config['sender_name']} <{config['sender']}>"

        server.send_message(msg)
        server.close()
        logging.info(f"Email sent to {to}")
    except Exception as e:
        logging.error(f"Failed to send email to {to}: {e}")

def read_message_html():
    # Read HTML message from message.html file
    with open("message.html", "r") as f:
        return f.read()

def main():
    # Set up logging
    logging.basicConfig(filename='email.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')
    logging.info("Start sending email")

    # Get SMTP configurations and valid email list
    config = get_config()
    to_list = get_email_list()

    # Subject
    subject = "Sample email from Python3"

    # Read HTML message
    message = read_message_html()

    # Send email to each recipient
    for to in to_list:
        send_email(to, subject, message, config)

    logging.info("Finished sending email")

if __name__ == "__main__":
    main()

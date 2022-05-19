#!/usr/bin/python3
#
# Author: Dung Pham
# Site: https://devopslite.com
# Use: this script use to send an email to a list of mail address with a html template
######################################################################################

## Import libs
# Lib to read smtp values
import configparser
# Lib to remove blank lines
#import sys
# Lib to validate email addresses
import re
# Lib to send emails with smtp server
import smtplib

## Read the SMTP configuration
def configSmtp():
    config = configparser.ConfigParser()
    config.read('config.cfg')

    smtpHost = config.get('smtp', 'SMTP_HOST')
    smtpUser = config.get('smtp', 'SMTP_USER')
    smtpPass = config.get('smtp', 'SMTP_PASS')
    smtpPort = config.get('smtp', 'SMTP_PORT')
    smtpAuth = config.get('smtp', 'SMTP_AUTH')
    smtpStartTls = config.get('smtp', 'SMTP_STARTTLS')

## Remove all blank lines in the email list
def removeBlankLine():
    # Clear the file email-list.out
    open("email-list.out", "w").close()

    with open('email-list.in', 'r') as inputMailList:
        with open('email-list.out', 'w') as outputMailList:
            for line in inputMailList:
                if not re.match(r'^\s*$', line):
                    outputMailList.write(line)
    
    with open('email-list.out') as outputList:
        for line in outputList.readlines():
            line.rstrip('\n')

## Validate email address
def validateEmailAddress(emailAddress):
    # Make a regular expression for validating an email address
    regex = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'

    if(re.fullmatch(regex, emailAddress)):
        print(emailAddress, 'is valid email address!')
    else:
        print(emailAddress, 'is invalid email address!')

## Send emails
def sendEmails():
    with open('email-list.out', 'r') as mailList:
        for email in mailList:
            validateEmailAddress(email)


## Execute the functions
#configSmtp()
removeBlankLine()
sendEmails()
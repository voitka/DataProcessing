#This script generates separate emails for each file in the provided folder
#

import email_functions as mail
from os import listdir as listdir
import win32com.client as win32


def Emailer(text, subject, to_email, cc_email, attachment):

    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = to_email
    mail.CC = cc_email
    mail.Subject = subject
    mail.HtmlBody = text

    mail.Attachments.Add(attachment)
    mail.Display(True)

def CreateEmails(text, subject, to_email, cc_email, path_to_attachments)

    attacments = listdir(path_to_attachments)

    for f in files:
        print(f)
        attacment = path_to_attachments + f
        print(attacment)
        mail.Emailer(text, subject, to_email, cc_email, attacment)


def main():
    subject = 'Email subject'
    text = 'Hello, email text is here.'
    path_to_directory = 'attachments/'
    to_email = 'olga.voitka@gmail.com'
    cc_email = 'olga.voitka@gmail.com'    
    
    CreateEmails(text, subject, to_email, cc_email, path_to_directory)


if __name__ == "__main__":
    main()

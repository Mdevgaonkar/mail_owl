import email
import imaplib
import smtplib
import datetime
import email.mime.multipart
import config
import base64


class mail_owl():
    def __init__(self):
        mydate = datetime.datetime.now()-datetime.timedelta(1)
        self.today = mydate.strftime("%d-%b-%Y")

    
    
   
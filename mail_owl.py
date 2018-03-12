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

    def login(self, username, password):
        self.username = username
        self.password = password
        while True:
            try:
                self.imap = imaplib.IMAP4_SSL(config.imap_server,config.imap_port)
                r, d = self.imap.login(username, password)
                assert r == 'OK', 'login failed'
                print(" > Sign as ", d)
            except:
                print(" > Sign In ...")
                continue
            break
    
    def list(self):
        # self.login()
        return self.imap.list()

    def select(self, str):
        return self.imap.select(str)

    def inbox(self):
        return self.imap.select("Inbox")

    def logout(self):
        return self.imap.logout()

    def unreadIds(self):
        r, d = self.imap.search(None, "UNSEEN")
        list = d[0].decode("utf-8").split(' ')
        return list

    def hasUnread(self):
        list = self.unreadIds()
        return list != ['']

    def unreadCnt(self):
        list = self.unreadIds()
        return len(list)
    
    def latestUnread(self):
        list = self.unreadIds()
        latest_id = list[-1]
        return self.getEmail(str(latest_id))
    
    def getEmail(self, id):
        r, d = self.imap.fetch(id, "(RFC822)")
        self.raw_email = d[0][1].decode("utf-8")
        self.email_message = email.message_from_string(self.raw_email)
        return self.email_message
    def getMailbody(self, email_message):
        if email_message.is_multipart():
            for payload in email_message.get_payload():
                # if payload.is_multipart(): ...
                body = (
                    payload.get_payload()
                    .split(email_message['from'])[0]
                    .split('\r\n\r\n2015')[0]
                )
                return body
        else:
            body = (
                email_message.get_payload()
                .split(email_message['from'])[0]
                .split('\r\n\r\n2015')[0]
            )
            return body

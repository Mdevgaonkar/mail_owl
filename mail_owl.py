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

    def getMailsubject(self, email_message):
        return email_message['Subject']
    
    def getMailfrom(self, email_message):
        return email_message['from']

    def getMailto(self, email_message):
        return email_message['to']

    def mailreturnpath(self, email_message):
        return email_message['Return-Path']

    def mailreplyto(self, email_message):
        return email_message['Reply-To']

    def mailall(self, email_message):
        return email_message

    def mailbodydecoded(self, email_message):
        return base64.urlsafe_b64decode(self.getMailbody(email_message))

    def sendEmailMIME(self, recipient, subject, message):
        msg = email.mime.multipart.MIMEMultipart()
        msg['to'] = recipient
        msg['from'] = self.username
        msg['subject'] = subject
        msg.add_header('reply-to', self.username)
        # headers = "\r\n".join(["from: " + "sms@kitaklik.com","subject: " + subject,"to: " + recipient,"mime-version: 1.0","content-type: text/html"])
        # content = headers + "\r\n\r\n" + message
        try:
            self.smtp = smtplib.SMTP(config.smtp_server, config.smtp_port)
            self.smtp.ehlo()
            self.smtp.starttls()
            self.smtp.login(self.username, self.password)
            self.smtp.sendmail(msg['from'], [msg['to']], msg.as_string())
            print("   email replied")
        except smtplib.SMTPException:
            print("Error: unable to send email")

    def sendEmail(self, recipient, subject, message):
        headers = "\r\n".join([
            "from: " + self.username,
            "subject: " + subject,
            "to: " + recipient,
            "mime-version: 1.0",
            "content-type: text/html"
        ])
        content = headers + "\r\n\r\n" + message
        while True:
            try:
                self.smtp = smtplib.SMTP(config.smtp_server, config.smtp_port)
                self.smtp.ehlo()
                self.smtp.starttls()
                self.smtp.login(self.username, self.password)
                self.smtp.sendmail(self.username, recipient, content)
                print("   email replied")
            except:
                print("   Sending email...")
                continue
            break

    def readIdsToday(self):
        r, d = self.imap.search(None, '(SINCE "'+self.today+'")', 'SEEN')
        list = d[0].decode("utf-8").split(' ')
        return list

    def readToday(self):
        list = self.readIdsToday()
        latest_id = list[-1]
        return self.getEmail(str(latest_id))
    
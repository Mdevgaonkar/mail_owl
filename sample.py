import mail_owl
import config

mail = mail_owl.mail_owl()
mail.login(config.email_id ,config.password)

mail.select('testingfolder')
# #to select inbox use inbox function directly
# mail.inbox() 

if mail.hasUnread() :
    unreadCnt = mail.unreadCnt()
    print("You have %d unread messages" % unreadCnt)
    message = mail.latestUnread() #gets latest unread mail
    # print(message)
    mailFrom = mail.getMailfrom(message)
    mailTo = mail.getMailto(message)
    mailSubject = mail.getMailsubject(message)
    mailbody = mail.getMailbody(message)
    print('From : %s' % mailFrom)
    print('To : %s' % mailTo)
    print('Subject : %s' % mailSubject)
    print('\n %s' % mailbody)
else:
    print('No unread messages for now')

mail.logout()
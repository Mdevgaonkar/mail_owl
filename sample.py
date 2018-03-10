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
else:
    print('No unread messages for now')

mail.logout()
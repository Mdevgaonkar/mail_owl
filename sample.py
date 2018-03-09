import mail_owl
import config

mail = mail_owl.mail_owl()
mail.login(config.email_id ,config.password)

mail.select('testingfolder')
# #to select inbox use inbox function directly
# mail.inbox() 

mail.logout()
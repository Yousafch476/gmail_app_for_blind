import imaplib
import email
m = imaplib.IMAP4_SSL("imap.gmail.com", 993)
m.login("offical078630@gmail.com","zfrcdvnrylhomusd")
action ='inbox'
m.select('"[Gmail]/'+action+'"')
result, data = m.uid('search', 'To') # search all email and return uids
result, data = m.uid('search', 'From') # search all email and return uids
if result == 'OK':
    for num in data[0].split():
        result, data = m.uid('fetch', '(RFC822)')
        if result == 'OK':
            email_message = email.message_from_bytes(data[0][1])    # raw email text including headers
            obj={'From':email_message['From'],'To':email_message['To'],'Subject':email_message['Subject']}

m.close()
m.logout()
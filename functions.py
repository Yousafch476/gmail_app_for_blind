from cgitb import html
import html
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import imaplib
import email
from email.header import decode_header
def sqlInjectSenitize(val):
    val = val.replace("'","").replace('"',"")
    return val

def escapHTML(val):
    val=html.escape(val)
    return val


def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

def userExist(username):
    try:
        user=User.objects.get(username=username,is_active=True)
      
    except User.DoesNotExist:
        user=None
    return user







def FetchMail(From_email,From_pwd,action):
    res=[]
    try:
        m = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        m.login(From_email,From_pwd)
        if action =='inbox':
            m.select('"'+action+'"')
        else:
            m.select('"[Gmail]/'+action+'"')

        result, data = m.uid('search', None, "ALL") # search all email and return uids
        if result == 'OK':
            for num in data[0].split():
                result, data = m.uid('fetch', num, '(RFC822)')
                if result == 'OK':
                    email_message = email.message_from_bytes(data[0][1])    # raw email text including headers
                    obj={'From':email_message['From'],'To':email_message['To'],'Subject':email_message['Subject']}
                    res.append(obj)
    except:
        res=None
    m.close()
    m.logout()
    return res


def SearchMail(From_email,From_pwd,action,em):
    res=[]
    m = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    m.login(From_email,From_pwd)
    if action =='inbox':
        m.select('"'+action+'"')
    else:
        m.select('"[Gmail]/'+action+'"')
    if action=='Sent Mail':
        result, data = m.uid('search', 'To',em) # search all email and return uids
    else:
        result, data = m.uid('search', 'From',em) # search all email and return uids
    if result == 'OK':
        for num in data[0].split():
            result, data = m.uid('fetch', num, '(RFC822)')
            if result == 'OK':
                email_message = email.message_from_bytes(data[0][1])    # raw email text including headers
                obj={'From':email_message['From'],'To':email_message['To'],'Subject':email_message['Subject']}
                res.append(obj)
    
    m.close()
    m.logout()
    return res


def fetchLatest(From_email,From_pwd,action):
    # establish connection with Gmail
    server ="imap.gmail.com"					
    imap = imaplib.IMAP4_SSL(server)
    data=[]
    # intantiate the username and the password
    username =From_email
    password =From_pwd

    # login into the gmail account
    imap.login(username, password)			

    # select the e-mails
    if action == 'inbox':
        res, messages = imap.select('"'+action+'"')
    else:
        res, messages = imap.select('"[Gmail]/'+action+'"')

    # calculates the total number of sent messages
    messages = int(messages[0])
    n=3
    if messages < n:
        n = messages
    print(n)
# iterating over the e-mails
    for i in range(messages, messages - n, -1):
        res, msg = imap.fetch(str(i), "(RFC822)")	
        for response in msg:
            if isinstance(response, tuple):

                msg = email.message_from_bytes(response[1])
                From = msg["From"]
                subject = msg["Subject"]
                To = msg["To"]

                obj={'From':From,'To':To,'Subject':subject}
                data.append(obj)
    return data
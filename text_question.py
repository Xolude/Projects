import smtplib, imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email, time

user = "your_email"  #Make sure you have POP enabled for external apps with google, as well as having IMAP enabled
pas = "your_password"
phonenumber = "4068905642" #Don't forget area code
sms_gateway = (str(phonenumber) + "@vtext.com") #Change suffix "@vtext" to your corresponding provider
smtp = "smtp.gmail.com" 
imap = "imap.gmail.com"
port = 587

def send_msg(message):
    server = smtplib.SMTP(smtp,port) #Server initialization for whenever the message is sent
    server.starttls()
    server.login(user,pas)

    msg = MIMEMultipart()
    msg['From'] = user  #To and from
    msg['To'] = sms_gateway
    body = str(message)
    msg.attach(MIMEText(body, 'plain'))
    sms = msg.as_string()  #Combine message parts into a string
    server.sendmail(user,sms_gateway,sms)  #Send message from user through gateway
    server.quit()  #Stop server instance

def get_body(message):   #Extract body from email HTML
    if message.is_multipart():  
        return get_body(message.get_payload(0))
    else:
        return message.get_payload(None,True)

def search(key,value,con): #Search for messages from specific sender
    result, data = con.search(None,key,'"{}"'.format(value))
    return data

def fetch():  #Fetch and/or refresh any new incoming messages
    global con, result, data, raw
    con = imaplib.IMAP4_SSL(imap)
    con.login(user,pas)
    con.select('INBOX')
    result, data = con.fetch(b'3','(RFC822)')
    raw = email.message_from_bytes(data[0][1])

def get_emails(result_bytes): #Make a list of messages to be used by other functions
    msgs = []
    for num in result_bytes[0].split():
        typ, data = con.fetch(num,'(RFC822)')
        msgs.append(data)
    return msgs

def ask_question(question,ans1,ans2): #Sends question and awaits response, as well as responding based on user input when received
    responses = []
    response = ""
    answer = False
    send_msg(str(question))

    while answer == False:
        time.sleep(10)  #Wait a bit
        fetch()  #Refresh messages
        messages = get_emails(search('FROM',sms_gateway,con))   #Check messages \/
        for i in messages:
            responses.append(get_body(email.message_from_bytes(i[0][1])))
        if len(responses) > 0:
            response = responses[-1].decode("utf-8")  #Decode the body html giving you just text
            print(response)
        if str(ans1).lower() in response.lower():  #Compare response \/
            send_msg("Good choice!")
            answer = True
        elif str(ans2).lower() in response.lower():
            send_msg("That's no good")
            answer = False

ask_question("Test Question, Y/N?","Y","N")
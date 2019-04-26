import smtplib

# set up username and smtppassword as global variables
global smtpusername
smtpusername = None
global smtppassword
smtppassword = None

# read the username (e-mail address) and password from file
def readUsernamePassword() :
    file = open("username.txt", "r")
    line = file.readline()
    splitLine = line.split()
    global smtpusername
    smtpusername = splitLine[0]
    global smtppassword
    smtppassword = splitLine[1]

def sendMail(toAddresses: object, subject: object, body: object) -> object:
    fromAddress = 'webproprtiesmonitor@cellsignal.com'
    username = smtpusername
    password = smtppassword
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    msg = "\r\n".join([
        "From: " + fromAddress,
        "To: " + toAddresses,
        "Subject: " + subject,
        "",
        body
    ])

    server.sendmail(fromAddress, toAddresses, msg)
    server.quit()

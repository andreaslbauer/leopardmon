import smtplib

def sendMail(toAddresses: object, subject: object, body: object) -> object:
    fromAddress = 'webproprtiesmonitor@cellsignal.com'
    username = 'andreaslbauer@gmail.com'
    password = '384Robbi'
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

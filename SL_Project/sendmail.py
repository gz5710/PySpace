import smtplib


try:
    gmail_user = 'bruce.gong.tmax@gmail.com'
    gmail_pwd = 'GZloveXJ1314'
    to = 'xujingone1989@gmail.com'

    msg_header = 'From: Sender Name <sender@server>\r\n' \
             'To: Receiver Name <receiver@server>\r\n' \
             'Cc: Receiver2 Name <receiver2@server>\r\n' \
             'MIME-Version: 1.0\r\n' \
             'Content-type: text/html\r\n' \
             'Subject: Any subject\r\n'
    title = 'I love U....'
    msg_content = '<h2>{title} > <font color="green">OK</font></h2>\n'.format(
        title=title)
    msg_full = (''.join([msg_header, msg_content])).encode()
    # server = smtplib.SMTP('smtp.gmail.com:587')
    # server.starttls()
    # server.login(sender, )
    # server.sendmail(sender, recept, msg = msg_full)
    #                 # ['receiver@server.com', 'receiver@server.com'],
    # server.quit()

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_pwd)

    server.sendmail(gmail_user, to, msg = msg_full)
    server.quit()
    print("Successful")
except Exception as ex:
    print(ex)
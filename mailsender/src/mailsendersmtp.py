#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from time import gmtime, strftime

def sendEmailWithAttachment(path, configList): 
    try:
        msg = MIMEMultipart()
        msg['From'] = configList[0]
        msg['To'] = ', '.join(configList[2])
        msg['Subject'] = configList[3] + "  " + strftime("%Y-%m-%d %H:%M:%S", gmtime())

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(path, "rb").read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition",
                                'attachment; filename="%s"' % path)
        msg.attach(part)

        server = smtplib.SMTP(configList[4], configList[5])
        server.starttls()
        server.login(configList[0], configList[1])
        server.sendmail(configList[0], configList[2], msg.as_string())
        server.quit()
        return 0
    except:
        return -1
        
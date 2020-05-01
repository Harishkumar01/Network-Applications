#run an smtp server in local

import smtplib

message = """ From: From harish <clientmachine>
To: To Harishkumar <machine running smtp server>
MIME-Version: 1.0
Content-Type: text/html
Subject: Test HTML email

This is an html email message


<h1>this is test HTML Message</h1>
"""

try:
	smtp = smtplib.SMTP("ip of smtp server")
	smtp.sendmail("from","to",message)
	print("Email sent")
except Exception as err:
	print(err)

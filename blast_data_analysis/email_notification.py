#usr/bin/env python3

import argparse


parser = argparse.ArgumentParser()
parser.add_argument("email", help="input the email address you wish the notification to be sent to")
parser.add_argument( '-a','--attachment', help='input the name of the file you wish to attach', default='no_file')
args = parser.parse_args()


import smtplib
import socket
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

fromaddr = 'bioinformaticsnotification@gmail.com'
toaddr = str(args.email)
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Your program has finished"

now = datetime.now()
where = socket.gethostname()
when_micro = now.strftime('%I:%M')
when_macro = now.strftime('%m/%d/%Y')
finish_time = 'at %s on %s.' % (when_micro , when_macro)


body = 'The program you were running on the computer \'' + where + '\' completed ' + finish_time


if args.attachment != 'no_file':
	read_attachment = open(args.attachment, "rb")
	part = MIMEBase('application', 'octet-stream')
	part.set_payload((read_attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % args.attachment)
	attach_note = '\nThe desired output file,\' %s\' is attached.' % (args.attachment)
	body = '\n\n' + body + attach_note
	msg.attach(part)
else:
	pass	
	
msg.attach(MIMEText(body, 'plain'))

 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, 'EuanFish12')
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
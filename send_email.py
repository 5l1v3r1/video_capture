"""Requires a file named config.cfg in the same directory with the format below:

[GMAIL]
smtp_server: smtp.gmail.com
smtp_port: 587
smtp_username: gmail_user_name
smtp_password: application_key

[ALERT]
from: from_address
to: address_to_send_to

gmail_user_name: str
    username of gmail account to use to send mail
smtp_password: str
    application key generated from the gmail account
from: str
    sender's email
to: str
    email address to send the alert to
"""
import smtplib
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser
import os
import cv2
import time
import tempfile
from datetime import datetime


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.cfg'))

gmail = {k: v for k, v in config.items('GMAIL')}
_from = config.get('ALERT', 'from')
_to = config.get('ALERT', 'to')


def send_mail(_from, _to, subject, content, filepath=None):
    msg = MIMEMultipart(From=_from, To=_to, Subject=subject)
    msg['subject'] = subject
    msg['from'] = _from
    msg['to'] = _to
    msg.attach(MIMEText(content))
    if filepath:
        with open(filepath, 'rb') as f:
            msg.attach(MIMEApplication(
                f.read(), Content_Disposition='attachment; filename=test',
                Name='Test.jpg'))
    mail = smtplib.SMTP(gmail['smtp_server'], int(gmail['smtp_port']))
    mail.starttls()
    mail.login(gmail['smtp_username'], gmail['smtp_password'])
    mail.sendmail(_from, [_to], msg.as_string())
    mail.quit()


if __name__ == '__main__':
    cap = cv2.cv.CaptureFromCAM(0)
    time.sleep(0.25)
    if cap:
        frame = cv2.cv.QueryFrame(cap)
        _file = tempfile.NamedTemporaryFile(suffix='.jpg')
        cv2.cv.SaveImage(_file.name, frame)
        timestr = datetime.now().strftime('%H:%M:%S %y-%b-%d')
        send_mail('home_security', _to, 'Movement detected {}'.format(timestr),
                  'This is the content', _file.name)

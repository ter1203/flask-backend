from typing import List
from flask_mail import Mail, Message
from flask import render_template, Flask, current_app

mail: Mail = None
def init_mail(app: Flask):
    '''Initialize email'''

    global mail
    mail = Mail(app)


def send_mail(
    title: str,
    sender: str,
    recipients: List[str],
    html: str
):
    '''Send mail'''

    msg = Message(title, sender=sender, recipients=recipients)
    msg.html = html
    mail.send(msg)


def send_mail_template(
    title: str,
    sender: str,
    recipients: List[str],
    template: str,
    **kwargs
):
    '''Send html mail'''

    msg = Message(title, sender=sender, recipients=recipients)
    msg.html = render_template(template, **kwargs)

    current_app.logger.debug(msg.html)

    mail.send(msg)

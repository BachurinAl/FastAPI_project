import smtplib
from email.message import EmailMessage
from celery import Celery
from config import SMTP_USER, SMTP_PASSWORD

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('tasks', broker='redis://localhost:6379')

def get_email_template_dashboard(username: str):
    email = EmailMessage()
    email['Subject'] = 'TradePro: Отчет Дашборд'
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER

    email.set_content(
        '<div>'
        f'<h1>Здравствуйте, вот ваш отчет.</h1>'
        '<img src="https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fbringwell.ru%2Fwp-content%2Fuploads%2Ff%2Fd%2F5%2Ffd562eda0375586d368e7e965b942406.png&lr=9&pos=13&rpt=simage&text=%D0%BE%D1%82%D1%87%D0%B5%D1%82%20%D0%B4%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4" width="600">'
        '</div>',
        subtype='html'
    )
    return email

@celery.task
def send_email_report_dashboard(username: str):
    email = get_email_template_dashboard(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
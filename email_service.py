import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr


class EmailService():
    def __init__(self, email:str, password:str):
        self.email = email
        self.password = password
        self.smtp_server = None
        self.smtp_port = None
        self.connection = None
        
        self.check_smtp_server_by_email()
        
    def check_smtp_server_by_email(self):
        
        smtp_list = {
            'gmail': {'server': 'smtp.gmail.com', 'port': 587},
            'outlook': {'server': 'smtp.office365.com', 'port': 587},
            'hotmail': {'server': 'smtp.office365.com', 'port': 587},
            'yahoo': {'server': 'smtp.mail.yahoo.com', 'port': 587}
        }
        
        email_domain = self.check_email_domain()
        
        if email_domain in smtp_list:
            self.smtp_server = smtp_list[email_domain]['server']
            self.smtp_port = smtp_list[email_domain]['port']
       
    
    def check_email_domain(self):
        regex_result = re.findall('@([^\.]+)', self.email)
        
        if regex_result:
            return regex_result[0]
            
    def connect(self):
        self.connection = smtplib.SMTP(self.smtp_server, self.smtp_port)
        self.connection.ehlo()
        self.connection.starttls()
    
    def quit(self):
        if self.connection:
            self.connection.quit()
    
    def login(self):
        self.connection.ehlo()
        self.connection.login(self.email, self.password)
    
    def send(self, to:str, subject:str, message:str, html:bool=False):
        
        msg = MIMEMultipart()
        msg['From'] = formataddr((str(Header('Yellot', 'utf-8')), self.email))
        msg['To'] = to
        msg['Subject'] = subject

        text = MIMEText(message, 'html' if html else 'text')
        msg.attach(text)
        
        self.connection.sendmail(self.email, to, msg.as_string())
        
        return (to, 'success')
from email_service import EmailService
from datetime import datetime
from models import UserClick
import base64
from config import URL_API_PROD
from io import StringIO
import csv 


def make_csv(data:list) -> str:
    csv_lines = []
    
    header = [cel for cel in data[0]]
    
    csv_lines.append(header)
    
    for line in data:
        line = [cel for cel in line.values()]
        csv_lines.append(line)
        
    si = StringIO()
    cw = csv.writer(si)
    cw.writerows(csv_lines)
    
    return si.getvalue()


def get_user_click_from_response(response:str) -> UserClick:
    
    email = base64.b64decode(response).decode("utf-8")
    
    user_click_from_response = {
        'user': get_user_from_email(email),
        'email': email,
        'datetime': datetime.now()
    }
    
    return UserClick(**user_click_from_response)

def get_all_users_clicks_to_response() -> list:
    return UserClick.all()

def get_user_from_email(email:str) -> str:
    
    user = email.replace('@yellot.com.br','')
    user = user.split('.')
    user = ' '.join([name.capitalize() for name in user])
    
    return user


def drop_table_user_click():
    return UserClick.drop_table()


def make_html_from_phishing_email(email:str) -> str:
    
    url = URL_API_PROD
    
    email_base64 = base64.b64encode(bytes(email, 'utf-8'))
    email_base64 = email_base64.decode('utf-8')
    
    link = url + email_base64
    
    with open('templates/email.html', 'r', encoding='utf8') as email_file:
        html = email_file.read()
        html = html.format(link = link)
        
    return html


def send_phishing_emails(email:str, password:str, to_list: list) -> list:
    email_service = EmailService(email, password)
    email_service.connect()
    email_service.login()
    
    results = []
    
    for to in to_list:
        html = make_html_from_phishing_email(to)
        result = email_service.send(to, 'Pesquisa Salarial', html, html=True)
        results.append(result)
        
    email_service.quit()
    
    return results
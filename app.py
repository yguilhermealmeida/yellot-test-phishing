from flask import Flask, render_template, request, make_response
from services import *

app = Flask(__name__)


@app.route('/<encoded_email>')
def get_user_click(encoded_email:str):
    
    user_click = get_user_click_from_response(encoded_email)
    user_click.save()

    return render_template('checkout.html')


@app.route('/results')
def get_all_users_clicks():
    return get_all_users_clicks_to_response()


@app.route('/results/download')
def get_all_users_clicks_csv():
    all_users_clicks = get_all_users_clicks_to_response()
    csv = make_csv(all_users_clicks)

    output = make_response(csv)
    output.headers["Content-Disposition"] = "attachment; filename=results.csv"
    output.headers["Content-type"] = "text/csv"
    
    return output


@app.route('/send', methods = ['POST', 'GET'])
def send():
    if request.method == 'GET':
        return render_template('send.html')
    
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        to_list = request.form['to_list']
        to_list = to_list.replace('\r','')
        to_list = to_list.split('\n')
        
        results = send_phishing_emails(email, password, to_list)
        
        return {
            'email': email,
            'to_len': len(to_list), 
            'to_list': to_list,
            'results': results
        }

@app.route('/admin/dropTable')
def drop_table():
    return {'success': drop_table_user_click()}

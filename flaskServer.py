from flask import Flask, render_template,  redirect, url_for, request, session
from werkzeug.serving import make_server
from manipulate_json import JsonStuff
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)



@app.route("/")
def home():
        
    if 'username' in session:
        return redirect("/counter")
    else:
        return render_template("home.html")
    
    
 
    
@app.route('/counter')
def counter():
    if 'username' not in session:
        return redirect("/")
    else:
        return render_template('counter.html', current_number=JsonStuff.get_user_number(session['username']), current_user = session['username'])

@app.route('/get_counter')
def get_counter():
    return str(JsonStuff.get_user_number(session['username']))

@app.route('/add', methods=['POST'])
def add():
    addition = int(request.form['addition'])
    JsonStuff.increment_user_number(session['username'],addition)
    return redirect('/counter')

@app.route('/subtract', methods=['POST'])
def subtract():
    subtraction = int(request.form['subtraction'])
    JsonStuff.decrement_user_number(session['username'],subtraction)
    return redirect('/counter')

@app.route('/logout', methods=['POST'])
def logout():
    JsonStuff.erase_user(session['username'])
    session.pop('username')
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    
    username = request.form['username']
    password = request.form['password']
    
    
    
    # Check if the credentials are valid 
    if(process_login(username, password)):
        #Successful login, redirect to the counter page
        session['username'] = request.form['username']
        return redirect('/counter')
    else:
        # nvalid credentials, redirect back to the login page
        
        return redirect('/')
    

def process_login(username, password):
        client_ip = request.remote_addr

        client_port = request.environ.get('REMOTE_PORT')
        
        error, status = JsonStuff.save_user_data(username, password, client_ip, client_port)
        if(status == False):
            print(error)
            return False
        else:
            return True

    
if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, debug=True)
    
    print(f"Server is running at http://{host}:{port}/")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
 

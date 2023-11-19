from flask import Flask, render_template,  redirect, url_for, request, session
from werkzeug.serving import make_server
from manipulate_json import JsonStuff
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)



@app.route("/")
def home():
    
    # referer = request.headers.get('Referer', '')
    # if '/counter' not in referer:
    #     return render_template("home.html")
    # else:
        
    if 'username' in session:
        print("here")
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
    # Return the current number as plain text
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
    
    
    
    # Check if the credentials are valid (replace this with your actual authentication logic)
    if(process_login(username, password)):
        # Successful login, redirect to the counter page
        session['username'] = request.form['username']
        return redirect('/counter')
    else:
        # Invalid credentials, redirect back to the login page
        
        return redirect('/')
    

def process_login(username, password):
        client_ip = request.remote_addr

        # Get the client's port (not commonly used in this context)
        client_port = request.environ.get('REMOTE_PORT')
        
        #MAKE JSON PROFILE: If method returns false, the user needs to retr
        error, status = JsonStuff.save_user_data(username, password, client_ip, client_port)
        if(status == False):
            print(error)
            return False
        else:
            return True

    
if __name__ == '__main__':
    # host = '127.0.0.1'
    # port = random.randint(1000,8000)
    app.run(host='0.0.0.0', port=5000, debug=True)
    #server = make_server(host, port, app)
    print(f"Server is running at http://{host}:{port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
 

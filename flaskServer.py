from flask import Flask, render_template,  redirect, url_for, request
from werkzeug.serving import make_server
from manipulate_json import JsonStuff

app = Flask(__name__)

current_number = 0
successfule_registration = False
current_user = ""


@app.route("/")
def home():
    return render_template("home.html")
 
    
@app.route('/counter')
def counter():
    return render_template('counter.html', current_number=current_number)

@app.route('/get_counter')
def get_counter():
    # Return the current number as plain text
    return str(current_number)

@app.route('/add', methods=['POST'])
def add():
    global current_number
    addition = int(request.form['addition'])
    current_number += addition
    return redirect('/counter')

@app.route('/subtract', methods=['POST'])
def subtract():
    global current_number
    subtraction = int(request.form['subtraction'])
    current_number -= subtraction
    return redirect('/counter')

@app.route('/logout', methods=['POST'])
def logout():
    JsonStuff.erase_user(current_user)
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if the credentials are valid (replace this with your actual authentication logic)
    if(process_login(username, password,)):
        # Successful login, redirect to the counter page
        return redirect('/counter')
    else:
        # Invalid credentials, redirect back to the login page
        return redirect('/')
    

# @app.route('/shutdown', methods=['POST'])
# def shutdown():
#     shutdown_server()
#     return 'Server shutting down...'

def process_login(username, password):
        global current_user
        client_ip = request.remote_addr

        # Get the client's port (not commonly used in this context)
        client_port = request.environ.get('REMOTE_PORT')
        
        #MAKE JSON PROFILE: If method returns false, the user needs to retr
        error, status = JsonStuff.save_user_data(username, password, client_ip, client_port)
        if(status == False):
            print(error)
            return False
        else:
            current_user = username
            return True

# def shutdown_server():
#     print("Shutting down the server...")
#     server.shutdown()
    
if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5000
    server = make_server(host, port, app)
    print(f"Server is running at http://{host}:{port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
 

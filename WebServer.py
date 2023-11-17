from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import time
from urllib.parse import parse_qs
import json
import random
from manipulate_json import JsonStuff

hostName = "localhost"
serverPort = random.randint(0,1000)

successfule_registration = False
current_user = ""


class WebServer(BaseHTTPRequestHandler):
    current_number = 0

    
    def do_GET(self):

        client_ip, client_port = self.client_address
        print(f"Client IP: {client_ip}, Client Port: {client_port}")
        
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>The Best Server Ever</title></head>", "utf-8"))
            self.wfile.write(bytes("<p>To continue, please register your profile in the system:</p>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8")) 
            #Login
            self.wfile.write(bytes('<form action="/login" method="post">', "utf-8"))
            self.wfile.write(bytes('  <label for="username">Username:</label>', "utf-8"))
            self.wfile.write(bytes('  <input type="text" id="username" name="username" required><br>', "utf-8"))
            self.wfile.write(bytes('  <label for="password">Password:</label>', "utf-8"))
            self.wfile.write(bytes('  <input type="password" id="password" name="password" required><br>', "utf-8"))
            self.wfile.write(bytes('  <input type="submit" value="Submit">', "utf-8"))
            self.wfile.write(bytes('</form>', "utf-8"))
            
            self.wfile.write(bytes('<form action="/shutdown" method="post"><input type="submit" value="Shutdown Server"></form>', "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
        elif self.path == "/counter":
            
            self.send_response(200)
            # Read the content of the HTML file
            with open("counter.html", "r") as file:
                html_content = file.read()

            # Replace the placeholder with the actual current number
            html_content = html_content.replace("{current_number}", str(self.current_number))
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            self.wfile.write(bytes(html_content, "utf-8"))
           
        elif self.path == "/get_counter":
            # Send the current number as a plain text response
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes(str(self.current_number), "utf-8"))
            
    def do_POST(self):
        
        client_ip, client_port = self.client_address
        
        
        if self.path == "/shutdown":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("<html><body><p>Shutting down the server...</p></body></html>", "utf-8"))
            # Start a new thread to perform the server shutdown, allowing this response to be sent
            threading.Thread(target=self.shutdown_server).start()
        elif self.path == "/login":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            post_params = parse_qs(post_data)
            
            username = post_params['username'][0]
            password = post_params['password'][0]

            # Process the login TODO make page for profile counter
            
            if(self.process_login(username, password)):
                current_user = username
                self.send_response(302)  # Redirect
                self.send_header('Location', '/counter') 
                self.end_headers()    
            else:
                self.send_response(302)  # Redirect
                self.send_header('Location', '/') 
                self.end_headers()

        elif self.path == "/add":
           
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            post_params = parse_qs(post_data)
            addition = int(post_params['addition'][0])
            self.current_number += addition
            print(self.current_number)
            self.send_response(302)  # Redirect
            self.send_header('Location', '/counter')
            self.end_headers()
            
        elif self.path == "/subtract":
           
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            post_params = parse_qs(post_data)
            subtraction = int(post_params['subtraction'][0])
            self.current_number -= subtraction
            print(self.current_number)
            self.send_response(302)  # Redirect
            self.send_header('Location', '/counter')
            self.end_headers()
            
        elif self.path == "/logout":
            #TODO DELETE ALL CURRENT USERDATA
            
            self.send_response(302)  # Redirect
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_error(404, "Not Found")
            
    def shutdown_server(self):
        self.server.shutdown()
    
    #SONYA AND ALINA
    def process_login(self, username, password):
        
        client_ip, client_port = self.client_address
        
        
        
        #MAKE JSON PROFILE: If method returns false, the user needs to retr
        error, status = JsonStuff.save_user_data(username, password, client_ip, client_port)
        if(status == False):
            print(error)
            return False
        else:
            return True
        
            
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), WebServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
    
    
import json

USER_DATA_FILE = "example_user.json"  # JSON file to store user data

class JsonStuff:  # Placeholder class; adjust this according to your structure
    @staticmethod
    def save_user_data(username, password, client_ip, client_port):
        # Load existing user data from the JSON file
        try:
            with open(USER_DATA_FILE, 'r') as file:
                users = json.load(file)
                if not isinstance(users, list):  # Ensure users is a list
                    users = list()
        except (FileNotFoundError,  json.decoder.JSONDecodeError):
            users = list()

        # Check if username already exists
        for user in users:
            if user['id'] == username:
                return "Username already exists", False
                #raise ValueError("Username already exists")

        # Check if password already exists
        for user in users:
            if user['password'] == password:
                return "Password already exists", False
                raise ValueError("Password already exists")

        # Validate password length
        if len(password) < 4:
            return "Password is too short", False
            #raise ValueError("Password is too short")

        # Validate for invalid characters in username or password (adjust as needed)
        invalid_chars = set("!@#$%^&*()+=-[]{}|\\;:'\",.<>/?")
        if any(char in invalid_chars for char in username):
            return "Username contains invalid characters", False
            #raise ValueError("Username contains invalid characters")

        if any(char in invalid_chars for char in password):
            return "Password contains invalid characters", False
            #raise ValueError("Password contains invalid characters")

        # Add new user data
        users.append({
            'id': username,
            'password': password,
            'server': {
                'ip': client_ip,
                'port': client_port
            }
        })

        # Save updated user data back to the JSON file
        with open(USER_DATA_FILE, 'w') as file:
            json.dump(users, file, indent=4)
        
        return "success", True
    
    def erase_user(username):
        
        try:
            with open(USER_DATA_FILE, 'r') as file:
                users = json.load(file)
                if not isinstance(users, list):  # Ensure users is a list
                    users = list()
        except (FileNotFoundError,  json.decoder.JSONDecodeError):
            users = list()
        
        users = [user for user in users if user['id'] != username]
        
        with open(USER_DATA_FILE, 'w') as file:
            json.dump(users, file, indent=4)
        
        

if __name__ == '__main__':
    try:
        JsonStuff.save_user_data('John', 'Nash', 'whdnq', 'feqk')
    except ValueError as e:
        print(f"Error: {e}")

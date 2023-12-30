import json
import secrets
import hashlib
import string


USER_DATA_FILE = "example_user.json"  # JSON file to store user data
PEPPER = "999988888ABABABA"  # Pepper value (can be anything)

class JsonStuff:
    @staticmethod
    def save_user_data(username, password, client_ip, client_port):
        # Load existing user data from the JSON file
        try:
            with open(USER_DATA_FILE, 'r') as file:
                users = json.load(file)
                if not isinstance(users, list):  # Ensure users is a list
                    users = list()
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            users = list()

        # Check if username already exists
        for user in users:
            if user['id'] == username:
                return "Username already exists", False
        
        # Minimum length is 8 
        if len(password) <= 8:
            return "Password should be at least 8 characters long", False

        # Check for special characters in the password
        special_characters = set(string.punctuation)  # Get all special characters
        if not any(char in special_characters for char in password):
            return "Password must contain at least one special character", False

        # Rest of the code remains unchanged
        # Generate a unique salt for each user
        salt = secrets.token_hex(16)
        # Apply pepper to the password
        peppered_password = password + PEPPER
        # Hash the salted and peppered password
        hashed_password = hashlib.sha256((salt + peppered_password).encode()).hexdigest()

        # Add new user data
        users.append({
            'id': username,
            'password': hashed_password,
            'salt': salt,
            'server': {
                'ip': client_ip,
                'port': client_port
            },
            'number': 0
        })

        # Save updated user data back to the JSON file
        with open(USER_DATA_FILE, 'w') as file:
            json.dump(users, file, indent=4)

        return "success", True

    @staticmethod
    def validate_user_credentials(username, password):
        try:
            with open(USER_DATA_FILE, 'r') as file:
                users = json.load(file)
                if not isinstance(users, list):  # Ensure users is a list
                    users = list()
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return False

        for user in users:
            if user['id'] == username:
                # Get the salt and pepper for password 
                salt = user.get('salt', '')
                peppered_password = password + PEPPER
                # Hash the salted and peppered password for comparison
                hashed_password = hashlib.sha256((salt + peppered_password).encode()).hexdigest()
                if hashed_password == user['password']:
                    return True

        return False
    
    
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
        
    def get_user_number(username):
        
        try:
            with open(USER_DATA_FILE, 'r') as file:
                users = json.load(file)
                if not isinstance(users, list):  # Ensure users is a list
                    users = list()
        except (FileNotFoundError,  json.decoder.JSONDecodeError):
            users = list()
            
        for user in users:
            if(user['id'] == username):
                return user['number']  
            
    def increment_user_number(username, amount):
        try:
            with open(USER_DATA_FILE, 'r') as file:
                users = json.load(file)
                if not isinstance(users, list):  # Ensure users is a list
                    users = list()
        except (FileNotFoundError,  json.decoder.JSONDecodeError):
            users = list()
            
        for user in users:
            if user['id'] == username:
                if amount < 0:  
                    user['number'] = user['number'] - abs(amount)  # Subtract absolute value
                else:
                    user['number'] = user['number'] + amount  # Otherwise, perform addition

        # Rewrite JSON file with updated users
        with open(USER_DATA_FILE, 'w') as file:
            json.dump(users, file, indent=4)
        
    def decrement_user_number(username, amount):
        try:
            with open(USER_DATA_FILE, 'r') as file:
                users = json.load(file)
                if not isinstance(users, list):  # Ensure users is a list
                    users = list()
        except (FileNotFoundError,  json.decoder.JSONDecodeError):
            users = list()
            
        for user in users:
            if(user['id'] == username):
                if amount < 0: 
                    user['number'] = user['number'] + abs(amount)  # Add absolute value
                else:
                    user['number'] = user['number'] - amount  # Otherwise, perform substraction

        with open(USER_DATA_FILE, 'w') as file:
            json.dump(users, file, indent=4)

if __name__ == '__main__':
    try:
        JsonStuff.save_user_data('John', 'Nash', 'whdnq', 'feqk')
    except ValueError as e:
        print(f"Error: {e}")

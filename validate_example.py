import logging
import random
from twilio.rest import Client

# Configure logging
logging.basicConfig(filename="password_attempts.log", level=logging.INFO)
logging.getLogger("twilio").setLevel(logging.WARNING)

CREDENTIALS_FILE = ""

def load_credentials():
    #Load credentials from text file into a dictionary
    credentials = {}
    with open(CREDENTIALS_FILE, "r") as f:
        for line in f:
            username, password, phone = line.strip().split(",")
            credentials[username] = {"password": password, "phone": phone}
        print(credentials)
    return credentials

def save_credentials(credentials):
    #Save credentials dictionary back into the text file
    with open(CREDENTIALS_FILE, "w") as f:
        for user, data in credentials.items():
            f.write(f"{user},{data['password']},{data['phone']}\n")


class PasswordValidator:
    def __init__(self, username, correct_password, phone_number, max_attempts=5):
        self.username = username
        self.correct_password = correct_password
        self.phone_number = phone_number
        self.max_attempts = max_attempts
        self.attempts = 0

        self.account_sid = ""
        self.auth_token = ""
        self.twilio_number = "+"

    def send_otp(self):
        """Generate and send OTP via Twilio"""
        otp = str(random.randint(100000, 999999))
        try:
            client = Client(self.account_sid, self.auth_token)
            client.messages.create(
                body=f"Your OTP is: {otp}",
                from_=self.twilio_number,
                to=self.phone_number
            )
            logging.info(f"OTP sent to {self.username} at {self.phone_number}")
            return otp
        except Exception as e:
            logging.error(f"Failed to send OTP to {self.username}: {e}")
            return None

    def reset_password(self):
        """Handle password reset process"""
        otp = self.send_otp()
        if not otp:
            print("Failed to send OTP. Please try again later.")
            return False

        entered_otp = input("Enter the OTP sent to your registered number: ")
        if entered_otp == otp:
            new_password = input("Enter your new password: ")
            self.correct_password = new_password

            # Update file
            user_credentials[self.username]["password"] = new_password
            save_credentials(user_credentials)

            logging.info(f"User {self.username} successfully reset password.")
            print("Password reset successful! Please log in with your new password.")
            return True
        else:
            logging.warning(f"User {self.username} entered wrong OTP during reset.")
            print("Incorrect OTP. Password reset failed.")
            return False

    def validate(self):
        # Main validation loop
        while self.attempts < self.max_attempts:
            entered = input("Enter password: ")
            self.attempts += 1

            if entered == self.correct_password:
                print("Access Granted!")
                logging.info(f"User {self.username} logged in successfully.")
                return True
            else:
                print(f"Wrong password! Attempts left: {self.max_attempts - self.attempts}")
                logging.warning(f"User {self.username} entered wrong password (Attempt {self.attempts})")

                choice = input("Forgot password? (yes/no): ").strip().lower()
                if choice == "yes":
                    if self.reset_password():
                        return True
                    else:
                        return False

        print("Too many failed attempts. Access Denied!")
        logging.error(f"User {self.username} exceeded maximum attempts. Access denied.")
        return False


# Load credentials from file
user_credentials = load_credentials()

username = input("Enter username: ")

if username not in user_credentials:
    print("Invalid username! Access Denied.")
    logging.error(f"Unknown user '{username}' tried to login.")
else:
    validator = PasswordValidator(username,user_credentials[username]["password"],user_credentials[username]["phone"])
    validator.validate()                #  user_credentials[Moksha]["password"]

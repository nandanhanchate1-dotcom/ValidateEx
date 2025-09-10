# Validate Password 

# 🔐 Password Validation System with OTP (Twilio Integration)

This script implements a **secure password validation system** that supports normal login attempts and a **password reset mechanism** via **OTP (One Time Password)** sent using Twilio.  

---

## 📂 Features
- 🔑 **Password Validation**: Verifies user credentials against stored values.  
- 📱 **OTP via SMS**: Sends a random 6-digit OTP to the registered phone number using Twilio.  
- 🔄 **Password Reset**: Enables password resets upon successful OTP validation.  
- 📜 **Credential Storage**: Stores usernames, passwords, and phone numbers in a text file.  
- 📊 **Logging**: Tracks login attempts, OTP requests, and failures via `logging` into a log file.  

---

## ⚙️ Workflow
1. 👤 User enters their **username**.  
   - ❌ If invalid → Access Denied.  
   - ✅ If valid → Prompt for password.  

2. 🔑 User inputs **password**.  
   - If correct → ✅ *Access Granted*.  
   - If wrong → ⚠️ *Attempts tracked*.  

3. 🛑 After multiple failed attempts:  
   - ❓ User is asked if they forgot their password.  
   - If "yes" → OTP is sent to their registered mobile number.  

4. 📱 **OTP Verification**:
   - ✅ Correct OTP → User sets a new password → Saved in credentials file.  
   - ❌ Wrong OTP → Password reset denied.  

5. 📘 All actions (logins, OTP sent, errors) are logged into **`password_attempts.log`**.  

---

## 📁 File Handling
- `load_credentials()`: Loads `username,password,phone` from a text file into a dictionary.  
- `save_credentials()`: Updates the credentials file whenever a password reset happens.  

---

## 👨‍💻 Classes
### `PasswordValidator`
Handles the complete login and reset process.  
- **Attributes**:  
  - `username` 👤  
  - `correct_password` 🔑  
  - `phone_number` 📱  
  - `max_attempts` (default = 5)  

- **Methods**:  
  - `send_otp()` → Generates and sends OTP 🔄  
  - `reset_password()` → Resets password if OTP is validated 🔐  
  - `validate()` → Main login workflow with multiple attempts ⚡  

---

## 📝 Logging
- ✅ Successful login.  
- ⚠️ Wrong password attempts.  
- 📩 OTP sent.  
- ❌ Invalid OTP entries.  
- 🚫 Access denied after too many failed attempts.  

---

## 🚀 Usage
1. Set your **Twilio credentials** (`account_sid`, `auth_token`, `twilio_number`).  
2. Prepare your **credentials file** with entries in:  

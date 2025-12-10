import smtplib
from email.mime.text import MIMEText
import os
import sys

# --- Configuration ---
# Read all necessary variables from the environment
sender = os.environ.get('EMAIL_USERNAME')
receiver_string = os.environ.get('EMAIL_TO')
subject = os.environ.get('EMAIL_SUBJECT')
body = os.environ.get('EMAIL_BODY')
server = os.environ.get('EMAIL_SERVER')
port = os.environ.get('EMAIL_PORT')
password = os.environ.get('EMAIL_PASSWORD')

# --- Validation ---
if not all([sender, receiver_string, subject, body, server, port, password]):
    print("FATAL ERROR: One or more required environment variables (EMAIL_*) are missing.")
    sys.exit(1)

# Split the string of receivers into a list (using the semicolon separator)
receivers = [r.strip() for r in receiver_string.split(';') if r.strip()]

if not receivers:
    print("ERROR: No valid recipients found in EMAIL_TO.")
    sys.exit(1)

# --- Email Construction ---
msg = MIMEText(body, 'html') # Use 'html' for the rich body content
msg['Subject'] = subject
msg['From'] = sender
# Set 'To' header field for display (joining recipients with comma)
msg['To'] = ", ".join(receivers) 

print(f"Attempting to connect to {server}:{port} to send email to {len(receivers)} recipient(s)...")

# --- Send Logic ---
try:
    # 1. Connect and Start TLS
    smtp_server = smtplib.SMTP(server, int(port))
    smtp_server.starttls()
    
    # 2. Login
    smtp_server.login(sender, password)
    print("Authentication successful.")
    
    # 3. Send the mail
    # The second argument to sendmail MUST be a list of all recipients
    smtp_server.sendmail(sender, receivers, msg.as_string())
    print("SUCCESS: Email sent successfully!")
    
except Exception as e:
    print(f"FAILURE: Could not send email. Error: {e}")
    sys.exit(1) # Ensure the workflow step fails
    
finally:
    smtp_server.quit()
    print("Connection closed.")

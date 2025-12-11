import smtplib
from email.mime.text import MIMEText
import os
import sys

# --- Configuration & Validation ---
# Read all necessary variables from the environment
env_vars = [
    'EMAIL_USERNAME', 'EMAIL_TO', 'EMAIL_SUBJECT', 'EMAIL_SERVER', 'EMAIL_PORT', 
    'EMAIL_PASSWORD', 'PR_TITLE', 'PR_NUMBER', 'PR_AUTHOR', 'PR_MERGED_BY', 
    'PR_URL', 'SUMMARY_OUTPUT', 'DIFF_OUTPUT'
]

config = {var: os.environ.get(var) for var in env_vars}

if not all(config.values()):
    missing = [var for var, val in config.items() if not val]
    print(f"FATAL ERROR: Missing environment variables: {', '.join(missing)}")
    sys.exit(1)

# Split the receiver string
receivers = [r.strip() for r in config['EMAIL_TO'].split(';') if r.strip()]

# --- HTML Body Template (Defined in Python) ---
HTML_BODY_TEMPLATE = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
  <h1 style="border-bottom: 2px solid #007bff; padding-bottom: 5px; color: #007bff;">
    ✅ PR MERGED: {config['PR_TITLE']}
  </h1>
  <p>A Pull Request has been successfully <strong>MERGED</strong> into the <code>main</code> branch.</p>
  
  <table border="0" cellpadding="5" cellspacing="0" style="width: 100%; max-width: 600px; border: 1px solid #ddd;">
    <tr>
      <td style="width: 30%; background-color: #f4f4f4;"><strong>PR Number:</strong></td>
      <td style="width: 70%;">#{config['PR_NUMBER']}</td>
    </tr>
    <tr>
      <td style="background-color: #f4f4f4;"><strong>Author:</strong></td>
      <td>@{config['PR_AUTHOR']}</td>
    </tr>
    <tr>
      <td style="background-color: #f4f4f4;"><strong>Merged By:</strong></td>
      <td>@{config['PR_MERGED_BY']}</td>
    </tr>
  </table>

  <h3 style="color: #28a745; margin-top: 25px;">🤖 Copilot AI-Generated Summary</h3>
  <div style="padding: 15px; border-left: 5px solid #28a745; background-color: #f7fff7; word-wrap: break-word;">
    {config['SUMMARY_OUTPUT']}
  </div>

  <h3 style="color: #6c757d; margin-top: 25px;">PR Code Changes (Diff)</h3>
  <div style="padding: 15px; border: 1px solid #eee; background-color: #fcfcfc; font-family: monospace; font-size: 13px; white-space: pre-wrap; word-wrap: break-word;">
    {config['DIFF_OUTPUT']}
  </div>

  <hr style="margin-top: 25px;">
  <p style="text-align: center;">
    <a href="{config['PR_URL']}" style="padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">
      View Full Pull Request on GitHub
    </a>
  </p>
</body>
</html>
"""

# --- Email Construction & Send Logic ---
# ... (rest of the script is the same, using HTML_BODY_TEMPLATE as the body variable)

# Create message object
msg = MIMEText(HTML_BODY_TEMPLATE, 'html')
msg['Subject'] = config['EMAIL_SUBJECT']
msg['From'] = config['EMAIL_USERNAME']
msg['To'] = ", ".join(receivers) 

print(f"Attempting to connect to {config['EMAIL_SERVER']}:{config['EMAIL_PORT']}...")

try:
    smtp_server = smtplib.SMTP(config['EMAIL_SERVER'], int(config['EMAIL_PORT']))
    smtp_server.starttls()
    smtp_server.login(config['EMAIL_USERNAME'], config['EMAIL_PASSWORD'])
    print("Authentication successful.")
    
    smtp_server.sendmail(config['EMAIL_USERNAME'], receivers, msg.as_string())
    print("SUCCESS: Email sent successfully!")
    
except Exception as e:
    print(f"FAILURE: Could not send email. Error: {e}")
    sys.exit(1)
    
finally:
    smtp_server.quit()
    print("Connection closed.")

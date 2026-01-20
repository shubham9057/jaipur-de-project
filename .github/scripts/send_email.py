import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(summary_file, diff_file):
    # 1. Read the content from the files
    try:
        with open(summary_file, 'r') as f:
            # Convert newlines to HTML breaks for the AI summary
            summary_content = f.read().replace('\n', '<br>')
        
        with open(diff_file, 'r') as f:
            # Read the diff and escape HTML characters
            diff_content = f.read().replace('<', '&lt;').replace('>', '&gt;')
    except Exception as e:
        print(f"Error reading files: {e}")
        sys.exit(1)   

    # 2. Read all necessary variables from the environment
    env_vars = [
        'EMAIL_USERNAME', 'EMAIL_SERVER', 'EMAIL_PORT', 'EMAIL_PASSWORD', 
        'PR_TITLE', 'PR_NUMBER', 'PR_AUTHOR', 'PR_MERGED_BY', 'PR_URL'
    ]

    config = {var: os.environ.get(var) for var in env_vars}

    # if not all(config.values()):
    #     missing = [var for var, val in config.items() if not val]
    #     print(f"FATAL ERROR: Missing environment variables: {', '.join(missing)}")
    #     sys.exit(1)

    # 3. Create HTML Body
    html_body = f"""
    <html>
      <body style="font-family: sans-serif; color: #333;">
        <h2>Copilot AI PR Summary</h2>
        <p><b>Author:</b> @{config['PR_AUTHOR']}</p>
        <hr>
        <div style="background: #f4f7f6; padding: 15px; border-radius: 5px; border: 1px solid #ddd;">
          {summary_content}
        </div>
        <h3>Code Changes</h3>
        <pre style="background: #222; color: #eee; padding: 10px; font-size: 12px; overflow: auto;">
          {diff_content}
        </pre>
        <br>
        <a href="{config['PR_URL']}" style="padding: 10px 20px; background: #2ea44f; color: white; text-decoration: none; border-radius: 5px;">View on GitHub</a>
      </body>
    </html>
    """

    # 4. Setup Email Metadata
    
    receivers_list = ['105shubhamnks@gmail.com', 'shubham.singhal@atrium.ai']

    msg = MIMEMultipart('alternative')
    msg.attach(MIMEText(html_body, 'html'))
    msg['Subject'] = f"✅ PR MERGED: PR #{config['PR_TITLE']} - {config['PR_TITLE']}"
    msg['From'] = config['EMAIL_USERNAME']
    msg['To'] = ", ".join(receivers_list)

    # 5. Send Email
    try:
        server = smtplib.SMTP(config['EMAIL_SERVER'], int(config['EMAIL_PORT']))
        server.starttls()
        server.login(config['EMAIL_USERNAME'], config['EMAIL_PASSWORD'])
        server.sendmail(config['EMAIL_USERNAME'], receivers_list, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure arguments are provided
    if len(sys.argv) < 3:
        print("Usage: python send_email.py <summary_file> <diff_file>")
        sys.exit(1)
        
    send_email(sys.argv[1], sys.argv[2])

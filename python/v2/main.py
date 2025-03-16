import dotenv
import yaml
import json
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


dotenv.load_dotenv("./smtp.env")

# --- Configuration ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")

# Filenames
TEMPLATE_FILE = "templates.yaml"
EMAILS_FILE = "emails.json"
ATTACHMENTS = ["Homayoon-Alimohammadi-Resume.pdf", "Research-Statement.pdf"]

def load_template(filename: str) -> dict:
    """Load the email template from a YAML file."""
    with open(filename, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def load_prof_data(filename: str) -> dict:
    """Load the list of professor data from a JSON file."""
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def attach_file(msg: MIMEMultipart, filepath: str) -> None:
    """Attach a file to the email message."""
    with open(filepath, "rb") as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(filepath))
    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(filepath)}"'
    msg.attach(part)

def main():
    # Load the template and the list of recipient emails
    template = load_template(TEMPLATE_FILE)
    prof_data = load_prof_data(EMAILS_FILE)

    # Setup SMTP connection to Gmail
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(SMTP_USER, SMTP_PASS)
    
    for prof in prof_data:
        prof_email = prof.get("email", "")

        # Substitute placeholders in subject and content
        subject = template.get("subject", "").format(**prof)
        content_plain = template.get("content_raw", "").format(**prof)
        content_html = template.get("content_html", "").format(**prof)
        
        # Create MIME multipart message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = prof_email
        
        # Attach plain text and HTML versions
        part1 = MIMEText(content_plain, "plain")
        part2 = MIMEText(content_html, "html")
        msg.attach(part1)
        msg.attach(part2)
        
        # Attach the files
        for attachment in ATTACHMENTS:
            if os.path.exists(attachment):
                attach_file(msg, attachment)
            else:
                print(f"Attachment {attachment} not found.")
        
        # Send email
        try:
            server.sendmail(SMTP_USER, prof_email, msg.as_string())
            print(f"Email sent to {prof_email}")
        except Exception as e:
            print(f"Failed to send email to {prof_email}: {e}")
    
    server.quit()

if __name__ == "__main__":
    main()

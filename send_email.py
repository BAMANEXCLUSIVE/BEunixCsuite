import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    smtp_server = "smtp.gmail.com"  # Use your SMTP server
    smtp_port = 587
    smtp_username = "your_email@gmail.com"  # Replace with your email
    smtp_password = "your_password"  # Replace with your password

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_username
    msg['To'] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Secure the connection
        server.login(smtp_username, smtp_password)
        server.send_message(msg)

# Example usage
send_email("Test Subject", "This is a test email body.", "recipient@example.com")
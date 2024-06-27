import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def private(name,email, phone, feedback):
    # Email configuration
    sender_email = "review@cosmeticcreationsspa.com"
    receiver_email = "Rebecca@cosmeticcreationsspa.com"
    password = "fdxi slyq umoh klge"
    # Email content
    subject = "Private Feedback"
    body = f"Full Name: {name}\nPhone Number: {phone}\nEmail: {email}\nFeedback: {feedback}"

    # Constructing the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Sending the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())



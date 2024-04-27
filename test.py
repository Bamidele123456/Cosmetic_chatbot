import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(first, last, number, appoint):
    # Email configuration
    sender_email = "bamideleprecious85@gmail.com"
    receiver_email = "Rebecca@cosmeticcreationsspa.com"
    password = "fhdr vwep reuq laxg"

    # Email content
    subject = "Appointment Details"
    body = f"First Name: {first}\nLast Name: {last}\nPhone Number: {number}\nAppointment Type: {appoint}"

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

# Assuming `first`, `last`, `number`, and `appoint` are extracted from the JSON data as mentioned in your code
first = "John"
last = "Doe"
number = "1234567890"
appoint = "Patient Coordinator"

# Sending the email
send_email(first, last, number, appoint)

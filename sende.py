import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def review_email(email):
    # Email configuration
    sender_email = "bamideleprecious85@gmail.com"
    receiver_email = email
    password = "fhdr vwep reuq laxg"

    # Email content
    subject = "Please share your feedback"
    html_content = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Email Template</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .header {
                text-align: center;
                padding: 10px 0;
            }
            .header img {
                max-width: 150px;
            }
            .content {
                font-size: 16px;
                color: #555555;
                text-align: center;
            }
            .content h1 {
                font-family: 'Roboto', Arial, Tahoma;
                Font-size: 32px;
                line-height: 48px;
                font-weight: 300;
                font-style: normal;
                color: #2a3135;
                padding: 20px 0 0 0;
                margin-top: 0;
            }
            .content p {
                font-family: 'Roboto', Arial, Tahoma;
                Font-size: 18px;
                line-height: 40px;
                font-weight: normal;
                font-style: normal;
                color: #607179;
                margin: 10px 0;
            }
            .button-container {
                text-align: center;
                margin: 20px 0;
            }
            .button {
                background-color: #28a745;
                color: #ffffff;
                padding: 15px 50px;
                text-decoration: none;
                border-radius: 5px;
                display: inline-block;
            }
            .footer {
                font-size: 14px;
                color: #888888;
                text-align: center;
                margin-top: 20px;
            }
            .footer p {
                margin: 5px 0;
            }
            .footer img {
                max-width: 100px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="https://cosmeticcreationsspa.com/wp-content/uploads/2016/08/logo.png" alt="Cosmetic Creations Logo">
                <p>5 ⭐ ⭐ ⭐ ⭐ ⭐</p>
            </div>
            <div class="content">
                <h1>Cosmetic Creations Skin Sanctuary & Med Spa</h1>
                <p>Hi Dele Oriku,</p>
                <p>Thanks for choosing Cosmetic Creations Skin Sanctuary & Med Spa. I hope you enjoyed your visit to Cosmetic Creations.</p>
                <p>Please consider leaving a review on Google and/or Yelp as it really helps us. Please mention your Aesthetician's name when leaving a review. If you have already left us a review then we thank you! ❤️ Cosmetic Creations Team!</p>
                <div class="button-container">
                    <a href="https://fcee-172-212-98-191.ngrok-free.app//gogn" class="button">Review Us</a>
                </div>
                <p>Sincerely,</p>
                <p>Rebecca Rotter</p>
                <div class="footer">
                    <img src="https://cosmeticcreationsstore.com/cdn/shop/files/Final-New-Logo-2020_2_300x300.png?v=1613544613" alt="Rebecca Rotter">
                    <p>Cosmetic Creations Skin Sanctuary & Med Spa</p>
                    <p>9923 TOPANGA CANYON BLVD.<br>Chatsworth, CA<br>(818) 528-5805<br><a href="mailto:info@cosmeticcreationsspa.com">info@cosmeticcreationsspa.com</a><br><a href="https://cosmeticcreationsspa.com">cosmeticcreationsspa.com</a></p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    # Constructing the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject
    part = MIMEText(html_content, "html")
    message.attach(part)

    # Sending the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


nemail = "bamidele8885@gmail.com"
review_email(nemail)

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email_from_gmail(address, subject, body):
    port = 465  # For SSL
    password = "almausxxxx"
    sender_email = "almausem@gmail.com"
    receiver_email = address
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    context = ssl.create_default_context()
    html = "<html><body><p>"+body+"</p></body></html>"

    text = body.replace("<br>","\n")

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("almausem@gmail.com", password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

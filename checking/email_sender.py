from email.message import EmailMessage
import ssl#For security layer
import smtplib

class Email:
    def __init__(self,email_sender , email_receiver , passcode):
        self.email_sender=email_sender
        self.email_receiver = email_receiver
        self.passcode = passcode
    
    def send_mail(self , subject , body):
        em = EmailMessage()

        em['From'] = self.email_sender
        em['To'] = self.email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com' , 465 , context = context) as smtp:
            smtp.login(self.email_sender , self.passcode)
            smtp.sendmail(self.email_sender , self.email_receiver , em.as_string())
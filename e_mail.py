import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mysql.connector
import random



def mail(text,subject,cell,branch):
  connection = mysql.connector.connect(host='localhost',database='cb',user='root', password='vishnu@123')
  if connection.is_connected():
      cursor = connection.cursor()
      cursor.execute("SELECT username FROM credentialsadmin WHERE cell = %s AND branch = %s", (cell, branch))
      order = cursor.fetchall()
  else:
      print("report table problem")

  for row in order:
      email=row[0]
      def send_email(email,text,subject):
          sender_email = "vishnureddyemail937@gmail.com"
          password = "voau afxh yfax xfkl"
          subject = subject
          smtp_server = "smtp.gmail.com"
          port = 587
          
          message = MIMEMultipart()
          message["From"] = sender_email
          message["To"] = email
          message["Subject"] = subject

          html = f"""
          <html>
            <body>
            <p>{text}</p>
            </body>
          </html>
          """

          message.attach(MIMEText(html, "html"))

          with smtplib.SMTP(smtp_server, port) as server:
              server.starttls()
              server.login(sender_email, password)
              server.sendmail(sender_email, email, message.as_string())

      send_email(email,text,subject)
  connection.close()
def otp(email):
    # Email and SMTP configuration
    sender_email = "vishnureddyemail937@gmail.com"
    password = "voau afxh yfax xfkl"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # This might be different depending on your provider
    def generate_otp():
        return ''.join(random.choices('0123456789', k=6))
    otp = generate_otp()
    my=mysql.connector.connect(host="localhost",user='root',password='vishnu@123',database='cb')
    cursor = my.cursor()
    em=email
    
    cursor.execute("insert into otp values(%s,%s)",(em,otp))
    my.commit()
    cursor.close()
    my.close()
    receiver_email = email
    # Message configuration
    subject = 'otp noreply'
    body = f'Your OTP (One Time Password) is: {otp}. Please use this OTP to complete your verification process. Do not share this OTP with anyone for security reasons'
    # Create message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Enable encryption
        server.login(sender_email, password)  # Login to the server
        server.send_message(message)  # Send the email
    
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# FOR NOW --
# If using gmail - you have to give permissions for access to less secure apps via this link
# https://www.google.com/settings/security/lesssecureapps
# --

class Mail(object):
	def __init__(self, username, password, smtpServer):
		self.server = smtplib.SMTP(smtpserver, 587)
		self.server.ehlo()
		self.server.starttls()
		self.server.login(username, password)
		

	def sendMail(self, title, price, link, to_address):
		self.message = MIMEMultipart()
		self.message['Subject'] = title + ", cijena: " + price
		self.message['From'] = "NjuskaScrape"
		self.message['To'] = to_address
		self.text = MIMEText(link, 'plain')
		self.message.attach(self.text)
		try:
			self.server.send_message(self.message) 
		except SMTPException:
			print("Error: unable to send email")
		finally:
			self.server.quit()

		
		


# m = Mail("username", "password", "smtp.gmail.com")
# m.sendMail('PS4 nov, zapakiran', "2999.99", "www.njuskalo.hr/ps4", 'ivan.esterajher@ztm.hr')

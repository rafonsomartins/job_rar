import smtplib
from email.message import EmailMessage
from datetime import datetime
import subprocess
import socket

def send_failure_email(error_message):
	sender_email = "sender@email.com"
	receiver_email = "receiver@email.com"
	password = "sender_password"
	ip = socket.gethostbyname(socket.gethostname())

	subject = "Script Failure Notification"
	body = f"Dear User,\n\nThe Storage Procedure in {ip} failed to run properly at {datetime.now()}.\nError details:\n{error_message}"

	msg = EmailMessage()
	msg['From'] = sender_email
	msg['To'] = receiver_email
	msg['Subject'] = subject
	msg.set_content(body)

	try:
		with smtplib.SMTP('smtp.office365.com', 587) as server:
			server.starttls()
			server.login(sender_email, password)
			server.sendmail(sender_email, receiver_email, msg.as_string())
		print("Failure email sent.")
	except Exception as e:
		print(f"Failed to send email: {e}")

if __name__ == "__main__":
	print(f"Runned at: {datetime.now()}")

	try:
		result = subprocess.run([
			"python3",
			"/home/rum/pythonScripts/StorageProcedures/routine.py",
			"excel_to_read.xlsx",
			"SQL_table_name",
			"processed_file_name_without_extension",
			"connection_name",
			"replace" # or append
		], check=True)
	except subprocess.CalledProcessError as e:
		send_failure_email(f"Error while running subprocess: {e}")

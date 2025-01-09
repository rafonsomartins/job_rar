import socket
import mysql.connector
from mysql.connector import Error
import datetime
import logging
import threading
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

STATE_FILE = 'server_state.json'

logging.basicConfig(filename='server.log', level=logging.INFO,
					format='%(asctime)s - %(levelname)s - %(message)s')

# Email configuration
EMAIL_CONFIG = {
	'smtp_server': 'smtp.office365.com',
	'port': 587,
	'sender_email': 'rum@rara.pt',
	'password': 'Solp0rt0'
}

last_client_time = time.time()
notified = [False, False, False]

# Database configuration
DB_CONFIGS = {
	'database': 'Refinaria',
	'user': 'rum_db',
	'password': '12345',
	'host': 'localhost',
	'port': 3306,
	'allow_local_infile': True
}

# File paths for email recipients
EMAIL_LISTS = {
	60: "recipients_60_seconds.txt",
	3600: "recipients_1_hour.txt",
	21600: "recipients_6_hours.txt"
}

# TCP Server setup
HOST = '0.0.0.0'
PORT = 40110

time_lock = threading.Lock()


# Function to save the state in the file
def save_state():
	state = {
		'last_client_time': last_client_time,
		'notified': notified
	}
	try:
		with open(STATE_FILE, 'w') as f:
			json.dump(state, f)
			logging.info("Server state saved.")
	except Exception as e:
		logging.error(f"Error saving server state: {e}")


# Function to load state from the file
def load_state():
	global last_client_time, notified
	try:
		with open(STATE_FILE, 'r') as f:
			state = json.load(f)
			last_client_time = state.get('last_client_time', time.time())
			notified = state.get('notified', [False, False, False])
			logging.info("Server state loaded.")
	except FileNotFoundError:
		logging.info(f"No previous state file found, using default values.")
	except Exception as e:
		logging.error(f"Error loading server state: {e}")


# Function to read email addresses from a file
def get_recipients(file_path):
	try:
		with open(file_path, 'r') as file:
			return [line.strip() for line in file if line.strip()]
	except FileNotFoundError:
		logging.error(f"Email list file not found: {file_path}")
		return []
	except Exception as e:
		logging.error(f"Error reading email list file {file_path}: {e}")
		return []


# Function to send an email
def send_email(subject, message, recipients):
	if not recipients:
		logging.warning(f"No recipients specified for subject: {subject}")
		return
	try:
		server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['port'])
		server.starttls()
		server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['password'])
		
		for recipient in recipients:
			msg = MIMEMultipart()
			msg['From'] = EMAIL_CONFIG['sender_email']
			msg['To'] = recipient
			msg['Subject'] = subject
			msg.attach(MIMEText(message, 'plain'))
			server.sendmail(EMAIL_CONFIG['sender_email'], recipient, msg.as_string())
			logging.info(f"Email sent to {recipient}: {subject}")
			save_state()

	except Exception as e:
		logging.error(f"Failed to send email: {e}")
	finally:
		server.quit()


# Monitoring function to check idle time
def monitor_idle_time():
	global last_client_time, notified
	intervals = [60, 3600, 21600]
	subject = ["60 segundos", "1 hora", "6 horas"]

	while True:
		load_state()
		with time_lock:
			idle_time = time.time() - last_client_time

		if idle_time < intervals[0]:
			notified = [False, False, False]

		for i, interval in enumerate(intervals):
			if idle_time >= interval and not notified[i]:
				recipients = get_recipients(EMAIL_LISTS[interval])
				send_email(
					f"Falha de comunicação na Balança de Ramas.",
					f"O servidor perdeu a comunicação com a Balança de Ramas há {subject[i]}.",
					recipients
				)
				notified[i] = True
				save_state()


# Function to insert data into the database
def insert_data_to_db(formatted_data):
	try:
		conn = mysql.connector.connect(**DB_CONFIGS)
		cursor = conn.cursor()
		query = "INSERT INTO Balanca_Ramas (Movimento, timestamp_from_plc) VALUES (%s, %s)"
		cursor.execute(query, (formatted_data[0], formatted_data[1]))
		conn.commit()
		logging.info("Data inserted into the database.")
	except Error as e:
		logging.error(f"Database error: {e}")
	finally:
		if conn.is_connected():
			cursor.close()
			conn.close()


# Function to format incoming data
def format_data(raw_data):
	try:
		data_str = raw_data.strip().decode('utf-8')
		parts = data_str.split(';')
		if len(parts) != 2:
			raise ValueError("Invalid data format")
		measurement = float(parts[0]) / 10
		timestamp_unix = int(parts[1])
		timestamp = datetime.datetime.fromtimestamp(timestamp_unix).strftime("%Y-%m-%d %H:%M:%S")
		return measurement, timestamp
	except Exception as e:
		logging.error(f"Error formatting data: {e}")
		return None, None


def start_server():
	global last_client_time, notified

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
		server_socket.bind((HOST, PORT))
		server_socket.listen(5)
		logging.info(f"Server listening on {HOST}:{PORT}...")
		
		while True:
			client_socket, client_address = server_socket.accept()
			with time_lock:
				last_client_time = time.time()

			logging.info(f"Connection established with {client_address}")
			with client_socket:
				try:
					raw_data = client_socket.recv(1024)
					if not raw_data:
						logging.info("Client disconected.")
						break

					logging.info(f"Raw data received: {raw_data}")
					formatted_data = format_data(raw_data)
					logging.info(f"Formatted data: {formatted_data}")

					if formatted_data[0] is not None and formatted_data[1] is not None:
						insert_data_to_db(formatted_data)
					else:
						logging.info("Invalid data. Skipping insertion.")
					save_state()

				except Exception as e:
					logging.error(f"Error: {e}")


if __name__ == "__main__":
	logging.info("Starting the PLC data server...")
	monitor_thread = threading.Thread(target=monitor_idle_time, daemon=True)
	monitor_thread.start()
	load_state()
	start_server()

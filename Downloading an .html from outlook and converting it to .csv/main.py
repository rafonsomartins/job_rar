import pandas as pd
import subprocess
import os
from datetime import datetime
import time
import argparse


# Argument parsing
parser = argparse.ArgumentParser(description='Process some files.')
parser.add_argument('-path', type=str, required=True, help='Path to the HTML file')
args = parser.parse_args()

html_file_path = args.path
start_time = time.time()

tables_path = "output_file.htm"

# Pass the path to the subprocess calls
result = subprocess.run(["py", "first_trim.py", "-path", html_file_path, "-output", tables_path], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)

result = subprocess.run(["py", "convertion.py", "-path", tables_path], capture_output=True, text=True)
print(result.stdout)

try:
	merged_df = pd.read_csv("Conv.csv", delimiter=';', decimal=',', encoding='utf-8-sig')
except Exception as e:
	print(f"Sorry, something went wrong: {e}")
	exit(2)

# Extract timestamp from filename
filename = os.path.basename(html_file_path)
parts = filename.split('_')
if len(parts) >= 4:
	date_str = parts[3].replace('-', '/')
	print(date_str)
	time_str = parts[4].split('.')[0].replace('-', ':')
	print(time_str)
	timestamp = f"{date_str} {time_str}"
	print(timestamp)
	merged_df["timestamp"] = timestamp

try:
	old = pd.read_csv('../Pedidos/Pedidos.csv', delimiter=';')
	new = pd.concat([old, merged_df])
	if os.path.exists(tables_path):
		os.remove(tables_path)
	new.to_csv('../Pedidos/Pedidos.csv', sep=';', index=False, encoding='utf-8-sig', decimal=',')
	print("Conversion to CSV and concatenation completed successfully.")
	end_time = time.time()
	print(f"Execution time: {end_time - start_time} seconds")
except FileNotFoundError:
	merged_df.to_csv('../Pedidos/Pedidos.csv', sep=';', index=False, encoding='utf-8-sig', decimal=',')
	print("Conversion to CSV completed successfully.")
except Exception as e:
	print(f"Sorry, something went wrong: {e}")

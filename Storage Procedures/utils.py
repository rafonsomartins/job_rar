import os
import shutil
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import unidecode
import mysql.connector
import re

def strip_dataframe(df):
	"""Strip leading/trailing whitespace from all string columns."""
	for col in df.select_dtypes(include='object').columns:
		df[col] = df[col].str.strip()
		df[col] = df[col].apply(
			lambda x: str(x).lstrip('0') if isinstance(x, str) and not re.match(r'^\d{2}(\.|:)\d{2}\1\d{4}$', str(x)) else x
		)
		df[col] = df[col].astype(str).replace({'.00.0000': '00.00.0000'})
	df.columns = df.columns.str.strip()
	return df

def normalize_column_name(col_name):
	"""Normalize a column name by removing accents."""
	return unidecode.unidecode(col_name)

def normalize_columns(df):
	"""Apply normalization to all column names."""
	df.columns = [normalize_column_name(col) for col in df.columns]
	return df

def insert_with_pandas(file_path, table_name, db_config, mode='append'):
	"""Insert a CSV file into the database using pandas."""
	try:
		df = pd.read_csv(file_path, sep=';', encoding='ISO-8859-1', decimal=',', engine='python')
		df = strip_dataframe(df)
		df = normalize_columns(df)
		connection_string = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
		engine = create_engine(connection_string)
		df.to_sql(table_name, engine, if_exists=mode, index=False)
	except Exception as e:
		print(f"Error during data insertion: {e}")
		return 1
	finally:
		if engine:
			engine.dispose()
	return 0

def move_file(file_path, processed_folder, filename_prefix):
	"""Move a file to the processed folder with a timestamped filename."""
	if not os.path.exists(file_path):
		print(f"File {file_path} not found.")
		return

	creation_time = os.path.getmtime(file_path)
	creation_date = datetime.fromtimestamp(creation_time)
	formatted_date = creation_date.strftime('%d%m%Y_%H%M%S')
	processed_filename = f"{filename_prefix}_{formatted_date}.csv"
	processed_path = os.path.join(processed_folder, processed_filename)

	os.makedirs(processed_folder, exist_ok=True)
	try:
		shutil.move(file_path, processed_path)
		retries = 5
		while (os.path.exists(file_path) and retries):
			shutil.move(file_path, processed_path)
			retries -= 1
		if os.path.exists(file_path):
			print(f"File {filename_prefix} was processed but couldn't move it to {processed_path}")
		else:
			print(f"File successfully moved to {processed_path}")
	except Exception as e:
		print(f"Error moving file: {e}")

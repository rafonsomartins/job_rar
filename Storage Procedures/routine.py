from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import insert_with_pandas, move_file

DB_CONFIGS = {
	'connection_name': {
		'database': 'database_name',
		'user': 'user_db',
		'password': 'user_password',
		'host': 'host_ip',
		'port': 3306,
		'allow_local_infile': True
	},
	'connection_name2': {
		'database': 'db_name2',
		'user': 'user2_db',
		'password': 'user2_password',
		'host': 'host_ip',
		'port': 3306,
		'allow_local_infile': True
	}
}

def process_csv(input_file, table_name, processed_prefix, db_name, mode, processed_folder):
	if not os.path.exists(input_file):
		print(f"File {input_file} not found.")
		return

	db_config = DB_CONFIGS.get(db_name)
	if not db_config:
		print(f"No database configuration found for {db_name}.")
		return

	if insert_with_pandas(input_file, table_name, db_config, mode):
		return

	move_file(input_file, processed_folder, processed_prefix)

if __name__ == "__main__":
	args = sys.argv[1:]
	if len(args) != 5:
		print("Usage: python routine.py <input_file> <table_name> <processed_prefix> <db_name> <mode>")
		sys.exit(1)

	input_file, table_name, processed_prefix, db_name, mode = args
	processed_folder = "Folder/to/save/processed/files"

	process_csv(input_file, table_name, processed_prefix, db_name, mode, processed_folder)

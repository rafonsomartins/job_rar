import subprocess
import sys
from datetime import datetime

def run_script(script_name, log_file):
	current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	try:
		# correr com opção '-u' para forçar a print a descarregar o buffer (imprimir logo no terminal e não apenas quando o processo morrer)
		process = subprocess.Popen(["py", "-u", script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		with open(log_file, "a") as f:
			f.write(f"{current_time} - Iniciando a execução do script {script_name}.\n")
			for line in process.stdout:
				sys.stdout.write(line)

			stdout, stderr = process.communicate()
			if process.returncode == 0:
				f.write(f"{current_time} - Script {script_name} executado com sucesso.\n")
				print(stdout)
			else:
				f.write(f"{current_time} - Ocorreu um erro ao executar o script {script_name}.\n")
				if stderr:
					f.write(f"Erro:\n{stderr}\n")
				sys.exit(1)

	except subprocess.CalledProcessError as e:
		with open(log_file, "a") as f:
			f.write(f"{current_time} - Ocorreu um erro ao executar o script {script_name}.\n")
			f.write(f"Erro:\n{e.stderr}\n")

		print(f"Ocorreu um erro ao executar o script {script_name}:\n{e.stderr}")
		sys.exit(1)

script_to_run = "hope2.py"
script_routine = "routine.py"
log_file = r'../Job Z_LISTAGEM_ORDENS, Step 1/logs.txt'

run_script(script_to_run, log_file)
run_script(script_routine, log_file)

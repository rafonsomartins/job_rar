import os
import subprocess
import shutil

buffer_dir = "..\\Job Z_LISTAGEM_ORDENS, Step 1\\buffer"
history_dir = "..\\Job Z_LISTAGEM_ORDENS, Step 1\\HISTORY"

changed = 0

for file_name in os.listdir(buffer_dir):
	file_path = os.path.join(buffer_dir, file_name)
	history_file_path = os.path.join(history_dir, file_name)

	if os.path.isfile(file_path):
		if os.path.exists(history_file_path):
				os.remove(file_path)
				print(f"Arquivo {file_name} já existe em HISTORY. Removido do buffer.")
		else:
			subprocess.run(["py", "main.py", "-path", f"{file_path}"])
			shutil.move(file_path, os.path.join(history_dir, file_name))
			changed = 1

origem = r'C:\Users\rum\OneDrive - RAR Açucar, S.A\Documents\1_Projetos\4_Indicadores\Pedidos\Pedidos\Pedidos.csv'
destino = r'C:\Users\rum\RAR Açucar, S.A\RUM Workspace - Documentos\Pedidos.csv'

if changed:
	shutil.copy2(origem, destino)

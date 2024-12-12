import time
import tilia as tl
import pandas as pd
import pyautogui

def run_ksv5(ciclo, month, year, test=True):
	tl.enter_value("KSV5")
	time.sleep(0.2)
	tl.enter_value("RARA")
	tl.exit_if_not_window("Executar distrib.real: 1ª tela")
	pyautogui.typewrite(month)
	tl.press_key("tab", 2)
	pyautogui.typewrite(year)
	tl.press_key("tab", 2)
	if not test:
		tl.press_key("space")
	tl.press_key("tab", 3)
	pyautogui.typewrite(ciclo)
	tl.press_key("enter")
	time.sleep(0.1)
	tl.press_key("f8")
	tl.exit_if_not_window("Exibição Distribuição real cont.centros de custo Lista básica")
	message = tl.force_clipboard_content(0.0078125, 0.188194, 0.102734375, 0.188194, sap_paste=True)
	tl.press_key("esc")
	tl.press_key("enter")
	if message == "Processamento encerrado com avisos" or message == "O processamento foi encerrado sem erros":
		return True, message
	else:
		return False, message

def run_ksu5(ciclo):
	print("Here goes the KSU5")
	# tl.enter_value("KSU5")
	# time.sleep(0.2)
	# tl.enter_value("RARA")
	# tl.exit_if_not_window("Executar distrib.real: 1ª tela")

def end_program(output):
	output = pd.DataFrame(output)
	output.to_excel("output_file.xlsx", index=False)
	tl.close_sap()
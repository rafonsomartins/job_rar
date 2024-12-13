import time
import pandas as pd
import pyautogui
import tilia as tl

def fill_ass_cycle(name, window1, window2, cycle, month, year, test=True):
	rara = False
	tl.enter_value(name)
	if not tl.wait_for_window(window1, timeout=0.8, wait=0.2) and tl.wait_for_window("Definir área contab.custos", timeout=1.5):
		tl.enter_value("RARA")
		rara = True
	if rara:
		tl.exit_if_not_window(window1, wait=0.2)
	pyautogui.typewrite(month)
	tl.press_key("tab", 2)
	pyautogui.typewrite(year)
	tl.press_key("tab", 2)
	if not test:
		tl.press_key("space")
	tl.press_key("tab", 3)
	pyautogui.typewrite(cycle)
	tl.press_key("enter")
	time.sleep(0.3)
	tl.press_key("f8")
	if not tl.wait_for_window(window2, timeout=0.5):
		tl.press_key("f8")
	tl.exit_if_not_window(window2, timeout=30)
	message = tl.force_clipboard_content(0.00820313, 0.188194, 0.1007813, 0.188194, sap_paste=True)
	tl.press_key("esc")
	tl.press_key("enter")
	if message == "Processamento encerrado com avisos" or message == "O processamento foi encerrado sem erros":
		return True, message
	else:
		return False, message

def run_ass_cycle(name, cycle, month, year, test=True):
	if name == "KSV5":
		window1 = "Executar distrib.real: 1ª tela"
		window2 = "Exibição Distribuição real cont.centros de custo Lista básica"
	elif name == "KSU5":
		window1 = "Executar Rateio real: 1ª tela"
		window2 = "Exibição Rateio real contabilidade centros custo Lista básica"
	else:
		exit("Error: SAP transaction for assessment cycle not recognized by the program. Exiting with failure.")

	return fill_ass_cycle(name, window1, window2, cycle, month, year, test)

def end_program(sap_bot, output, output_file):
	output = pd.DataFrame(output)
	output.to_excel(output_file, index=False)
	sap_bot.close_sap()

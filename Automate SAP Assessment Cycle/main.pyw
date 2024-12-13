import time
import pandas as pd
import tilia as tl
from utils import end_program, run_ass_cycle
from interface import get_inputs

def main():
	username, password, month, year, test, input_file, output_file = get_inputs()

	rateios = pd.read_excel(input_file)

	sap_bot = tl.SAPAutomation(username, password)
	sap_bot.open_sap(username, password)

	output = []
	tl.mouse_click(0.371875, 0.3013889)
	for _, rateio in rateios.iterrows():
		if rateio['Transação executar'] == "KSV5" or rateio['Transação executar'] == "KSU5":
			res, message = run_ass_cycle(rateio["Transação executar"], rateio["Ciclo"], month, year, test)
			output.append({"Transação": rateio['Transação executar'], "Ciclo": rateio['Ciclo'], "Mensagem": message})
			if not res:
				end_program(sap_bot, output, output_file)
				exit(f"Error in {rateio['Transação executar']}: {rateio['Ciclo']}. Message: {message}. Exiting program.")
		else:
			exit("Error: SAP transaction for assessment cycle not recognized by the program. Exiting with failure.")
		sap_bot.go_to_main_page()

	end_program(sap_bot, output, output_file)

if __name__ == "__main__":
	start = time.time()
	main()

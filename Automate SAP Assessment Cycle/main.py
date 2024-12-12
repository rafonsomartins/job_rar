import time
import getpass
import pandas as pd
import tilia as tl
from utils import end_program, run_ksu5, run_ksv5

def main():
	username = input("SAP username: ")
	password = getpass.getpass("SAP password: ")
	month = input("Month: ")
	year = input("Year: ")
	test_input = input("Run in test mode [y or n]: ").lower()
	infile = input("infile: ")
	if test_input == "y" or test_input == "yes":
		test = True
	elif test_input == "n" or test_input == "no":
		test = False

	rateios = pd.read_excel(infile, sheet_name='3.4', index_col=None)
	rateios.columns = (['Transaction', 'Cicle'])

	output = []
	tl.open_sap(username, password)
	for _, rateio in rateios.iterrows():
		if rateio['Transaction'] == "KSV5":
			res, message = run_ksv5(rateio["Cicle"], month, year, True)
			output.append({"Transação": rateio['Transaction'], "Cicle": rateio['Cicle'], "Mensagem": message})
			if not res:
				end_program(output)
				exit(f"Error in {rateio['Transaction']}: {rateio['Cicle']}. Message: {message}. Exiting program.")
		elif rateio['Transaction'] == "KSU5":
			# run_ksu5(rateio["Cicle"])
			continue
		else:
			exit("Error: SAP transaction for assessment cycle not recognized by the program. Exiting with failure.")
		tl.go_to_main_page()
	end_program(output)

if __name__ == "__main__":
	start = time.time()
	main()
	print(f"\nProgram duration: {round(time.time()-start)} seconds")

import tkinter as tk
from tkinter import filedialog, messagebox

def get_inputs():
    def browse_input_file():
        file_path = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*"))
        )
        if file_path:
            input_file_entry.delete(0, tk.END)
            input_file_entry.insert(0, file_path)

    def browse_output_file():
        file_path = filedialog.asksaveasfilename(
            title="Select Output File",
            defaultextension=".xlsx",
            filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*"))
        )
        if file_path:
            output_file_entry.delete(0, tk.END)
            output_file_entry.insert(0, file_path)

    def submit():
        nonlocal username, password, month, year, test, input_file, output_file
        username = username_entry.get()
        password = password_entry.get()
        month = month_entry.get()
        year = year_entry.get()
        test = test_var.get()
        input_file = input_file_entry.get()
        output_file = output_file_entry.get()

        if not username or not password or not month or not year or not input_file or not output_file:
            messagebox.showerror("Error", "All fields are required.")
            return
        try:
            int(year)
            int(month)
        except ValueError:
            messagebox.showerror("Error", "Year and month must be numbers.")
            return

        root.destroy()

    root = tk.Tk()
    root.title("SAP Input Form")
    root.geometry("500x400")

    tk.Label(root, text="SAP Username:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
    username_entry = tk.Entry(root)
    username_entry.grid(row=0, column=1)

    tk.Label(root, text="SAP Password:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.grid(row=1, column=1)

    tk.Label(root, text="Month:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
    month_entry = tk.Entry(root)
    month_entry.grid(row=2, column=1)

    tk.Label(root, text="Year:").grid(row=3, column=0, sticky="e", padx=10, pady=5)
    year_entry = tk.Entry(root)
    year_entry.grid(row=3, column=1)

    tk.Label(root, text="Input File:").grid(row=4, column=0, sticky="e", padx=10, pady=5)
    input_file_entry = tk.Entry(root, width=30)
    input_file_entry.insert(0, "Input_file.xlsx")
    input_file_entry.grid(row=4, column=1)
    tk.Button(root, text="Browse", command=browse_input_file).grid(row=4, column=2, padx=5)

    tk.Label(root, text="Output File:").grid(row=5, column=0, sticky="e", padx=10, pady=5)
    output_file_entry = tk.Entry(root, width=30)
    output_file_entry.insert(0, "Output_file.xlsx")
    output_file_entry.grid(row=5, column=1)
    tk.Button(root, text="Browse", command=browse_output_file).grid(row=5, column=2, padx=5)

    test_var = tk.BooleanVar(value=True)
    tk.Checkbutton(root, text="Run in Test Mode", variable=test_var).grid(row=6, columnspan=2, pady=10)

    tk.Button(root, text="Submit", command=submit).grid(row=7, columnspan=3, pady=10)

    username = password = month = year = test = input_file = output_file = None
    root.mainloop()

    return username, password, month, year, test, input_file, output_file

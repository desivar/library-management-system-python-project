import tkinter as tk
from tkinter import messagebox
import database_functions as db
import datetime

# --- Functions ---


def add_patient_action():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    dob_str = dob_entry.get()
    gender = gender_entry.get()
    contact_number = contact_entry.get()
    address = address_entry.get()

    try:
        dob = datetime.datetime.strptime(dob_str, "%Y-%m-%d").date()
    except ValueError:
        messagebox.showerror(
            "Error", "Invalid Date of Birth format. Use YYYY-MM-DD."
        )
        return

    mydb = db.connect_db()
    if mydb is None:
        messagebox.showerror("Error", "Database connection failed.")
        return

    patient_id = db.record_patient(mydb, first_name, last_name, dob, gender,
                                   contact_number, address)
    mydb.close()

    if patient_id:
        messagebox.showinfo("Success", f"Patient added with ID: {patient_id}")
        clear_entries()
    else:
        messagebox.showerror("Error", "Failed to add patient.")


def find_patient_action():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    dob_str = dob_entry.get()

    try:
        dob = datetime.datetime.strptime(dob_str, "%Y-%m-%d").date()
    except ValueError:
        messagebox.showerror(
            "Error", "Invalid Date of Birth format. Use YYYY-MM-DD."
        )
        return

    mydb = db.connect_db()
    if mydb is None:
        messagebox.showerror("Error", "Database connection failed.")
        return

    patient_id = db.find_patient(
        mydb, first_name, last_name, dob)  # Pass date object
    mydb.close()

    if patient_id:
        patient_id_label.config(text=f"Patient ID: {patient_id}")
    else:
        messagebox.showinfo("Not Found", "No matching patient found.")
        patient_id_label.config(text="Patient ID:")


def edit_patient_action():
    try:
        patient_id_str = patient_id_entry.get()
        patient_id = int(patient_id_str)
    except ValueError:
        messagebox.showerror("Error", "Invalid Patient ID.")
        return

    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    dob_str = dob_entry.get()
    gender = gender_entry.get()
    contact_number = contact_entry.get()
    address = address_entry.get()

    try:
        dob = datetime.datetime.strptime(dob_str, "%Y-%m-%d").date()
    except ValueError:
        messagebox.showerror(
            "Error", "Invalid Date of Birth format. Use YYYY-MM-DD."
        )
        return

    mydb = db.connect_db()
    if mydb is None:
        messagebox.showerror("Error", "Database connection failed.")
        return

    if db.edit_patient(mydb, patient_id, first_name, last_name, dob, gender,
                       contact_number, address):
        messagebox.showinfo("Success", "Patient information updated.")
        clear_entries()
    else:
        messagebox.showerror("Error", "Failed to update patient information.")
    mydb.close()


def delete_patient_action():
    try:
        patient_id_str = patient_id_entry.get()
        patient_id = int(patient_id_str)
    except ValueError:
        messagebox.showerror("Error", "Invalid Patient ID.")
        return

    mydb = db.connect_db()
    if mydb is None:
        messagebox.showerror("Error", "Database connection failed.")
        return

    if db.delete_patient(mydb, patient_id):
        messagebox.showinfo("Success", "Patient deleted.")
        clear_entries()
        patient_id_label.config(text="Patient ID:")
    else:
        messagebox.showerror("Error", "Failed to delete patient.")
    mydb.close()


def clear_entries():
    patient_id_entry.delete(0, tk.END)
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    dob_entry.delete(0, tk.END)
    gender_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)


# --- GUI Setup ---
root = tk.Tk()
root.title("Library Management System")  # Or Clinic Lab Management
root.geometry("800x600")
root.resizable(True, True)

# --- Labels and Entry Fields ---
patient_id_label = tk.Label(root, text="Patient ID:")
patient_id_label.grid(row=0, column=0, sticky="w")
patient_id_entry = tk.Entry(root)
patient_id_entry.grid(row=0, column=1, sticky="ew")

first_name_label = tk.Label(root, text="First Name:")
first_name_label.grid(row=1, column=0, sticky="w")
first_name_entry = tk.Entry(root)
first_name_entry.grid(row=1, column=1, sticky="ew")

last_name_label = tk.Label(root, text="Last Name:")
last_name_label.grid(row=2, column=0, sticky="w")
last_name_entry = tk.Entry(root)
last_name_entry.grid(row=2, column=1, sticky="ew")

dob_label = tk.Label(root, text="Date of Birth (YYYY-MM-DD):")
dob_label.grid(row=3, column=0, sticky="w")
dob_entry = tk.Entry(root)
dob_entry.grid(row=3, column=1, sticky="ew")

gender_label = tk.Label(root, text="Gender:")
gender_label.grid(row=4, column=0, sticky="w")
gender_entry = tk.Entry(root)
gender_entry.grid(row=4, column=1, sticky="ew")

contact_label = tk.Label(root, text="Contact Number:")
contact_label.grid(row=5, column=0, sticky="w")
contact_entry = tk.Entry(root)
contact_entry.grid(row=5, column=1, sticky="ew")

address_label = tk.Label(root, text="Address:")
address_label.grid(row=6, column=0, sticky="w")
address_entry = tk.Entry(root)
address_entry.grid(row=6, column=1, sticky="ew")

# --- Buttons ---
add_button = tk.Button(root, text="Add Patient", command=add_patient_action)
add_button.grid(row=7, column=0, columnspan=2, pady=(10, 5))

find_button = tk.Button(root, text="Find Patient", command=find_patient_action)
find_button.grid(row=8, column=0, columnspan=2, pady=(5, 5))

edit_button = tk.Button(root, text="Edit Patient", command=edit_patient_action)
edit_button.grid(row=9, column=0, columnspan=2, pady=(5, 5))

delete_button = tk.Button(
    root, text="Delete Patient", command=delete_patient_action
)
delete_button.grid(row=10, column=0, columnspan=2, pady=(5, 10))

# --- Grid Configuration ---
root.grid_columnconfigure(1, weight=1)

root.mainloop()

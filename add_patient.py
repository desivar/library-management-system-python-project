import mysql.connector
import datetime


def connect_db():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="Desire",
            password="templo88",
            database="clinic_lab_management"
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
    return None


def record_patient(mydb, first_name, last_name, dob_str, gender,
                   contact_number, address):
    try:
        with mydb.cursor() as mycursor:
            if not first_name or not last_name:
                raise ValueError("First and last names are required.")
            try:
                dob = datetime.datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD.")
            if not contact_number:
                raise ValueError("Contact number is required.")

            sql = """
                INSERT INTO Patients (FirstName, LastName, DateOfBirth, Gender,
                ContactNumber, Address)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                first_name, last_name, dob, gender, contact_number, address
            )
            mycursor.execute(sql, values)
            mydb.commit()
            print("Patient record inserted successfully!")
            patient_id = mycursor.lastrowid
            return patient_id

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return None
    except ValueError as err:
        print(f"Validation Error: {err}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
    return None


def delete_patient(mydb, patient_id):
    try:
        with mydb.cursor() as mycursor:
            sql = "DELETE FROM Patients WHERE PatientID = %s"
            mycursor.execute(sql, (patient_id,))
            mydb.commit()
            if mycursor.rowcount > 0:
                print(f"{mycursor.rowcount} Patient record(s) "
                      "deleted successfully!")
                return True
            else:
                print("No matching patient records found.")
                return False
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
    return False


def edit_patient(mydb, patient_id, first_name, last_name, dob_str, gender,
                 contact_number, address):
    try:
        with mydb.cursor() as mycursor:
            try:
                dob = datetime.datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD.")

            sql = """
                UPDATE Patients
                SET FirstName = %s, LastName = %s, DateOfBirth = %s,
                Gender = %s,
                ContactNumber = %s, Address = %s
                WHERE PatientID = %s
            """
            values = (
                first_name, last_name, dob, gender,
                contact_number, address, patient_id
            )
            mycursor.execute(sql, values)
            mydb.commit()
            if mycursor.rowcount > 0:
                print(f"{mycursor.rowcount} Patient record(s) "
                      "updated successfully!")
                return True
            else:
                print("No matching patient records found.")
                return False
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return False
    except ValueError as err:
        print(f"Validation Error: {err}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
    return False


def find_patient(mydb, first_name, last_name, dob_str):
    try:
        with mydb.cursor() as mycursor:
            try:
                dob = datetime.datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD.")
            sql = (
                "SELECT PatientID FROM Patients WHERE FirstName = %s "
                "AND LastName = %s AND DateOfBirth = %s"
            )
            values = (first_name, last_name, dob)
            mycursor.execute(sql, values)
            result = mycursor.fetchone()
            if result:
                return result[0]
            else:
                return None

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return None
    except ValueError as err:
        print(f"Validation Error: {err}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# --- Main program ---
if __name__ == "__main__":
    mydb = connect_db()
    if mydb is None:
        exit()

    while True:
        print("\nClinic Lab Management Menu:")
        print("1. Add Patient")
        print("2. Delete Patient")
        print("3. Edit Patient")
        print("4. Find Patient")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            dob_str = input("Enter date of birth (YYYY-MM-DD): ")
            gender = input("Enter gender: ")
            contact_number = input("Enter contact number: ")
            address = input("Enter address: ")

            patient_id = record_patient(
                mydb, first_name, last_name, dob_str, gender,
                contact_number, address
            )
            if patient_id:
                print(f"Patient record added with PatientID: {patient_id}")
            else:
                print("Failed to add patient record.")

        elif choice == '2':
            patient_id = input("Enter PatientID to delete: ")
            if delete_patient(mydb, patient_id):
                print("Patient deleted.")
            else:
                print("Failed to delete patient.")

        elif choice == '3':
            patient_id = input("Enter PatientID to edit: ")
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            dob_str = input("Enter date of birth (YYYY-MM-DD): ")
            gender = input("Enter gender: ")
            contact_number = input("Enter contact number: ")
            address = input("Enter address: ")
            if edit_patient(mydb, patient_id, first_name, last_name,
                            dob_str, gender, contact_number, address):
                print("Patient information updated.")
            else:
                print("Failed to update patient information.")

        elif choice == '4':
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            dob_str = input("Enter date of birth (YYYY-MM-DD): ")
            patient_id = find_patient(mydb, first_name, last_name, dob_str)
            if patient_id:
                print(f"Patient found with PatientID: {patient_id}")
            else:
                print("No matching patient found.")

        elif choice == '5':
            mydb.close()
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

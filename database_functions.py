import mysql.connector


def connect_db():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="Desire",  # Replace with your MySQL user
            password="templo88",  # Replace with your MySQL password
            database="clinic_lab_management"  # Replace with your database name
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None


def record_patient(mydb, first_name, last_name, dob, gender, contact_number,
                   address):
    try:
        with mydb.cursor() as mycursor:
            sql = (
                "INSERT INTO Patients (FirstName, LastName, DateOfBirth, "
                "Gender, ContactNumber, Address) "
                "VALUES (%s, %s, %s, %s, %s, %s)"
            )
            values = (
                first_name, last_name, dob, gender, contact_number, address
            )
            mycursor.execute(sql, values)
            mydb.commit()
            patient_id = mycursor.lastrowid
            return patient_id

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def find_patient(mydb, first_name, last_name, dob):
    try:
        with mydb.cursor() as mycursor:
            sql = """
                SELECT PatientID
                FROM Patients
                WHERE FirstName = %s AND LastName = %s AND DateOfBirth = %s
            """
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
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def edit_patient(mydb, patient_id, first_name, last_name, dob, gender,
                 contact_number, address):
    try:
        with mydb.cursor() as mycursor:
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
                return True
            else:
                return False

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def delete_patient(mydb, patient_id):
    try:
        with mydb.cursor() as mycursor:
            sql = "DELETE FROM Patients WHERE PatientID = %s"
            mycursor.execute(sql, (patient_id,))
            mydb.commit()

            if mycursor.rowcount > 0:
                return True
            else:
                return False

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def record_appointment(mydb, patient_id, doctor_id, appointment_date,
                       appointment_time, notes):  # Corrected parameters
    try:
        with mydb.cursor() as mycursor:
            sql = """
                INSERT INTO Appointments (
                    PatientID, DoctorID, AppointmentDate,
                    AppointmentTime, Notes
                )
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                patient_id, doctor_id, appointment_date,
                appointment_time, notes
            )  # Corrected values
            mycursor.execute(sql, values)
            mydb.commit()
            return True  # Indicate success

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def list_doctors(mydb):
    try:
        with mydb.cursor() as mycursor:
            sql = "SELECT DoctorID, DoctorName FROM Doctors"  # Example query
            mycursor.execute(sql)
            doctors = mycursor.fetchall()
            return doctors

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

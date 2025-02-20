import tkinter as tk
import mysql.connector


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="lab_management"
    )


def main():
    root = tk.Tk()
    root.title("My Laboratory App")
    root.geometry("400x300")

    # Add your widgets here

    root.mainloop()


if __name__ == "__main__":
    main()
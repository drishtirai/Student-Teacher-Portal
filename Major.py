from tkinter import *
from tkinter import messagebox, ttk, filedialog
from PIL import ImageTk
import time
import pymysql
import pandas as pd

def connect_to_mysql():
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='Deepu@1234',
            database='teacher_portal'
        )
        return conn
    except pymysql.Error as err:
        messagebox.showerror('Error', f'Error connecting to MySQL: {err}')
        return None

def login():
    username = usernameEntry.get()
    password = passwordEntry.get()

    if username == '' or password == '':
        messagebox.showerror('Error', 'Fields cannot be empty')
    else:
        try:
            conn = connect_to_mysql()
            if conn:
                cursor = conn.cursor()
                query = "SELECT * FROM users WHERE username=%s AND password=%s"
                cursor.execute(query, (username, password))
                user = cursor.fetchone()

                if user:
                    messagebox.showinfo('Success', 'Welcome')
                    window.destroy()
                    open_student_management(user[0])  # Pass the user_id to student management
                else:
                    messagebox.showerror('Error', 'Please enter correct credentials')

                cursor.close()
                conn.close()
        except pymysql.Error as err:
            messagebox.showerror('Error', f'Error connecting to MySQL: {err}')

def signup():
    username = usernameEntry.get()
    password = passwordEntry.get()
    email = emailEntry.get()

    if username == '' or password == '' or email == '':
        messagebox.showerror('Error', 'Fields cannot be empty')
    else:
        try:
            conn = connect_to_mysql()
            if conn:
                cursor = conn.cursor()

                # Insert the user into the "users" table
                query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
                cursor.execute(query, (username, password, email))
                conn.commit()

                messagebox.showinfo('Success', 'Sign up successful! Please log in.')
                cursor.close()
                conn.close()
        except pymysql.Error as err:
            messagebox.showerror('Error', f'Error connecting to MySQL: {err}')

def open_student_management(user_id):
    # Create main window (root) for student management
    root = ttkthemes.ThemedTk()
    root.get_themes()
    root.set_theme('radiance')
    root.geometry('1280x700+0+0')
    root.resizable(False, False)
    root.title('Teacher Management System')

    # Connect to the database 
    connect_database()

    # Start the main event loop
    root.mainloop()

def iexit():
    result = messagebox.askyesno('Confirm', 'Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass

def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = studentTable.get_children()
    newlist = []
    for index in indexing:
        content = studentTable.item(index)
        datalist = content['values']
        newlist.append(datalist)

    table = pd.DataFrame(newlist, columns=['Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'DOB', 'Added Date', 'Added Time'])
    table.to_csv(url, index=False)
    messagebox.showinfo('Success', 'Data is saved successfully')

def toplevel_data(title, button_text, command):
    global idEntry, phoneEntry, nameEntry, emailEntry, addressEntry, genderEntry, dobEntry, screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(False, False)
    idLabel = Label(screen, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(screen, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(screen, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(screen, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    emailEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(screen, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    addressEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(screen, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    genderEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(screen, text='D.O.B', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    student_button = ttk.Button(screen, text=button_text, command=command)
    student_button.grid(row=7, columnspan=2, pady=15)
    if title == 'Update Student':
        indexing = studentTable.focus()
        content = studentTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        phoneEntry.insert(0, listdata[2])
        emailEntry.insert(0, listdata[3])
        addressEntry.insert(0, listdata[4])
        genderEntry.insert(0, listdata[5])
        dobEntry.insert(0, listdata[6])

def add_student():
    conn = connect_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, mobile, email, address, gender, dob, added_date, added_time) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (nameEntry.get(),
                        phoneEntry.get(),
                        emailEntry.get(),
                        addressEntry.get(),
                        genderEntry.get(),
                        dobEntry.get(),
                        time.strftime('%d/%m/%Y'),
                        time.strftime('%H:%M:%S')))
        conn.commit()
        messagebox.showinfo('Success', 'Student added successfully')
        cursor.close()
        conn.close()
        clear_entries()
        display_data()

def update_student():
    conn = connect_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s, "
                       "added_date=%s, added_time=%s WHERE id=%s",
                       (nameEntry.get(),
                        phoneEntry.get(),
                        emailEntry.get(),
                        addressEntry.get(),
                        genderEntry.get(),
                        dobEntry.get(),
                        time.strftime('%d/%m/%Y'),
                        time.strftime('%H:%M:%S'),
                        idEntry.get()))
        conn.commit()
        messagebox.showinfo('Success', 'Student updated successfully')
        cursor.close()
        conn.close()
        clear_entries()
        display_data()

def delete_student():
    conn = connect_database()
    if conn:
        cursor = conn.cursor()
        if not studentTable.selection():
            messagebox.showerror("Error", "Please select a student to delete")
        else:
            result = messagebox.askquestion("Confirm Delete", "Are you sure you want to delete this record?")
            if result == 'yes':
                selected_item = studentTable.selection()[0]  # Get the selected item's ID
                cursor.execute("DELETE FROM students WHERE id=%s", studentTable.set(selected_item)['Id'])
                conn.commit()
                messagebox.showinfo('Success', 'Student deleted successfully')
                display_data()
        cursor.close()
        conn.close()

def search_student():
    conn = connect_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE " + str(searchBy.get()) + " LIKE '%" + str(searchText.get()) + "%'")
        records = cursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        for row in records:
            studentTable.insert('', 'end', values=row)
        cursor.close()
        conn.close()

def clear_entries():
    idEntry.delete(0, END)
    nameEntry.delete(0, END)
    phoneEntry.delete(0, END)
    emailEntry.delete(0, END)
    addressEntry.delete(0, END)
    genderEntry.delete(0, END)
    dobEntry.delete(0, END)

def display_data():
    conn = connect_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        records = cursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        for row in records:
            studentTable.insert('', 'end', values=row)
        cursor.close()
        conn.close()

def connect_database():
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='Deepu@1234',
            database='teacher_portal'
        )
        return conn
    except pymysql.Error as err:
        messagebox.showerror('Error', f'Error connecting to MySQL: {err}')
        return None

# GUI Part for Login and Signup

window = Tk()
window.geometry('1280x700+0+0')
window.resizable(False, False)
window.title('Teacher Management System')

loginFrame = Frame(window)  # Create the loginFrame
loginFrame.pack()

# ... (previously defined GUI code)

usernameLabel = Label(loginFrame, text='Username', font=('times new roman', 20, 'bold'))
usernameLabel.grid(row=1, column=0, pady=15, padx=30, sticky=W)
usernameEntry = Entry(loginFrame, font=('roman', 15, 'bold'), width=24)
usernameEntry.grid(row=1, column=1, pady=15, padx=10)

passwordLabel = Label(loginFrame, text='Password', font=('times new roman', 20, 'bold'))
passwordLabel.grid(row=2, column=0, pady=15, padx=30, sticky=W)
passwordEntry = Entry(loginFrame, font=('roman', 15, 'bold'), width=24, show='*')
passwordEntry.grid(row=2, column=1, pady=15, padx=10)

loginButton = Button(loginFrame, text='Login', font=('times new roman', 14, 'bold'), width=15
                     , fg='white', bg='cornflowerblue', activebackground='cornflowerblue',
                     activeforeground='white', cursor='hand2', command=login)
loginButton.grid(row=4, column=1, pady=10)

signupButton = Button(loginFrame, text='Sign Up', font=('times new roman', 14, 'bold'), width=15
                      , fg='white', bg='green', activebackground='green',
                      activeforeground='white', cursor='hand2', command=signup)
signupButton.grid(row=4, column=0, pady=10)

# ... (previously defined GUI code)

# Start the main event loop for login and signup
window.mainloop()

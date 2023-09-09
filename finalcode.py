from tkinter import *
from tkinter import messagebox
from tkinter import ttk, messagebox, filedialog
from PIL import ImageTk
import ttkthemes
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
                    # Close the login window
                    window.destroy()
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

                # Get the user ID of the newly inserted user
                user_id = cursor.lastrowid

                # Insert the student information along with the associated user ID into the "students" table
                query = "INSERT INTO students (user_id, name, mobile, email, address, gender, dob) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (user_id, nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get()))
                conn.commit()

                messagebox.showinfo('Success', 'Sign up successful! Please log in.')
                cursor.close()
                conn.close()
        except pymysql.Error as err:
            messagebox.showerror('Error', f'Error connecting to MySQL: {err}')


def forgot_password():
    messagebox.showinfo('Forgot Password', 'Please contact support to reset your password.')

window = Tk()

window.geometry('1280x700+0+0')
window.resizable(False, False)

backgroundImage = ImageTk.PhotoImage(file='bg.jpg')
bgLabel = Label(window, image=backgroundImage)
bgLabel.place(x=0, y=0)

loginFrame = Frame(window, bg='white')
loginFrame.place(x=400, y=150)

logoImage = PhotoImage(file='logo.png')
logoLabel = Label(loginFrame, image=logoImage)
logoLabel.grid(row=0, column=0, columnspan=2, pady=10)

usernameImage = PhotoImage(file='user.png')
usernameLabel = Label(loginFrame, image=usernameImage, text='Username', compound=LEFT
                      , font=('times new roman', 20, 'bold'), bg='white')
usernameLabel.grid(row=1, column=0, pady=10, padx=20)

usernameEntry = Entry(loginFrame, font=('times new roman', 20, 'bold'), bd=5, fg='royalblue')
usernameEntry.grid(row=1, column=1, pady=10, padx=20)

passwordImage = PhotoImage(file='password.png')
passwordLabel = Label(loginFrame, image=passwordImage, text='Password', compound=LEFT
                      , font=('times new roman', 20, 'bold'), bg='white')
passwordLabel.grid(row=2, column=0, pady=10, padx=20)

passwordEntry = Entry(loginFrame, font=('times new roman', 20, 'bold'), bd=5, fg='royalblue', show='*')
passwordEntry.grid(row=2, column=1, pady=10, padx=20)

emailImage = PhotoImage(file='email.png')
emailLabel = Label(loginFrame, image=emailImage, text='Email', compound=LEFT
                      , font=('times new roman', 20, 'bold'), bg='white')
emailLabel.grid(row=3, column=0, pady=10, padx=20)

emailEntry = Entry(loginFrame, font=('times new roman', 20, 'bold'), bd=5, fg='royalblue')
emailEntry.grid(row=3, column=1, pady=10, padx=20)

loginButton = Button(loginFrame, text='Login', font=('times new roman', 14, 'bold'), width=15
                     , fg='white', bg='cornflowerblue', activebackground='cornflowerblue',
                     activeforeground='white', cursor='hand2', command=login)
loginButton.grid(row=4, column=1, pady=10)

signupButton = Button(loginFrame, text='Sign Up', font=('times new roman', 14, 'bold'), width=15
                      , fg='white', bg='green', activebackground='green',
                      activeforeground='white', cursor='hand2', command=signup)
signupButton.grid(row=4, column=0, pady=10)

forgotPasswordButton = Button(loginFrame, text='Forgot Password?', font=('times new roman', 12), fg='blue', bg='white',
                              bd=0, cursor='hand2', command=forgot_password)
forgotPasswordButton.grid(row=5, columnspan=2, pady=10)
window.mainloop()

# Student Management Functionality Part

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

def sort_column(col):
    items = studentTable.get_children('')
    items = sorted(items, key=lambda x: studentTable.set(x, col))
    studentTable.delete(*studentTable.get_children())
    for item in items:
        studentTable.insert('', END, values=studentTable.item(item)['values'])

def update_data():
    query = 'update student set name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s, date=%s, time=%s where id=%s'
    mycursor.execute(query, (nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(),
                             genderEntry.get(), dobEntry.get(), date, currenttime, idEntry.get()))
    con.commit()
    messagebox.showinfo('Success', f'Id {idEntry.get()} is modified successfully', parent=screen)
    screen.destroy()
    show_student()
    toplevel_data('Update Student', 'Update', update_data)

def show_student():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)

def delete_student():
    indexing = studentTable.focus()
    if indexing:
        result = messagebox.askyesno('Confirm Delete', 'Do you want to delete this student?', parent=root)
        if result:
            content = studentTable.item(indexing)
            content_id = content['values'][0]
            query = 'delete from student where id=%s'
            mycursor.execute(query, content_id)
            con.commit()
            messagebox.showinfo('Deleted', f'Id {content_id} is deleted successfully')
            query = 'select * from student'
            mycursor.execute(query)
            fetched_data = mycursor.fetchall()
            studentTable.delete(*studentTable.get_children())
            for data in fetched_data:
                studentTable.insert('', END, values=data)
    else:
        messagebox.showwarning('No Selection', 'Please select a student to delete.', parent=root)

def search_data():
    query = 'select * from student where id=%s or name=%s or email=%s or mobile=%s or address=%s or gender=%s or dob=%s'
    mycursor.execute(query, (idEntry.get(), nameEntry.get(), emailEntry.get(), phoneEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get()))
    studentTable.delete(*studentTable.get_children())
    fetched_data = mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('', END, values=data)

def add_data():
    if idEntry.get() == '' or nameEntry.get() == '' or phoneEntry.get() == '' or emailEntry.get() == '' or addressEntry.get() == '' or genderEntry.get() == '' or dobEntry.get() == '':
        messagebox.showerror('Error', 'All Fields are required', parent=screen)
    else:
        try:
            query = 'insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query, (idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(),
                                     genderEntry.get(), dobEntry.get(), date, currenttime))
            con.commit()
            messagebox.showinfo('Success', f'Id {idEntry.get()} is added successfully', parent=screen)
            screen.destroy()
            show_student()
            toplevel_data('Add Student', 'Add', add_data)
        except pymysql.IntegrityError:
            messagebox.showerror('Error', 'Id cannot be repeated', parent=screen)
            return

# GUI Part
root = ttkthemes.ThemedTk()

root.get_themes()
root.set_theme('radiance')

root.geometry('1174x680+0+0')
root.resizable(0, 0)
root.title('Teacher Management System')

datetimeLabel = Label(root, font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=5, y=5)
date = time.strftime('%d/%m/%Y')
currenttime = time.strftime('%H:%M:%S')
datetimeLabel.config(text=f'   Date: {date}\nTime: {currenttime}')

s = 'Teacher Management System'
count = 0
text = ''
def slider():
    global text, count
    text = text + s[count]
    sliderLabel.config(text=text)
    count += 1
    if count >= len(s):
        count = 0
        text = ''
    sliderLabel.after(300, slider)

sliderLabel = Label(root, font=('arial', 28, 'italic bold'), width=30)
sliderLabel.place(x=200, y=0)
slider()

leftFrame = Frame(root)
leftFrame.place(x=50, y=80, width=300, height=600)

logo_image = PhotoImage(file='student.png')
logo_Label = Label(leftFrame, image=logo_image)
logo_Label.grid(row=0, column=0)

addstudentButton = ttk.Button(leftFrame, text='Add Student', width=25, command=lambda: toplevel_data('Add Student', 'Add', add_data))
addstudentButton.grid(row=1, column=0, pady=20)

searchstudentButton = ttk.Button(leftFrame, text='Search Student', width=25, command=lambda: toplevel_data('Search Student', 'Search', search_data))
searchstudentButton.grid(row=2, column=0, pady=20)

deletestudentButton = ttk.Button(leftFrame, text='Delete Student', width=25, command=delete_student)
deletestudentButton.grid(row=3, column=0, pady=20)

updatestudentButton = ttk.Button(leftFrame, text='Update Student', width=25, command=lambda: toplevel_data('Update Student', 'Update', update_data))
updatestudentButton.grid(row=4, column=0, pady=20)

showstudentButton = ttk.Button(leftFrame, text='Show Student', width=25, command=show_student)
showstudentButton.grid(row=5, column=0, pady=20)

exportstudentButton = ttk.Button(leftFrame, text='Export data', width=25, command=export_data)
exportstudentButton.grid(row=6, column=0, pady=20)

exitButton = ttk.Button(leftFrame, text='Exit', width=25, command=iexit)
exitButton.grid(row=7, column=0, pady=20)

rightFrame = Frame(root)
rightFrame.place(x=350, y=80, width=820, height=600)

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

studentTable = ttk.Treeview(rightFrame, columns=('Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'D.O.B', 'Added Date', 'Added Time'),
                          xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)

studentTable.pack(expand=1, fill=BOTH)

studentTable.heading('Id', text='Id', command=lambda: sort_column('Id'))
studentTable.heading('Name', text='Name', command=lambda: sort_column('Name'))
studentTable.heading('Mobile', text='Mobile No', command=lambda: sort_column('Mobile'))
studentTable.heading('Email', text='Email Address', command=lambda: sort_column('Email'))
studentTable.heading('Address', text='Address', command=lambda: sort_column('Address'))
studentTable.heading('Gender', text='Gender', command=lambda: sort_column('Gender'))
studentTable.heading('D.O.B', text='D.O.B', command=lambda: sort_column('D.O.B'))
studentTable.heading('Added Date', text='Added Date', command=lambda: sort_column('Added Date'))
studentTable.heading('Added Time', text='Added Time', command=lambda: sort_column('Added Time'))

studentTable.column('Id', width=50, anchor=CENTER)
studentTable.column('Name', width=200, anchor=CENTER)
studentTable.column('Email', width=300, anchor=CENTER)
studentTable.column('Mobile', width=200, anchor=CENTER)
studentTable.column('Address', width=300, anchor=CENTER)
studentTable.column('Gender', width=100, anchor=CENTER)
studentTable.column('D.O.B', width=200, anchor=CENTER)
studentTable.column('Added Date', width=200, anchor=CENTER)
studentTable.column('Added Time', width=200, anchor=CENTER)

style = ttk.Style()

style.configure('Treeview', rowheight=40, font=('arial', 12, 'bold'), fieldbackground='white', background='white')
style.configure('Treeview.Heading', font=('arial', 14, 'bold'), foreground='red')

studentTable.config(show='headings')
def connect_database():
    global mycursor, con
    try:
        con = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='Deepu@1234',
            database='teacher_portal'
        )
        mycursor = con.cursor()

        query = 'CREATE DATABASE IF NOT EXISTS teacher_portal'
        mycursor.execute(query)

        query = 'USE teacher_portal'
        mycursor.execute(query)

        query = 'CREATE TABLE IF NOT EXISTS student (id INT NOT NULL PRIMARY KEY, name VARCHAR(30), mobile VARCHAR(10), email VARCHAR(30),' \
                'address VARCHAR(100), gender VARCHAR(20), dob VARCHAR(20), date VARCHAR(50), time VARCHAR(50))'
        mycursor.execute(query)

        addstudentButton.config(state=NORMAL)
        searchstudentButton.config(state=NORMAL)
        updatestudentButton.config(state=NORMAL)
        showstudentButton.config(state=NORMAL)
        exportstudentButton.config(state=NORMAL)
        deletestudentButton.config(state=NORMAL)

    except pymysql.Error:
        messagebox.showerror('Error', 'Invalid Details')
        return

# ... (previously defined functions)

def add_data():
    if idEntry.get() == '' or nameEntry.get() == '' or phoneEntry.get() == '' or emailEntry.get() == '' or addressEntry.get() == '' or genderEntry.get() == '' or dobEntry.get() == '':
        messagebox.showerror('Error', 'All Fields are required', parent=screen)
    else:
        try:
            query = 'INSERT INTO student VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            mycursor.execute(query, (
                idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(),
                genderEntry.get(), dobEntry.get(), date, currenttime))
            con.commit()
            messagebox.showinfo('Success', f'Id {idEntry.get()} is added successfully', parent=screen)
            result = messagebox.askyesno('Confirm', 'Do you want to clean the form?', parent=screen)
            if result:
                idEntry.delete(0, END)
                nameEntry.delete(0, END)
                phoneEntry.delete(0, END)
                emailEntry.delete(0, END)
                addressEntry.delete(0, END)
                genderEntry.delete(0, END)
                dobEntry.delete(0, END)
            else:
                pass

            show_student()

        except pymysql.IntegrityError:
            messagebox.showerror('Error', 'Id cannot be repeated', parent=screen)
            return

# ... (previously defined functions)

# GUI Part
root = ttkthemes.ThemedTk()

# ... (previously defined GUI code)




# Create main window (root)
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry('1280x700+0+0')
root.resizable(False, False)
root.title('Teacher Management System')

# ... (previously defined GUI code for the login/signup part)

# Function to switch between login and signup frames
def switch_frame():
    if signup_frame.winfo_ismapped():
        login_frame.grid(row=0, column=0, padx=100, pady=50)
        signup_frame.grid_remove()
    else:
        signup_frame.grid(row=0, column=0, padx=100, pady=50)
        login_frame.grid_remove()

# ... (previously defined GUI code for the student management part)

# Connect to the database
connect_database()

# Start the main event loop
root.mainloop()

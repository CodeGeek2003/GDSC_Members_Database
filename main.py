import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

conn = sqlite3.connect('members.db')
cursor = conn.cursor()

# Create the members table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        member_id TEXT,
        email TEXT,
        phone_number TEXT,
        points INTEGER
    )
''')
conn.commit()

def display_points_table():
    cursor.execute('SELECT * FROM members ORDER BY points DESC')
    members = cursor.fetchall()

    points_window = tk.Tk()
    points_window.title('Members by Points')

    tree = ttk.Treeview(points_window)
    tree['columns'] = ('name', 'member_id', 'email', 'phone_number', 'points')
    tree.heading('#0', text='ID')
    tree.heading('name', text='Member Name')
    tree.heading('member_id', text='Member ID')
    tree.heading('email', text='Email')
    tree.heading('phone_number', text='Phone Number')
    tree.heading('points', text='Points')

    for member in members:
        tree.insert(parent='', index='end', iid=member[0], text=member[0], values=(member[1], member[2], member[3], member[4], member[5]))

    tree.pack(expand=True, fill='both')

    points_window.mainloop()

# search for a member by phone number
def search_member():
    def show_member_info():
        phone_number = entry_phone.get()
        cursor.execute('SELECT * FROM members WHERE phone_number=?', (phone_number,))
        member = cursor.fetchone()
        if member:
            member_info_window = tk.Tk()
            member_info_window.title('Member Information')

            info_label = tk.Label(member_info_window, text=f'Member Name: {member[1]}\nMember ID: {member[2]}\nEmail: {member[3]}\nPhone Number: {member[4]}\nPoints: {member[5]}')
            info_label.pack()

            member_info_window.mainloop()
        else:
            messagebox.showinfo('Member Information', 'Member not found.')

    phone_window = tk.Tk()
    phone_window.title('Search Member by Phone Number')

    # Entry for phone number search
    label_phone = tk.Label(phone_window, text='Enter phone number:')
    label_phone.pack()

    entry_phone = tk.Entry(phone_window)
    entry_phone.pack()

    # Search button
    btn_search_phone = tk.Button(phone_window, text='Search', command=show_member_info)
    btn_search_phone.pack()

    phone_window.mainloop()

# display all members
def display_all_members_table():
    cursor.execute('SELECT * FROM members')
    members = cursor.fetchall()

    all_members_window = tk.Tk()
    all_members_window.title('All Members')

    tree = ttk.Treeview(all_members_window)
    tree['columns'] = ('name', 'member_id', 'email', 'phone_number', 'points')
    tree.heading('#0', text='ID')
    tree.heading('name', text='Member Name')
    tree.heading('member_id', text='Member ID')
    tree.heading('email', text='Email')
    tree.heading('phone_number', text='Phone Number')
    tree.heading('points', text='Points')

    for member in members:
        tree.insert(parent='', index='end', iid=member[0], text=member[0], values=(member[1], member[2], member[3], member[4], member[5]))

    tree.pack(expand=True, fill='both')

    all_members_window.mainloop()

# add a new member
def add_new_member():
    def save_member():
        name = entry_name.get()
        phone_number = entry_phone.get()
        member_id = entry_member_id.get()
        email = entry_email.get()
        points = 0

        cursor.execute('INSERT INTO members (name, member_id, email, phone_number, points) VALUES (?, ?, ?, ?, ?)', (name, member_id, email, phone_number, points))
        conn.commit()
        messagebox.showinfo('Success', 'Member added successfully.')
        new_member_window.destroy()

    new_member_window = tk.Tk()
    new_member_window.title('Add New Member')

    # Entry fields for member details
    label_name = tk.Label(new_member_window, text='Member Name:')
    label_name.pack()
    entry_name = tk.Entry(new_member_window)
    entry_name.pack()

    label_phone = tk.Label(new_member_window, text='Phone Number:')
    label_phone.pack()
    entry_phone = tk.Entry(new_member_window)
    entry_phone.pack()

    label_member_id = tk.Label(new_member_window, text='Student ID:')
    label_member_id.pack()
    entry_member_id = tk.Entry(new_member_window)
    entry_member_id.pack()

    label_email = tk.Label(new_member_window, text='Email:')
    label_email.pack()
    entry_email = tk.Entry(new_member_window)
    entry_email.pack()

    btn_save = tk.Button(new_member_window, text='Save', command=save_member)
    btn_save.pack()

    new_member_window.mainloop()

# sign-in function
def sign_in():
    if entry_username.get() == 'GDSC FUE' and entry_password.get() == 'gdsc2023':
        sign_in_window.destroy()

        main_window = tk.Tk()
        main_window.title('GDSC FUE Members')

        btn_points = tk.Button(main_window, text='Display Points', command=display_points_table)
        btn_points.pack()

        btn_search = tk.Button(main_window, text='Search Member by Phone Number', command=search_member)
        btn_search.pack()

        btn_all_members = tk.Button(main_window, text='Display All Members', command=display_all_members_table)
        btn_all_members.pack()

        btn_add_member = tk.Button(main_window, text='Add New Member', command=add_new_member)
        btn_add_member.pack()

        main_window.mainloop()
    else:
        messagebox.showerror('Invalid Credentials', 'Invalid username or password.')

# GUI Setup for sign-in
sign_in_window = tk.Tk()
sign_in_window.title('Sign In')

# Username and Password Entry
label_username = tk.Label(sign_in_window, text='Username:')
label_username.pack()
entry_username = tk.Entry(sign_in_window)
entry_username.pack()

label_password = tk.Label(sign_in_window, text='Password:')
label_password.pack()
entry_password = tk.Entry(sign_in_window, show='*')
entry_password.pack()

btn_signin = tk.Button(sign_in_window, text='Sign In', command=sign_in)
btn_signin.pack()

sign_in_window.mainloop()

from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
from json.decoder import JSONDecodeError
import pandas

FONT = ("HP Simplified", 11, 'normal')
BACKGROUND = 'BlanchedAlmond'


# ---------------------------- RESET FUNCTIONS ------------------------------- #
def in_focus(entry_item):
    """Resets the entry field when in focus"""
    entry_item.delete(0, END)
    entry_item.config(fg='black')


def out_focus(entry_item, text):
    """Resets the entry field when out of focus"""
    entry_item.delete(0, END)
    entry_item.config(fg='grey')
    if text == 'website':
        entry_item.insert(0, 'Enter a Website or App name.')
    elif text == 'email':
        entry_item.insert(0, 'Enter your email id.')
    else:
        entry_item.insert(0, 'Enter or generate a password.')


def all_reset():
    """Resets all the fields"""
    website_input.focus()
    in_focus(website_input)
    out_focus(email_input, 'email')
    out_focus(password_input, 'password')
    pyperclip.copy('')


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """Generates a strong password"""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
               'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    pass_letters = [choice(letters) for _ in range(randint(8, 10))]
    pass_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    pass_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password = pass_letters + pass_symbols + pass_numbers
    shuffle(password)
    password = ''.join(password)
    in_focus(password_input)
    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- EVENT LISTENERS ------------------------------- #
def on_website_click(event):
    """Gets called whenever website entry is clicked"""
    if website_input.get() == 'Enter a Website or App name.':
        in_focus(website_input)


def on_website_out(event):
    """Gets called whenever website entry is clicked out"""
    if website_input.get() == '':
        out_focus(website_input, 'website')


def on_email_click(event):
    """Gets called whenever email entry is clicked"""
    if email_input.get() == 'Enter your email id.':
        in_focus(email_input)


def on_email_out(event):
    """Gets called whenever email entry is clicked out"""
    if email_input.get() == '':
        out_focus(email_input, 'email')


def on_pass_click(event):
    """Gets called whenever password entry is clicked"""
    if password_input.get() == 'Enter or generate a password.':
        in_focus(password_input)


def on_pass_out(event):
    """Gets called whenever password entry is clicked out"""
    if password_input.get() == '':
        out_focus(password_input, 'password')


# ---------------------------- SAVE PASSWORD ------------------------------- #
def dump_or_create_and_dump(data):
    """Writes data in a json file if file is present otherwise creates a new file before writing"""
    with open('data.json', 'w') as existing_data:
        json.dump(data, existing_data, indent=4)


def invalid_data():
    """Shows invalid data message box if user leaves any fields empty"""
    messagebox.showwarning(title='Invalid Data', message="Don't leave any fields empty")


def save_password():
    """Saves website, email and password data locally if all conditions are met"""
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {website: {'email': email, 'password': password, }}
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        invalid_data()
    elif window.focus_get() == password_input and (website == 'Enter a Website or App name.' or
                                                   email == 'Enter your email id.'):
        invalid_data()
    elif window.focus_get() == website_input and (password == 'Enter or generate a password.' or
                                                  email == 'Enter your email id.'):
        invalid_data()
    elif window.focus_get() == email_input and (website == 'Enter a Website or App name.' or
                                                password == 'Enter or generate a password.'):
        invalid_data()
    else:
        is_ok = messagebox.askokcancel(title=website, message=f'Here are the details: \nEmail: {email}\n'
                                                              f'Password: {password}'f'\nIs it ok to save?')
        if is_ok:
            try:
                with open('data.json', 'r') as existing_data:
                    data = json.load(existing_data)  # Reads existing json file data
            except (FileNotFoundError, JSONDecodeError):
                dump_or_create_and_dump(new_data)  # creates new file if it is not present and writes into it
            else:
                if website in data:
                    update = messagebox.askyesno(title='Data already exists',
                                                 message=f'There is already a password saved for {website}.\n'
                                                         f'Would you like to overwrite?')
                    if update:
                        data.update(new_data)  # Updates existing data with new data
                        dump_or_create_and_dump(data)  # Writes into the json file
                else:
                    data.update(new_data)  # Updates existing data with new data
                    dump_or_create_and_dump(data)  # Writes into the json file
            finally:
                website_input.focus()
                in_focus(website_input)
                out_focus(email_input, 'email')
                out_focus(password_input, 'password')


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def find_password():
    """Searches the data file for any existing details"""
    website = website_input.get()
    if website == '':
        messagebox.showwarning(title='Blank Field', message='Please enter a website name')
    else:
        try:
            existing_data = pandas.read_json('data.json')
        except ValueError:
            messagebox.showinfo(title='No data available', message='No data file found. Try saving some details.')
        else:
            if website in existing_data:
                yes_or_no = messagebox.askyesno(title=website,
                                                message=f'This website or app login details are available:\n'
                                                        f'Email: {existing_data[website].email}\n'
                                                        f'Password: {existing_data[website].password}\n'
                                                        f'Do you want to copy the password?')
                if yes_or_no:
                    pyperclip.copy(existing_data[website].password)
            else:
                messagebox.showinfo(title='No data available', message=f'No details for {website} exists')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50, bg='BlanchedAlmond')
window.resizable(width=False, height=False)
canvas = Canvas(width=200, height=200, bg=BACKGROUND, highlightthickness=0)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Website Label
website_label = Label(text='Website:', font=FONT, bg=BACKGROUND)
website_label.grid(column=0, row=1)

# Email Label
email_label = Label(text='Email/Username:', font=FONT, bg=BACKGROUND)
email_label.grid(column=0, row=2)

# Password Label
password_label = Label(text='Password:', font=FONT, bg=BACKGROUND)
password_label.grid(column=0, row=3)

# Website Input
website_input = Entry(width=24, font=FONT)
website_input.focus()
website_input.bind('<FocusIn>', on_website_click)
website_input.bind('<FocusOut>', on_website_out)
website_input.grid(column=1, row=1, sticky="EW")

# Email Input
email_input = Entry(width=40, font=FONT)
out_focus(email_input, 'email')
email_input.bind('<FocusIn>', on_email_click)
email_input.bind('<FocusOut>', on_email_out)
email_input.grid(column=1, row=2, columnspan=2, sticky="EW")

# Password Input
password_input = Entry(width=24, font=FONT)
password_input.grid(column=1, row=3, sticky="EW")
out_focus(password_input, 'password')
password_input.bind('<FocusIn>', on_pass_click)
password_input.bind('<FocusOut>', on_pass_out)

# Generate Password Button
generate_button = Button(text='Generate Password', font=FONT, command=generate_password, bg='honeydew2',
                         activebackground='honeydew3')
generate_button.grid(column=2, row=3, sticky="EW")

# Add Password Button
add_button = Button(text='Add', font=FONT, command=save_password, bg='PaleGreen', activebackground='limegreen')
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")

# Reset Button
reset_button = Button(text='Reset', font=FONT, command=all_reset, bg='tomato', activebackground='firebrick1')
reset_button.grid(column=1, row=5, columnspan=2, sticky="EW")

# Search Button
search_button = Button(text='Search', font=FONT, command=find_password, bg='cornsilk2', activebackground='cornsilk3')
search_button.grid(column=2, row=1, sticky="EW")

window.mainloop()

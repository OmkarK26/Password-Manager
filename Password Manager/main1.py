import json
import re
from tkinter import *
from tkinter import messagebox, ttk
from random import choice, randint, shuffle

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(letters) for _ in range(randint(2, 4))]
    password_numbers = [choice(letters) for _ in range(randint(2, 4))]

    password_list = password_numbers + password_symbols + password_letters
    shuffle(password_list)
    password = "".join(password_list)
    password_input.delete(0, END)
    password_input.insert(0, password)

    check_password_strength()

def check_password_strength():
    password = password_input.get()

    length_regex = re.compile(r'^.{8,}$')
    uppercase_regex = re.compile(r'[A-Z]')
    lowercase_regex = re.compile(r'[a-z]')
    digit_regex = re.compile(r'\d')
    symbol_regex = re.compile(r'[!@#$%^&*()_+{}|:"<>?~`\-=[\];\',./]')

    length = bool(length_regex.search(password))
    uppercase = bool(uppercase_regex.search(password))
    lowercase = bool(lowercase_regex.search(password))
    digit = bool(digit_regex.search(password))
    symbol = bool(symbol_regex.search(password))

    strength = sum([length, uppercase, lowercase, digit, symbol])

    if strength == 5:
        update_progress_bar(100, 'green')
    elif strength >= 3:
        update_progress_bar(75, 'blue')
    elif strength >= 2:
        update_progress_bar(50, 'yellow')
    elif strength >= 1:
        update_progress_bar(25, 'orange')
    else:
        update_progress_bar(10, 'red')

def update_progress_bar(value, color):
    password_strength_bar['value'] = value
    style.configure('PasswordStrength.Horizontal.TProgressbar', background=color)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()

    entered_data = {
        website: {
            'email': email,
            'password': password
        }
    }

    if website == '' or email == '' or password == '':
        messagebox.showinfo(title="Error", message="Please do not leave the fields empty")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(entered_data, data_file, indent=4)
        else:
            data.update(entered_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)

# ---------------------------- SEARCH BUTTON ------------------------------- #
def search():
    website = website_input.get()
    try:
        with open("data.json", "r") as data_file:
            data_retrieved = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="Website not found in the database.")
    else:
        if website in data_retrieved:
            email_id = data_retrieved[website]["email"]
            password = data_retrieved[website]["password"]
            messagebox.showinfo(title="Website Email id and Password", message=f"Email id : {email_id} \n password : {password}")
        else:
            messagebox.showerror(title="Error", message="Website does not exist in the database.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="#ECECEC")

canvas = Canvas(window, height=200, width=200, bg="#ECECEC", highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(window, text="Website:", font=("Helvetica", 12), bg="#ECECEC", fg="black")
website_label.grid(column=0, row=1, sticky="E")
website_input = Entry(window, width=40)
website_input.grid(column=1, row=1, columnspan=2, sticky="W")

email_label = Label(window, text="Email/Username:", font=("Helvetica", 12), bg="#ECECEC", fg="black")
email_label.grid(column=0, row=2, sticky="E")
email_input = Entry(window, width=40)
email_input.grid(column=1, row=2, columnspan=2, sticky="W")

password_label = Label(window, text="Password:", font=("Helvetica", 12), bg="#ECECEC", fg="black")
password_label.grid(column=0, row=3, sticky="E")
password_input = Entry(window, width=32)
password_input.grid(column=1, row=3, sticky="W")

generate_button = Button(window, text="Generate Password", font=("Helvetica", 10), bg="#4CAF50", fg="white", command=generate_pass)
generate_button.grid(column=2, row=3, sticky="W")

password_strength_bar = ttk.Progressbar(window, orient='horizontal', mode='determinate', length=200, style='PasswordStrength.Horizontal.TProgressbar')
password_strength_bar.grid(column=1, row=4, columnspan=2, pady=(10, 0))

add_button = Button(window, text="Add", font=("Helvetica", 10), bg="#4CAF50", fg="white", width=36, command=save)
add_button.grid(column=1, row=5, columnspan=2, pady=(10, 0))

search_button = Button(window, text="Search", font=("Helvetica", 10), bg="#4CAF50", fg="white", command=search)
search_button.grid(column=2, row=1, sticky="W")

window.mainloop()

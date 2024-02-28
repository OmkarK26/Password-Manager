import json
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import re
from tkinter import ttk


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8,10))]
    password_symbols = [choice(letters) for _ in range(randint(2,4))]
    password_numbers = [choice(letters) for _ in range(randint(2,4))]

    password_list = password_numbers + password_symbols + password_letters
    shuffle(password_list)
    password = "".join(password_list)
    password_input.insert(0, password)

    password_strength = check_password_strength(password)
    # messagebox.showinfo(title="Password Strength", message=f"Password Strength: {password_strength}")

    if password_strength == "Very Strong":
        password_strength_bar['value'] = 100
        password_strength_bar['style'] = 'PasswordStrength.VeryStrong.Horizontal.TProgressbar'
    elif password_strength == "Strong":
        password_strength_bar['value'] = 75
        password_strength_bar['style'] = 'PasswordStrength.Strong.Horizontal.TProgressbar'
    elif password_strength == "Moderate":
        password_strength_bar['value'] = 50
        password_strength_bar['style'] = 'PasswordStrength.Moderate.Horizontal.TProgressbar'
    elif password_strength == "Weak":
        password_strength_bar['value'] = 25
        password_strength_bar['style'] = 'PasswordStrength.Weak.Horizontal.TProgressbar'
    else:
        password_strength_bar['value'] = 10
        password_strength_bar['style'] = 'PasswordStrength.VeryWeak.Horizontal.TProgressbar'

def check_password_strength(password):

    password = password_input.get()
    # Define criteria for a strong password
    length_regex = re.compile(r'^.{8,}$')  # At least 8 characters
    uppercase_regex = re.compile(r'[A-Z]')  # At least one uppercase letter
    lowercase_regex = re.compile(r'[a-z]')  # At least one lowercase letter
    digit_regex = re.compile(r'\d')         # At least one digit
    symbol_regex = re.compile(r'[!@#$%^&*()_+{}|:"<>?~`\-=[\];\',./]')  # At least one symbol

    # Check each criterion
    length = bool(length_regex.search(password))
    uppercase = bool(uppercase_regex.search(password))
    lowercase = bool(lowercase_regex.search(password))
    digit = bool(digit_regex.search(password))
    symbol = bool(symbol_regex.search(password))

    # Calculate the overall strength score
    strength = sum([length, uppercase, lowercase, digit, symbol])

    # Determine the strength level based on the score
    if strength == 5:
        return "Very Strong"
    elif strength >= 3:
        return "Strong"
    elif strength >= 2:
        return "Moderate"
    elif strength >= 1:
        return "Weak"
    else:
        return "Very Weak"

def check_password_strength_on_click():
    password = password_input.get()
    password_strength = check_password_strength(password)

    if password_strength == "Very Strong":
        password_strength_bar['value'] = 100
        password_strength_bar['style'] = 'PasswordStrength.VeryStrong.Horizontal.TProgressbar'
    elif password_strength == "Strong":
        password_strength_bar['value'] = 75
        password_strength_bar['style'] = 'PasswordStrength.Strong.Horizontal.TProgressbar'
    elif password_strength == "Moderate":
        password_strength_bar['value'] = 50
        password_strength_bar['style'] = 'PasswordStrength.Moderate.Horizontal.TProgressbar'
    elif password_strength == "Weak":
        password_strength_bar['value'] = 25
        password_strength_bar['style'] = 'PasswordStrength.Weak.Horizontal.TProgressbar'
    else:
        password_strength_bar['value'] = 10
        password_strength_bar['style'] = 'PasswordStrength.VeryWeak.Horizontal.TProgressbar'

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
        messagebox.showinfo(title="Error" , message="Please do not leave the fields empty")
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
        messagebox.showerror(title="Error", message="Database file not found.")
    else:
        if website in data_retrieved:
            email_id = data_retrieved[website]["email"]
            password = data_retrieved[website]["password"]
            email_input.delete(0, END)  # Clear previous content
            email_input.insert(0, email_id)  # Auto-fill email input
            password_input.delete(0, END)  # Clear previous content
            password_input.insert(0, password)  # Auto-fill password input
            messagebox.showinfo(title="Website Email id and Password", message=f"Email id : {email_id} \n password : {password}")
        else:
            messagebox.showerror(title="Error", message="Website not found in the database.")



# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Generator")
window.config(padx=50, pady=50, bg="#ECECEC")
canvas = Canvas(window, height=250, width=250)
canvas.grid(column=1, row=0)

logo_img = PhotoImage(file="logo.png")
canvas.create_image(155,100, image=logo_img)

website_label = Label(window, text="Website:", font=("Helvetica"), bg="#ECECEC")
website_label.grid(column=0, row=1)
website_input = Entry(window, width=40)
website_input.config(bg="white")
website_input.grid(column=1, row=1, columnspan=1)

email_label = Label(window, text="Email: ", font=("Helvetica"), bg="#ECECEC")
email_label.grid(column=0, row=2)
email_input = Entry(window, width=40)
email_input.config(bg="white")
email_input.insert(0, "omkar@gmail.com")
email_input.grid(column=1, row=2, columnspan=2)

password_label = Label(window, text="Password:", font=("Helvetica"), bg="#ECECEC")
password_label.grid(column=0, row=3)
password_input = Entry(window, width=32)
password_input.config(bg="white")
password_input.grid(column=0, row=3, columnspan=3)

password_button = Button(window, text="Generate", bg="white", font="Helvetica", command=generate_pass)
password_button.config()
password_button.grid(column=2, row=3, columnspan=3)

password_strength_bar = ttk.Progressbar(window, orient='horizontal', mode='determinate', length=365)
password_strength_bar.grid(column=1, row=4)
style = ttk.Style()
style.theme_use('default')  # Choose your desired theme

style.configure('PasswordStrength.VeryStrong.Horizontal.TProgressbar', background='green')
style.configure('PasswordStrength.Strong.Horizontal.TProgressbar', background='blue')
style.configure('PasswordStrength.Moderate.Horizontal.TProgressbar', background='yellow')
style.configure('PasswordStrength.Weak.Horizontal.TProgressbar', background='orange')
style.configure('PasswordStrength.VeryWeak.Horizontal.TProgressbar', background='red')

strength_check = Button(window, text="Check Strength", command=check_password_strength_on_click)
strength_check.grid(column=3, row=4, columnspan=2)



add_button = Button(window, text="ADD", bg="white", font="Helvetica", width=42, command=save)
add_button.grid(column=1, row=5)

search_button = Button(window, text="  Search ", bg="white", font="Helvetica", command=search)
search_button.grid(column=2, row=1, columnspan=3)


window.mainloop()


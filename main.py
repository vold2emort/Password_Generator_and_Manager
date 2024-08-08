from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
# Password Generator Project


def generate_password():
    password_input.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(6, 8))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_numbers + password_symbols + password_letters
    shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)


# Search
def find_password():
    search_label = website_input.get()
    with open("data.json", "r") as data_file:
        data = json.load(data_file)

    for key in data:
        if search_label == key:
            messagebox.showinfo(title="Information", message=f"Website: {key}\n"
                                                             f"Email: {data[key]['email']}\n"
                                                             f"Password: {data[key]['password']}")

# Password save


def save():
    website = website_input.get()
    email = email_input.get()
    password_box = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password_box,
        }
    }
    if len(website) == 0 or len(password_box) == 0:
        messagebox.showinfo(title="Error", message="Don't leave the fields empty")
    else:
        try:
            # reading old data can cause DcodeError if file empty
            # can cause fileNotFound error if there is no file
            with open("data.json", "r") as data_file:
                data = json.load(data_file)

        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        # In case an empty .json file is created the empty file can't be read on 46
        except json.JSONDecodeError as e:
            print(f"{e}\n Please delete the empty .json file")

        else:
            # updating the old data and adding to the .json file
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)

# ui part


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
wallpaper = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=wallpaper)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
website_input = Entry(width=21)
website_input.focus()
website_input.grid(column=1, row=1)
search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(row=1, column=2)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
email_input = Entry(width=40)
email_input.insert(0, "regular_every_day_normal_mf@gmail.com")
email_input.grid(column=1, row=2, columnspan=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)
password_input = Entry(width=21)
password_input.grid(column=1, row=3)

generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3)

add_button = Button(text="Add", width=34, command=save)
add_button.grid(column=1, row=5, columnspan=2)

window.mainloop()

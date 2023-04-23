from tkinter import *
from time import *
from tinydb import *
import awesometkinter as atk
import re
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from validate_email import validate_email
import random

usersdb = TinyDB("usersdb.json")
user = Query()
balance = Query()


def show_frame(frame):
    deposit_status["text"] = ""
    incorrect_label["text"] = ""
    registration_status_label["text"] = ""
    withdraw_status["text"] = ""
    change_password_status["text"] = ""
    exchange_status["text"] = ""
    frame.tkraise()


def tick_start():
    current_time = strftime("%I:%M %p")
    time_start_label.config(text=current_time)
    time_start_label.after(200, tick_start)


def tick_register():
    current_time = strftime("%I:%M %p")
    time_register_label.config(text=current_time)
    time_register_label.after(200, tick_register)


def tick_mainmenu():
    current_time = strftime("%I:%M %p")
    time_mainmenu_label.config(text=current_time)
    time_mainmenu_label.after(200, tick_mainmenu)


def tick_balance():
    current_time = strftime("%I:%M %p")
    time_balance_label.config(text=current_time)
    time_balance_label.after(200, tick_balance)


def tick_deposit():
    current_time = strftime("%I:%M %p")
    time_deposit_label.config(text=current_time)
    time_deposit_label.after(200, tick_deposit)


def tick_withdraw():
    current_time = strftime("%I:%M %p")
    time_withdraw_label.config(text=current_time)
    time_withdraw_label.after(200, tick_withdraw)


def tick_changepassword():
    current_time = strftime("%I:%M %p")
    time_change_password_label.config(text=current_time)
    time_change_password_label.after(200, tick_changepassword)


def tick_services():
    current_time = strftime("%I:%M %p")
    time_services_label.config(text=current_time)
    time_services_label.after(200, tick_services)


def tick_exchange():
    current_time = strftime("%I:%M %p")
    time_exchange_label.config(text=current_time)
    time_exchange_label.after(200, tick_exchange)


def tick_sendmoney():
    current_time = strftime("%I:%M %p")
    time_send_money_label.config(text=current_time)
    time_send_money_label.after(200, tick_sendmoney)


def tick_loanmoney():
    current_time = strftime("%I:%M %p")
    time_loan_money_label.config(text=current_time)
    time_loan_money_label.after(200, tick_loanmoney)


def login():
    username_get = username.get()
    password_get = password.get()
    user_check = usersdb.search(user.username == username_get)
    password_check = usersdb.search((user.username == username_get) & (user.password == password_get))
    if user_check:
        if password_check:
            password.set("")
            incorrect_label["text"] = ""
            show_frame(main_menu_frame)
        else:
            incorrect_label["text"] = "Uneseni podaci su neispravni"
    else:
        incorrect_label["text"] = "Uneseni podaci su neispravni"


def check_username(uss):
    if len(uss) < 4:
        registration_status_label["fg"] = "red"
        registration_status_label["text"] = "Korisnicko ime mora da sadrzi minimum 4 karaktera"
        return False
    else:
        return True


def check_password(pw):
    if len(pw) < 8:
        registration_status_label["fg"] = "red"
        registration_status_label["text"] = "Lozinka mora da sadrzi 8 ili vise karaktera"
        return False
    elif not re.search("[A-Z]", pw):
        registration_status_label["fg"] = "red"
        registration_status_label["text"] = "Lozinka mora da sadrzi bar jedno veliko slovo"
        return False
    elif not re.search("[a-z]", pw):
        registration_status_label["fg"] = "red"
        registration_status_label["text"] = "Lozinka mora da sadrzi bar jedno malo slovo"
        return False
    elif not re.search("[0-9]", pw):
        registration_status_label["fg"] = "red"
        registration_status_label["text"] = "Lozinka mora da sadrzi bar jedan broj"
        return False
    else:
        return True


def register_submit():
    registration_status_label["text"] = ""
    account_number_set = random.randint(1000000, 2000000)
    foreign_currency_account_number_set = random.randint(2000000, 3000000)
    new_user = {"username": registred_username.get(),
                "password": registred_password.get(),
                "email": registred_email.get(),
                "account_number": account_number_set,
                "foreign_currency_account_number": foreign_currency_account_number_set,
                "balance": 100000,
                "foreign_currency_balance": 0,
                }
    check_user = usersdb.search(user.username == registred_username.get())
    check_if_email_exists = usersdb.search(user.email == registred_email.get())
    email_is_valid = validate_email(registred_email.get())
    if check_username(registred_username.get()):
        if email_is_valid:
            if not check_if_email_exists:
                if registred_password.get() == repeated_password.get():
                    if check_password(registred_password.get()):
                        if check_user:
                            registration_status_label["fg"] = "red"
                            registration_status_label["text"] = "Korisnik vec postoji"
                            registred_password.set("")
                            registred_username.set("")
                            repeated_password.set("")
                        else:
                            registration_status_label["fg"] = "#66ff33"
                            registration_status_label["text"] = "Uspesno ste se registrovali"
                            usersdb.insert(new_user)
                            registred_password.set("")
                            registred_username.set("")
                            repeated_password.set("")
                            registred_email.set("")
                else:
                    registration_status_label["fg"] = "red"
                    registration_status_label["text"] = "Lozinke se ne podudaraju"
                    registred_password.set("")
                    repeated_password.set("")
            else:
                registration_status_label["fg"] = "red"
                registration_status_label["text"] = "Ova E-mail adresa je vec registrovana"
        else:
            registration_status_label["fg"] = "red"
            registration_status_label["text"] = "Neispravan E-mail"


def balance_check():
    show_frame(balance_frame)
    account_number = usersdb.get(Query()["username"] == username.get()).get("account_number")
    foreign_account_number = usersdb.get(Query()["username"] == username.get()).get("foreign_currency_account_number")
    balance_amount = usersdb.get(Query()["username"] == username.get()).get("balance")
    foreign_balance_amount = usersdb.get(Query()["username"] == username.get()).get("foreign_currency_balance")
    account_label["text"] = "Dinarski racun: " + str(account_number)
    account_balance_label["text"] = "Raspoloziva sredstva: " + str(balance_amount) + " RSD"
    foreign_account_label["text"] = "Devizni racun: " + str(foreign_account_number)
    foreign_account_balance_label["text"] = "Raspoloziva sredstva: " + str(foreign_balance_amount) + " EUR"


def withdraw(amount):
    flag = 0
    username_get = username.get()
    old_amount_get = usersdb.get(Query()["username"] == username_get)
    old_amount = old_amount_get.get("balance")
    if amount > 0:
        if amount % 500 == 0 and amount <= 50000:
            if old_amount >= amount:
                new_amount = old_amount - amount
                usersdb.update({"balance": new_amount}, user.username == username_get)
                withdraw_status["fg"] = "#90ff1a"
                withdraw_status["text"] = "Uspesno ste podigli: " + str(amount) + " RSD"
                send_mail(amount, new_amount, flag)
                another_amount.set(0)
            else:
                withdraw_status["fg"] = "red"
                withdraw_status["text"] = "Nemate dovoljno novca na racunu!"
        elif amount > 50000:
            withdraw_status["fg"] = "red"
            withdraw_status["text"] = "Limit po transakciji je 50000"
        else:
            withdraw_status["fg"] = "red"
            withdraw_status["text"] = "Iznos mora biti deljiv sa 500"
    else:
        withdraw_status["fg"] = "red"
        withdraw_status["text"] = "Iznos mora biti veci od 0"


def send_mail(amount, new_amount, flag):
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "dejan@gmail.com"
    receiver_email_get = usersdb.get(Query()["username"] == username.get())
    receiver_email = receiver_email_get.get("email")
    email_password = ""
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = receiver_email
    if flag == 0:
        message["Subject"] = "Izvestaj o podizanju novca"
        text = "Sa Vaseg racuna je uspesno podignuto " + str(amount) + " RSD" + ".\nVase novo stanje iznosi: " + str(
            new_amount) + " RSD"
        part1 = MIMEText(text, "plain")
        message.attach(part1)
    elif flag == 1:
        message["Subject"] = "Izvestaj o uplati na racun"
        text = "Na Vas racun je uspesno uplaceno " + str(amount) + " RSD" + ".\nVase novo stanje iznosi: " + str(
            new_amount) + " RSD"
        part1 = MIMEText(text, "plain")
        message.attach(part1)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, message.as_string())


def deposit(amount):
    flag = 1
    username_get = username.get()
    old_amount_get = usersdb.get(Query()["username"] == username_get)
    old_amount = old_amount_get.get("balance")
    if int(amount) < 500:
        deposit_status.pack()
        deposit_status["fg"] = "red"
        deposit_status["text"] = "Minimalni iznos za uplatu je 500 RSD"
    elif not int(amount) % 500 == 0:
        deposit_status.pack()
        deposit_status["fg"] = "red"
        deposit_status["text"] = "Iznos mora biti deljiv sa 500"
    elif int(amount) > 50000:
        deposit_status.pack()
        deposit_status["fg"] = "red"
        deposit_status["text"] = "Maksimalni iznos po transakciji je 50000 RSD"
    else:
        deposit_status.pack()
        deposit_status["fg"] = "#66ff33"
        deposit_status["text"] = "Uspesno ste uplatili " + str(amount) + " RSD"
        new_amount = old_amount + int(amount)
        usersdb.update({"balance": new_amount}, user.username == username_get)
        send_mail(amount, new_amount, flag)


def change_password():
    username_get = username.get()
    new_password_get = new_password.get()
    repeated_new_password_get = repeated_new_password.get()
    old_password_get = usersdb.get(Query()["username"] == username.get())
    old_password = old_password_get.get("password")
    if entered_old_password.get() == old_password:
        if new_password_get == repeated_new_password_get:
            if check_password(new_password.get()):
                change_password_status["fg"] = "#66ff33"
                change_password_status["text"] = "Uspesno ste promenili lozinku"
                usersdb.update({"password": new_password.get()}, user.username == username_get)
                entered_old_password.set("")
                new_password.set("")
                repeated_new_password.set("")
            else:
                change_password_status["fg"] = "red"
                change_password_status["text"] = "Nova lozinka neispunjava kriterijume"
        else:
            change_password_status["fg"] = "red"
            change_password_status["text"] = "Lozinke se ne podudaraju"
    else:
        change_password_status["fg"] = "red"
        change_password_status["text"] = "Stara sifra je neispravna"


def exchange_show():
    show_frame(exchange_frame)


def exchange(amount):
    dinarski = ("Dinarski racun: " + str(account_number))
    devizni = ("Devizni racun: " + str(foreign_currency_account_number))
    current_balance = usersdb.get(Query()["username"] == username.get()).get("balance")
    current_foreign_balance = usersdb.get(Query()["username"] == username.get()).get("foreign_currency_balance")
    dinar_amount = amount * 118
    if exchange_amount.get() >= 10:
        if exchange_amount.get() <= 500:
            if option1.get() != option2.get():
                if option1.get() == dinarski and option2.get() == devizni:
                    if current_balance >= dinar_amount:
                        usersdb.update({"balance": current_balance - dinar_amount}, user.username == username.get())
                        usersdb.update({"foreign_currency_balance": current_foreign_balance + amount},
                                       user.username == username.get())
                        exchange_status["fg"] = "#66ff33"
                        exchange_status["text"] = "Uspesno ste kupili " + str(amount) + " EUR"
                        exchange_amount.set(0)
                    else:
                        exchange_status["fg"] = "red"
                        exchange_status["text"] = "Nemate dovoljno sredstava na dinarskom racunu"
                elif option1.get() == devizni and option2.get() == dinarski:
                    if current_foreign_balance >= amount:
                        usersdb.update({"balance": current_balance + dinar_amount}, user.username == username.get())
                        usersdb.update({"foreign_currency_balance": current_foreign_balance - amount},
                                       user.username == username.get())
                        exchange_status["fg"] = "#66ff33"
                        exchange_status["text"] = "Uspesno ste prodali " + str(amount) + " EUR"
                        exchange_amount.set(0)
                    else:
                        print(option1.get())
                        print(devizni)
                        print(option2.get())
                        print(dinarski)
                        exchange_status["fg"] = "red"
                        exchange_status["text"] = "Nemate dovoljno sredstava na deviznom racunu"
                else:
                    print(option1.get())
                    print("Dinarski racun: " + str(account_number) + " Stanje: " +
                          str(usersdb.get(Query()["username"] == username.get()).get("balance")))
                    print(option2.get())
                    print("Devizni racun: " + str(foreign_currency_account_number) + " Stanje: " +
                          str(usersdb.get(Query()["username"] == username.get()).get("foreign_currency_balance")))
                    exchange_status["fg"] = "red"
                    exchange_status["text"] = "Greska"
            else:
                exchange_status["fg"] = "red"
                exchange_status["text"] = "Ne mozete razmeniti novac na isti racun"
        else:
            exchange_status["fg"] = "red"
            exchange_status["text"] = "Maksimalni iznos za razmenu je 500 EUR"
    else:
        exchange_status["fg"] = "red"
        exchange_status["text"] = "Minimalni iznos za razmenu je 10 EUR"


def cash_loan_check():
    if cash_loan_amount.get() < 100000:
        cash_loan_status["text"] = "Minimalni iznos za uzimanje kredita je 100.000 RSD"
        cash_loan_status["fg"] = "red"
    elif cash_loan_amount.get() > 500000:
        cash_loan_status["text"] = "Maksimalni iznos za uzimanje kredita je 500.000 RSD"
        cash_loan_status["fg"] = "red"
    else:
        monthly_rate = cash_loan_amount.get() / 12
        cash_loan_status["text"] = "Uspesno"
        cash_loan_status["fg"] = "green"


def send_money(amount):
    current_balance = usersdb.get(Query()["username"] == username.get()).get("balance")
    check_if_account_to_send_exists = usersdb.search(user.account_number == send_to_account.get())
    if send_money_from_account.get() == "Dinarski racun: " + str(account_number):
        if check_if_account_to_send_exists:
            receiver_current_balance = usersdb.get(Query()["account_number"] == send_to_account.get()).get("balance")
            if amount > 0:
                usersdb.update({"balance": current_balance - amount}, user.username == username.get())
                usersdb.update({"balance": receiver_current_balance + amount},
                               user.account_number == send_to_account.get())
                send_money_status_label["fg"] = "green"
                send_money_status_label["text"] = "Uspesno ste poslali novac na racun: " + str(send_to_account.get())
            else:
                send_money_status_label["fg"] = "red"
                send_money_status_label["text"] = "Iznos mora biti veci od 0 RSD"
        else:
            send_money_status_label["fg"] = "red"
            send_money_status_label["text"] = "Racun na koji zelite da posaljete novac ne postoji!"
    else:
        send_money_status_label["fg"] = "red"
        send_money_status_label["text"] = "Izaberite Vas racun!"


def hide_password(_):
    password_entrybox.configure(fg="black", show="*")
    register_password_entrybox.configure(fg="black", show="*")
    repeat_password_entrybox.configure(fg="black", show="*")
    new_password_entrybox.configure(fg="black", show="*")
    repeated_new_password_entrybox.configure(fg="black", show="*")


window = Tk()
window.title("Bankomat v1.0")
window.state("zoomed")
window.iconphoto(False, PhotoImage(file="bank.png"))
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# PRAVLJENJE FREJMOVA #
start_frame = Frame(window, bg="#660066")
register_frame = Frame(window, bg="#333333")
main_menu_frame = Frame(window, bg="#0a0a29")
balance_frame = Frame(window, bg="#0a0a29")
withdraw_frame = Frame(window, bg="#0a0a29")
deposit_frame = Frame(window, bg="#0a0a29")
change_password_frame = Frame(window, bg="#404040")
services_frame = Frame(window, bg="#330033")
exchange_frame = Frame(window, bg="#330000")
loan_money_frame = Frame(window, bg="#0a0a29")
cash_loan_frame = Frame(window, bg="#0a0a29")
house_loan_frame = Frame(window, bg="#0a0a29")
send_money_frame = Frame(window, bg="#0a0a29")
for frame in (start_frame, register_frame, main_menu_frame, balance_frame, withdraw_frame, deposit_frame,
              change_password_frame, services_frame, exchange_frame, loan_money_frame, cash_loan_frame,
              house_loan_frame, send_money_frame):
    frame.grid(row=0, column=0, sticky="nsew")

# START MENI #
start_frame_title = Label(start_frame, text="E-banking", font="orbitron 100 bold", fg="#ff99ff", bg="#660066")
start_frame_title.pack(pady="30", fill="x")
username_label = Label(start_frame, text="Unesite vase korisnicko ime:", font="orbitron 13", bg="#660066", fg="#ff99ff")
username_label.pack()

username = StringVar()
username_entrybox = Entry(start_frame, textvariable=username, font="orbitron 12", width=22, bg="#660066")
username_entrybox.focus_set()
username_entrybox.pack(ipady=4)

password_label = Label(start_frame, text="Unesite vasu lozinku: ", font="orbitron 13", bg="#660066", fg="#ff99ff")
password_label.pack()

password = StringVar()
password_entrybox = Entry(start_frame, textvariable=password, font="orbitron 12", width=22, bg="#660066")
password_entrybox.pack(ipady=4)
password_entrybox.bind("<FocusIn>", hide_password)

login_button = Button(start_frame, text="Login", command=login, font="orbitron", relief="raised", borderwidth=3,
                      width=24, height=2, bg="#ff99ff")
login_button.pack(pady=10)

register_button = Button(start_frame, text="Registracija", command=lambda: show_frame(register_frame), font="orbitron",
                         relief="raised", borderwidth=3, width=24, height=2)
register_button.pack()

incorrect_label = Label(start_frame, text="", font="orbitron 12", bg="#4d004d", fg="red", anchor="n")
incorrect_label.pack(fill="both", expand=True)

# STRANICA ZA REGISTRACIJA #
# NASLOV #
register_frame_title = Label(register_frame, text="Registracija", font="orbitron 70 bold", bg="#333333", fg="#808080")
register_frame_title.pack(side=TOP)
Label(register_frame, text="___________________________________________", font="orbitron 40", bg="#333333",
      fg="#808080").pack()
Label(register_frame, text="", bg="#333333", fg="#808080").pack(pady=40)
# UNOS KORISNICKOG IMENA #
register_username_label = Label(register_frame, text="Korisnicko ime:", font="orbitron 13", bg="#333333",
                                fg="#808080").pack()
registred_username = StringVar()
register_username_entrybox = Entry(register_frame, textvariable=registred_username, font="orbitron 13", width=22,
                                   bg="#333333")
register_username_entrybox.pack()

# UNOS EMAIL ADRESE #
register_email_label = Label(register_frame, text="E-mail:", font="orbitron 13", bg="#333333",
                             fg="#808080").pack()
registred_email = StringVar()
register_email_entrybox = Entry(register_frame, textvariable=registred_email, font="orbitron 13", width=22,
                                bg="#333333")
register_email_entrybox.pack()
# UNOS ZELJENE LOZINKE #
register_password_label = Label(register_frame, text="Unesite zeljenu lozinku:", font="orbitron 13", bg="#333333",
                                fg="#808080")
register_password_label.pack()
registred_password = StringVar()
register_password_entrybox = Entry(register_frame, textvariable=registred_password, font="orbitron 13", width=22,
                                   bg="#333333")
register_password_entrybox.pack()
register_password_entrybox.bind("<FocusIn>", hide_password)

# PONAVLJANJE LOZINKE #
repeat_password_label = Label(register_frame, text="Ponovite Vasu lozinku:", font="orbitron 13", bg="#333333",
                              fg="#808080")
repeat_password_label.pack()
repeated_password = StringVar()
repeat_password_entrybox = Entry(register_frame, textvariable=repeated_password, font="orbitron 13", width=22,
                                 bg="#333333")
repeat_password_entrybox.pack()
repeat_password_entrybox.bind("<FocusIn>", hide_password)

# POTVRDI DUGME #
submit_button = Button(register_frame, text="Registruj se", font="orbitron", command=register_submit, relief="raised",
                       borderwidth=3, bg="#00ff00", fg="#4d4d4d", width=25, height=2)
submit_button.pack(pady=10)

# STATUS REGISTRACIJE #
registration_status_label = Label(register_frame, text="", font="orbitron 13", bg="#333333", fg="#66ff33", anchor="n")
registration_status_label.pack()

# POVRATAK U POCETNI MENI #
Button(register_frame, text="Nazad", font="orbitron", command=lambda: show_frame(start_frame), relief="raised",
       borderwidth=4, width=25, height=2).pack()

# GLAVNI MENI #
main_menu_title = Label(main_menu_frame, text="IZABERITE OPCIJU", font="orbitron 50 bold", bg="#0a0a29",
                        fg="#7070db").pack(pady=10)
Label(main_menu_frame, text="___________________________________________", font="orbitron 40", bg="#0a0a29",
      fg="#1f1f7a").pack()
balance_check_button = Button(main_menu_frame, text="Provera Stanja", font="orbitron", bg="#1f1f7a", fg="white",
                              command=balance_check,
                              relief="raised", borderwidth=4, width=29, height=3).pack(pady=3)
withdraw_button = Button(main_menu_frame, text="Podizanje Novca", font="orbitron", bg="#1f1f7a", fg="white",
                         command=lambda: show_frame(withdraw_frame),
                         relief="raised", borderwidth=4, width=29, height=3).pack(pady=3)
deposit_button = Button(main_menu_frame, text="Uplata Novca", font="orbitron", bg="#1f1f7a", fg="white",
                        command=lambda: show_frame(deposit_frame),
                        relief="raised", borderwidth=4, width=29, height=3).pack(pady=3)
change_password_button = Button(main_menu_frame, text="Promena lozinke", font="orbitron", bg="#1f1f7a", fg="white",
                                command=lambda: show_frame(change_password_frame), relief="raised", borderwidth=4,
                                width=29, height=3).pack(pady=3)
services_button = Button(main_menu_frame, text="Usluge", font="orbitron", bg="#1f1f7a", fg="white",
                         command=lambda: show_frame(services_frame),
                         relief="raised", borderwidth=4, width=29, height=3).pack(pady=3)
back_button = Button(main_menu_frame, text="Izlaz", font="orbitron", bg="#1f1f7a", fg="white",
                     command=lambda: show_frame(start_frame),
                     relief="raised", borderwidth=4, width=29, height=3).pack(pady=3)

# PROVERA STANJA FRAME #
Label(balance_frame, text="BALANS PO RACUNIMA", font="orbitron 50 bold", bg="#0a0a29", fg="#6f6fdc").pack()
Label(balance_frame, text="___________________________________________", font="orbitron 40", bg="#0a0a29",
      fg="#6f6fdc").pack()
Label(balance_frame, text="", font="orbitron", bg="#0a0a29", fg="black").pack(pady=15)
account_label = Label(balance_frame, text="", font="orbitron 15", bg="#0a0a29", fg="#6f6fdc")
account_label.pack()
account_balance_label = Label(balance_frame, text="", font="orbitron", bg="#0a0a29", fg="#6f6fdc")
account_balance_label.pack(pady=5)
Label(balance_frame, text="", font="orbitron", bg="#0a0a29", fg="black").pack(pady=40)
foreign_account_label = Label(balance_frame, text="", font="orbitron 15", bg="#0a0a29", fg="#6f6fdc")
foreign_account_label.pack(pady=5)
foreign_account_balance_label = Label(balance_frame, text="", font="orbitron", bg="#0a0a29", fg="#6f6fdc")
foreign_account_balance_label.pack()
Button(balance_frame, command=lambda: show_frame(main_menu_frame), text="Nazad", font="orbitron 13", borderwidth=3,
       bg="#1f1f7a", fg="white", width=20, height=2).pack(pady=80)

# WITHDRAW FRAME #
Label(withdraw_frame, text="IZABERITE IZNOS:", font="Orbitron 50 bold", bg="#0a0a29", fg="#7070db").pack()
Label(withdraw_frame, text="___________________________________________", font="orbitron 40", bg="#0a0a29",
      fg="#7070db").pack()
Button(withdraw_frame, text="1000", font="orbitron", bg="#1f1f7a", fg="white", command=lambda: withdraw(1000),
       relief="raised", borderwidth=3, width=25, height=3).pack(pady=3)
Button(withdraw_frame, text="2000", font="orbitron", bg="#1f1f7a", fg="white", command=lambda: withdraw(2000),
       relief="raised", borderwidth=3, width=25, height=3).pack(pady=3)
Button(withdraw_frame, text="3000", font="orbitron", bg="#1f1f7a", fg="white", command=lambda: withdraw(3000),
       relief="raised", borderwidth=3, width=25, height=3).pack(pady=3)
Button(withdraw_frame, text="5000", font="orbitron", bg="#1f1f7a", fg="white", command=lambda: withdraw(5000),
       relief="raised", borderwidth=3, width=25, height=3).pack(pady=3)
another_amount = IntVar()
Label(withdraw_frame, text="Drugi iznos:", font="orbitron", bg="#0a0a29", fg="#7070db").pack(pady=4)
Entry(withdraw_frame, textvariable=another_amount, font="orbitron", width=6).pack(pady=4)
atk.Button3d(withdraw_frame, text="Potvrdi", command=lambda: withdraw(another_amount.get())).pack()
withdraw_status = Label(withdraw_frame, text="", font="orbitron 22 bold", bg="#0a0a29", fg="#90ff1a", anchor="n")
withdraw_status.pack()
Button(withdraw_frame, text="Izlaz", command=lambda: show_frame(main_menu_frame), relief="raised", font="orbitron 13",
       borderwidth=4, width=20, height=3, bg="#1f1f7a", fg="white").pack()

# DEPOSIT FRAME #
deposit_frame_title = Label(deposit_frame, text="IZABERITE IZNOS", font="orbitron 50 bold", bg="#0a0a29", fg="#7070db")
deposit_frame_title.pack()
Label(deposit_frame, text="___________________________________________", font="orbitron 40", bg="#0a0a29",
      fg="#7070db").pack()
Button(deposit_frame, text="1000", command=lambda: deposit(1000), relief="raised", font="orbitron", borderwidth=4,
       width=25, height=3, bg="#1f1f7a", fg="white").pack(pady=3)
Button(deposit_frame, text="2000", command=lambda: deposit(2000), relief="raised", font="orbitron", borderwidth=4,
       width=25, height=3, bg="#1f1f7a", fg="white").pack(pady=3)
Button(deposit_frame, text="3000", command=lambda: deposit(3000), relief="raised", font="orbitron", borderwidth=4,
       width=25, height=3, bg="#1f1f7a", fg="white").pack(pady=3)
Button(deposit_frame, text="5000", command=lambda: deposit(5000), relief="raised", font="orbitron", borderwidth=4,
       width=25, height=3, bg="#1f1f7a", fg="white").pack(pady=3)
Label(deposit_frame, text="Drugi iznos:", font="orbitron 20", bg="#0a0a29", fg="white").pack(pady=3)
another_deposit_amount = IntVar()
another_deposit_amount_entrybox = Entry(deposit_frame, textvariable=another_deposit_amount, width=6)
another_deposit_amount_entrybox.pack(pady=3)
atk.Button3d(deposit_frame, text="Potvrdi", command=lambda: deposit(another_deposit_amount_entrybox.get())).pack()
deposit_status = Label(deposit_frame, text="", font="orbitron 22 bold", bg="#0a0a29", fg="green")
deposit_status.pack()
Button(deposit_frame, text="Izlaz", command=lambda: show_frame(main_menu_frame), relief="raised", font="orbitron 13",
       borderwidth=4, width=20, height=3, bg="#1f1f7a", fg="white").pack()

# PROMENA LOZINKE FRAME #
Label(change_password_frame, text="PROMENA LOZINKE", font="orbitron 50 bold", bg="#404040", fg="white").pack()
Label(change_password_frame, text="___________________________________________", font="orbitron 40", bg="#404040",
      fg="green").pack()
Label(change_password_frame, text="", bg="#404040").pack(pady=40)
Label(change_password_frame, text="Stara lozinka:", font="orbitron", bg="#404040", fg="#bfbfbf").pack()
entered_old_password = StringVar()
entered_old_password_entrybox = Entry(change_password_frame, font="orbitron", bg="#404040",
                                      textvariable=entered_old_password, width=20)
entered_old_password_entrybox.pack()
Label(change_password_frame, text="Nova lozinka:", font="orbitron", bg="#404040", fg="#bfbfbf").pack()
new_password = StringVar()
new_password_entrybox = Entry(change_password_frame, font="orbitron", bg="#404040", textvariable=new_password, width=20)
new_password_entrybox.pack()
new_password_entrybox.bind("<FocusIn>", hide_password)
Label(change_password_frame, text="Ponovite lozinku:", font="orbitron", bg="#404040", fg="#bfbfbf").pack()
repeated_new_password = StringVar()
repeated_new_password_entrybox = Entry(change_password_frame, font="orbitron", bg="#404040",
                                       textvariable=repeated_new_password, width=20)
repeated_new_password_entrybox.pack()
repeated_new_password_entrybox.bind("<FocusIn>", hide_password)
atk.Button3d(change_password_frame, text="POTVRDI", command=change_password).pack(pady=15)
change_password_status = Label(change_password_frame, text="", font="orbitron", bg="#404040", fg="#66ff33", anchor="n")
change_password_status.pack()
Button(change_password_frame, text="NAZAD", font="orbitron 12", command=lambda: show_frame(main_menu_frame),
       borderwidth=4, width=20, height=3, relief="raised").pack(pady=40)

# USLUGE FRAME #
Label(services_frame, text="IZABERITE USLUGU", font="orbitron 50 bold", bg="#330033", fg="white").pack()
Label(services_frame, text="___________________________________________", font="orbitron 40", bg="#330033",
      fg="green").pack()
Label(services_frame, text="", font="orbitron", bg="#330033", fg="black").pack(pady=40)
Button(services_frame, text="MENJACNICA", font="orbitron", relief="raised", bg="#990099", fg="white",
       command=exchange_show,
       borderwidth=4, width=25, height=3).pack(pady=3)
Button(services_frame, text="UZIMITE KREDIT", font="orbitron", relief="raised", bg="#990099", fg="white",
       command=lambda: show_frame(loan_money_frame),
       borderwidth=4, width=25, height=3).pack(pady=3)
Button(services_frame, text="SLANJE NOVCA", font="orbitron", relief="raised", bg="#990099", fg="white",
       command=lambda: show_frame(send_money_frame),
       borderwidth=4, width=25, height=3).pack(pady=3)
Button(services_frame, text="IZLAZ", font="orbitron", relief="raised", bg="#990099", fg="white",
       command=lambda: show_frame(main_menu_frame), borderwidth=4, width=25, height=3).pack(pady=3)

# EXCHANGE FRAME #
Label(exchange_frame, text="MENJACNICA", font="orbitron 50 bold", bg="#330000", fg="#cc0000").pack()
Label(exchange_frame, text="___________________________________________", font="orbitron 40", bg="#330000",
      fg="green").pack()
Label(exchange_frame, text="", font="orbitron", bg="#330000").pack(pady=20)
Label(exchange_frame, text="Sa racuna:", font="orbitron", bg="#330000", fg="white").pack()
account_number = usersdb.get(Query()["username"] == username.get()).get("account_number")
foreign_currency_account_number = usersdb.get(Query()["username"] == username.get()).get(
    "foreign_currency_account_number")
option1 = StringVar(exchange_frame)
option1.set("Dinarski racun: " + str(account_number))
option1_list = OptionMenu(exchange_frame,
                          option1,
                          "Dinarski racun: " + str(account_number),
                          "Devizni racun: " + str(foreign_currency_account_number))
option1_list.pack()
Label(exchange_frame, text="", font="orbitron", bg="#330000").pack(pady=10)
option1_list.config(bg="#330000", fg="white", width=32)
Label(exchange_frame, text="Na racun:", font="orbitron", bg="#330000", fg="white").pack()
option2 = StringVar(exchange_frame)
option2.set("Devizni racun: " + str(foreign_currency_account_number))
option2_list = OptionMenu(exchange_frame,
                          option2,
                          "Dinarski racun: " + str(account_number),
                          "Devizni racun: " + str(foreign_currency_account_number))
option2_list.pack()
option2_list.config(bg="#330000", fg="white", width=32)
Label(exchange_frame, text="Iznos:", font="orbitron", bg="#330000", fg="white").pack()
exchange_amount = IntVar()
exchange_amount_entrybox = Entry(exchange_frame, font="orbitron", bg="#330000", fg="white", width=4,
                                 textvariable=exchange_amount)
exchange_amount_entrybox.pack()
Label(exchange_frame, text="EUR", font="orbitron", bg="#330000", fg="white").pack()
atk.Button3d(exchange_frame, text="Potvrdi", command=lambda: exchange(exchange_amount.get())).pack()
exchange_status = Label(exchange_frame, text="", font="orbitron", bg="#330000", fg="white")
exchange_status.pack()
Button(exchange_frame, text="IZLAZ", font="orbitron", relief="raised", bg="#cc0000", fg="white",
       command=lambda: show_frame(services_frame), borderwidth=4, width=25, height=3).pack(pady=50)

# UZIMANJE KREDITA #
Label(loan_money_frame, text="UZIMANJE KREDITA", font="orbitron 50 bold", bg="#0a0a29", fg="#7070db").pack()
Label(loan_money_frame, text="___________________________________________", font="orbitron 40", bg="#0a0a29",
      fg="green").pack()
Label(loan_money_frame, text="", font="orbitron", bg="#0a0a29").pack(pady=20)
Label(loan_money_frame, text="Izaberite kredit:", font="orbitron 15", bg="#0a0a29", fg="white").pack()
Button(loan_money_frame, command=lambda: show_frame(cash_loan_frame), text="Kes kredit", font="orbitron", bg="#7070db",
       fg="white", relief="raised", height=3, width=20).pack(
    pady=5)
Button(loan_money_frame, command=lambda: show_frame(house_loan_frame), text="Stambeni kredit", font="orbitron",
       bg="#7070db", fg="white", relief="raised", height=3,
       width=20).pack(pady=5)
Button(loan_money_frame, command=lambda: show_frame(services_frame), text="Izlaz", font="orbitron",
       bg="#7070db", fg="white", relief="raised", height=3,
       width=20).pack(pady=5)

# KES KREDIT FRAME #
Label(cash_loan_frame, text="KES KREDIT", font="orbitron 50 bold", bg="#0a0a29", fg="#7070db").pack()
Label(cash_loan_frame, text="___________________________________________", font="orbitron 40", bg="#0a0a29",
      fg="green").pack()
Label(cash_loan_frame, text="", font="orbitron", bg="#0a0a29").pack(pady=20)
Label(cash_loan_frame, text="Valuta kredita:    RSD", font="orbitron 14", bg="#0a0a29", fg="white").pack()
Label(cash_loan_frame, text="Tip kamatne stope: FIKSNA", font="orbitron 14", bg="#0a0a29", fg="white").pack()
Label(cash_loan_frame, text="Rok otplate(meseci): 12", font="orbitron 14", bg="#0a0a29", fg="white").pack()
Label(cash_loan_frame, text="Fiksna kamatna stopa: 10%", font="orbitron 14", bg="#0a0a29", fg="white").pack()
Label(cash_loan_frame, text="", font="orbitron", bg="#0a0a29").pack(pady=25)
Label(cash_loan_frame, text="Iznos kredita:", font="orbitron 14", bg="#0a0a29", fg="white").pack()
cash_loan_amount = IntVar()
cash_loan_amount_entry = Entry(cash_loan_frame, font="orbitron 14", bg="#0a0a29", fg="white", width=7,
                               textvariable=cash_loan_amount)
cash_loan_amount_entry.pack()
Button(cash_loan_frame, command=cash_loan_check, text="Izracunaj", font="orbitron", bg="#7070db", fg="white",
       relief="raised",
       height=1, width=9).pack(pady=5)
cash_loan_status = Label(cash_loan_frame, text="", font="orbitron 14", bg="#0a0a29", fg="red")
cash_loan_status.pack(pady=5)
Button(cash_loan_frame, command=lambda: show_frame(loan_money_frame), text="Izlaz", font="orbitron",
       bg="#7070db", fg="white", relief="raised", height=3,
       width=20).pack(pady=5)

# STAMBENI KREDIT FRAME #

# SLANJE NOVCA #
Label(send_money_frame, text="SLANJE NOVCA", font="orbitron 50 bold", bg="#0a0a29", fg="#7070db").pack()
Label(send_money_frame, text="___________________________________________", font="orbitron 40", bg="#0a0a29",
      fg="green").pack()
Label(send_money_frame, text="", font="orbitron", bg="#0a0a29").pack(pady=20)
Label(send_money_frame, text="Sa racuna:", font="orbitron", bg="#0a0a29", fg="white").pack()
send_money_from_account = StringVar()
from_account_optionlist = OptionMenu(send_money_frame, send_money_from_account,
                                     "Dinarski racun: " + str(account_number))
from_account_optionlist.pack()
from_account_optionlist.config(bg="#0a0a29", fg="white", width="22")
Label(send_money_frame, text="", font="orbitron", bg="#0a0a29").pack(pady=3)
Label(send_money_frame, text="Unesite racun primaoca:", font="orbitron", bg="#0a0a29", fg="white").pack()
send_to_account = IntVar()
Entry(send_money_frame, textvariable=send_to_account, bg="#0a0a29", fg="white", width=22).pack()
Label(send_money_frame, text="", font="orbitron", bg="#0a0a29").pack(pady=3)
Label(send_money_frame, text="Iznos za slanje:", font="orbitron", bg="#0a0a29", fg="white").pack()
send_amount = IntVar()
Entry(send_money_frame, textvariable=send_amount, font="orbitron", bg="#0a0a29", fg="white", width=8).pack()
atk.Button3d(send_money_frame, text="Potvrdi", command=lambda: send_money(send_amount.get())).pack()
send_money_status_label = Label(send_money_frame, text="", bg="#0a0a29", fg="white")
send_money_status_label.pack()
Button(send_money_frame, text="IZLAZ", font="orbitron", bg="#7070db", command=lambda: show_frame(services_frame),
       relief="raised", borderwidth=3, width=10, height=2).pack(pady=20)

# VREME #
footer_start_frame = Frame(start_frame, relief="raised", borderwidth=3, height=35)
footer_start_frame.pack(fill="x", side="bottom")
time_start_label = Label(footer_start_frame, font="orbitron 12")
time_start_label.pack(side="right")

footer_register_frame = Frame(register_frame, relief="raised", borderwidth=3, height=35)
footer_register_frame.pack(fill="x", side="bottom")
time_register_label = Label(footer_register_frame, font="orbitron 12")
time_register_label.pack(side="right")

footer_mainmenu_frame = Frame(main_menu_frame, relief="raised", borderwidth=3, height=35)
footer_mainmenu_frame.pack(fill="x", side="bottom")
time_mainmenu_label = Label(footer_mainmenu_frame, font="orbitron 12")
time_mainmenu_label.pack(side="right")

footer_balance_frame = Frame(balance_frame, relief="raised", borderwidth=3, height=35)
footer_balance_frame.pack(fill="x", side="bottom")
time_balance_label = Label(footer_balance_frame, font="orbitron 12")
time_balance_label.pack(side="right")

footer_withdraw_frame = Frame(withdraw_frame, relief="raised", borderwidth=3, height=35)
footer_withdraw_frame.pack(fill="x", side="bottom")
time_withdraw_label = Label(footer_withdraw_frame, font="orbitron 12")
time_withdraw_label.pack(side="right")

footer_deposit_frame = Frame(deposit_frame, relief="raised", borderwidth=3, height=35)
footer_deposit_frame.pack(fill="x", side="bottom")
time_deposit_label = Label(footer_deposit_frame, font="orbitron 12")
time_deposit_label.pack(side="right")

footer_change_password_frame = Frame(change_password_frame, relief="raised", borderwidth=3, height=35)
footer_change_password_frame.pack(fill="x", side="bottom")
time_change_password_label = Label(footer_change_password_frame, font="orbitron 12")
time_change_password_label.pack(side="right")

footer_services_frame = Frame(services_frame, relief="raised", borderwidth=3, height=35)
footer_services_frame.pack(fill="x", side="bottom")
time_services_label = Label(footer_services_frame, font="orbitron 12")
time_services_label.pack(side="right")

footer_exchange_frame = Frame(exchange_frame, relief="raised", borderwidth=3, height=35)
footer_exchange_frame.pack(fill="x", side="bottom")
time_exchange_label = Label(footer_exchange_frame, font="orbitron 12")
time_exchange_label.pack(side="right")

footer_send_money_frame = Frame(send_money_frame, relief="raised", borderwidth=3, height=35)
footer_send_money_frame.pack(fill="x", side="bottom")
time_send_money_label = Label(footer_send_money_frame, font="orbitron 12")
time_send_money_label.pack(side="right")

footer_loan_money_frame = Frame(loan_money_frame, relief="raised", borderwidth=3, height=35)
footer_loan_money_frame.pack(fill="x", side="bottom")
time_loan_money_label = Label(footer_loan_money_frame, font="orbitron 12")
time_loan_money_label.pack(side="right")

tick_start()
tick_register()
tick_mainmenu()
tick_balance()
tick_withdraw()
tick_deposit()
tick_changepassword()
tick_services()
tick_exchange()
tick_sendmoney()
tick_loanmoney()

show_frame(start_frame)
window.mainloop()

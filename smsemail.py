import tkinter
from tkinter import *
import datetime
import smtplib, ssl
import imaplib, email
import os
from email import policy
from threading import Thread

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("SMS MESSAGE VIA EMAIL")
        self.semail = "4163581222@txt.bell.ca"
        self.new_semail = self.semail.split("@")
        self.messages_frame = tkinter.Frame(master)
        self.my_msg = tkinter.StringVar()  # For the messages to be sent.
        self.my_msg.set("Type your messages here.")
        self.scrollbar = tkinter.Scrollbar(self.messages_frame)
        self.listbox = Listbox(self.messages_frame, height=30, width=95, borderwidth=2, relief="solid", yscrollcommand=self.scrollbar.set)
        self.listbox.pack()
        try:
            f = open(f'{self.new_semail[0]}.txt', "r")
            msgs = f.readlines()
            f.close
            for i in msgs:
                self.listbox.insert(tkinter.END, i)
        except:
            pass
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.listbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.listbox.pack()
        self.messages_frame.pack()
        self.entry_field = tkinter.Entry(master, textvariable=self.my_msg, width=95)
        self.entry_field.bind("<Return>", self.send_email)
        self.entry_field.pack()
        send_button = tkinter.Button(master, text="Send", command=self.send_email, width=50)
        send_button.pack()
        receive_thread = Thread(target=self.listen_email)
        receive_thread.start()


    def greet(self):
        print("Greetings!")

    def send_email(self):
        port = 465  # For SSL
        password = "vershu1317"
        remail = "rishismsservice@gmail.com"
        semail = "4163581222@txt.bell.ca"

        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(remail, password)
            msg = self.my_msg.get()
            self.my_msg.set("") 

            server.sendmail(remail, semail, f'{msg} - Rishi')  
            new_semail = semail.split("@")
            date = datetime.datetime.now()
            today = datetime.date.today()
            self.listbox.insert(tkinter.END, f'{today.year}/{today.month}/{today.year} - {date.hour}:{date.minute} - Rishi: {msg}')
            with open(f'{new_semail[0]}.txt', "a") as f:
                f.write(f'{today.year}/{today.month}/{today.year} - {date.hour}:{date.minute} - Rishi: {msg}\n')
                f.close()

    def listen_email(self):
        while True:
            imap_host = 'imap.gmail.com'
            imap_user = 'rishismsservice@gmail.com'
            imap_user_pass = "vershu1317"
            semail = "4163581222@txt.bell.ca"

            # init imap connection
            mail = imaplib.IMAP4_SSL(imap_host, 993)
            rc, resp = mail.login(imap_user, imap_user_pass)

            # select only unread messages from inbox
            mail.select('Inbox')
            status, data = mail.search(None, '(UNSEEN)')

            # for each e-mail messages, print text content
            for num in data[0].split():
                # get a single message and parse it by policy.SMTP (RFC compliant)
                status, data = mail.fetch(num, '(RFC822)')
                email_msg = data[0][1]
                email_msg = email.message_from_bytes(email_msg, policy=policy.SMTP)

                if str(email_msg['From']) == semail:

                    #print("\n----- MESSAGE START -----\n")

                    #print("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\n" % ( \
                        #str(email_msg['From']), \
                        #str(email_msg['To']), \
                        #str(email_msg['Date']), \
                        #str(email_msg['Subject'] )))

                    # print only message parts that contain text data
                    for part in email_msg.walk():
                        # download attachment and save it
                        filename = part.get_filename()
                        if filename:
                            folder_name = semail
                            if not os.path.isdir(folder_name):
                                # make a folder for this email (named after the subject)
                                os.mkdir(folder_name)
                            filepath = os.path.join(folder_name, filename)
                            open(filepath, "wb").write(part.get_payload(decode=True))
                    
                    f = open(f'{semail}/text_0.txt', "r")
                    new_semail = semail.split("@")
                    date = datetime.datetime.now()
                    today = datetime.date.today()
                    msg = f.read()
                    self.listbox.insert(tkinter.END, f'{today.year}/{today.month}/{today.year} - {date.hour}:{date.minute} - {new_semail[0]}: {msg}')
                    f.close()
                    with open(f'{new_semail[0]}.txt', "a") as f:
                        f.write(f'{today.year}/{today.month}/{today.year} - {date.hour}:{date.minute} - {new_semail[0]}: {msg}\n')
                        f.close()
                    os.system(f'cmd /c "rmdir /Q /S {semail}"')


                    #print("\n----- MESSAGE END -----\n")
                else:
                    return 


root = Tk()
root.geometry("600x600")
root.resizable(0,0)
my_gui = MyFirstGUI(root)
root.mainloop()
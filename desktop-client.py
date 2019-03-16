import tkinter as tk
from PIL import ImageTk, Image
import sqlite3 as sq
import requests
import json
from argon2 import PasswordHasher   

def main():   

    root= tk.Tk()
    root.title("Desktop-Client")
    root.geometry("600x600")
   
    ######### IP ADDRESS OF SERVER ################

    def check_server_ip_address(address):
        print("Reached here ",address)
        print("http://"+address+"/hello")
        # check_if_server= requests.get("http://"+address+"/hello")
        # check_if_server= requests.get("https://api.github.com/events")

        # if check_if_server.status_code == 200:
        if 1 == 1:
            print("Server is okay ")

            ##CheckBox Image
            canvas= tk.Canvas(main_ip_frame)
            image= Image.open("checkmark.png")
            image= image.resize((20, 20))
            canvas.img = ImageTk.PhotoImage(image)
            canvas.create_image(10, 10, image=canvas.img) 
            canvas.pack(side=tk.RIGHT)
            ########

            check_credentials['state']= 'normal'
            check_token['state']= 'normal'


        else:    
            print("Server is not okay") 

    def send_credentials(username, password):
        payload= {
            username: username,
            password: password
        }
        # receive_token= requests.post("http://"+address, data= payload)
        # print(receive_token.json())

        # token_from_server= json.loads(receive_token)
        token= "aaaa"
        print(username, password, token)
        conn = sq.connect('Desktop-Database.db')
        connection= conn.cursor()
        connection.execute("CREATE TABLE IF NOT EXISTS user_credentials (Username TEXT, Password TEXT, Token TEXT)") 
        connection.execute('INSERT INTO user_credentials (Username, Password, Token) VALUES (?, ?, ?)',(username, password, token)) 
        conn.commit()
    
    def send_token(token):
        payload= {
            token: token
        }
        # send_token= requests.post("http://"+address, data= payload)
        print(token)



    main_ip_frame= tk.Frame()
    ip_frame= tk.Frame(main_ip_frame) 
    ip= tk.StringVar(ip_frame)
    ip_label = tk.Label(ip_frame, text="Server IP Address")
    ip_entry= tk.Entry(ip_frame, textvariable= ip)
    ip_entry.pack(padx= 5, pady= 5, side=tk.RIGHT)
    ip_label.pack(padx= 5, pady= 5, side=tk.LEFT)
    ip_frame.bind("<FocusOut>", lambda event: check_server_ip_address(address= ip.get()))
    ip_frame.pack(side=tk.LEFT)
    main_ip_frame.pack()

    ########## USERNAME ################

    username_frame= tk.Frame()
    username= tk.StringVar(username_frame)
    username_label = tk.Label(username_frame, text="User Name")
    username_entry= tk.Entry(username_frame, textvariable= username)
    username_entry.pack(padx= 5, pady= 5, side=tk.RIGHT)
    username_label.pack(padx= 5, pady= 5, side=tk.LEFT)
    username_frame.pack()

    ########## PASSWORD ##################

    password_frame= tk.Frame()
    password= tk.StringVar(password_frame)
    password_label = tk.Label(password_frame, text="Password")
    password_entry= tk.Entry(password_frame, show= "*", textvariable= password)
    # password_entry.bind('<Return>',get_password)
    password_entry.pack(padx= 5, pady= 5, side= tk.RIGHT)
    password_label.pack(padx= 5, pady= 5, side= tk.LEFT)
    password_frame.pack()

    ########## CHECK CREDENTIALS OF USERNAME AND PASSWORD ######

    check_credentials= tk.Button(text= "Check!", state= tk.DISABLED, command= lambda: send_credentials(username= username.get(), password= password.get()))
    check_credentials.pack() 

    ########## TOKEN #####################

    token_frame= tk.Frame()
    token= tk.StringVar(token_frame)
    token_label = tk.Label(token_frame, text="Token")
    token_entry= tk.Entry(token_frame, textvariable= token)
    token_entry.pack(padx= 5, pady= 5, side=tk.RIGHT)
    token_label.pack(padx= 5, pady= 5, side=tk.LEFT)
    token_frame.pack()

    ########## CHECK TOKEN ######

    check_token= tk.Button(text= "Check Token!", state= tk.DISABLED, command= lambda: send_token(token= token.get()))
    check_token.pack()

    root.mainloop()

    print("Username ",username.get(), "\nPassword ",password.get(), "\nIP Address ",ip.get(),"\nToken ",token.get())

if __name__ == '__main__':
    main()
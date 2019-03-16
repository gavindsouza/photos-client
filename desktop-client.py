import tkinter as tk
from PIL import ImageTk, Image
import sqlite3 as sq
import requests   
global img

def main():   

    root= tk.Tk()
    root.title("Desktop-Client")
    root.geometry("600x600")
   
    ######### IP ADDRESS OF SERVER ################

    def check_server_ip_address(address):
        print("Reached here ",address)
        # check_if_server= requests.get("http://"+address+"/hello")
        # check_if_server= requests.get("https://api.github.com/events")

        if 1 == 1:
            print("Server is okay")
            canvas= tk.Canvas(main_ip_frame)
            image= Image.open("checkmark.png")
            image= image.resize((20, 20))
            canvas.img = ImageTk.PhotoImage(image)
            canvas.create_image(200, 200, image=canvas.img) 
            canvas.pack(side=tk.RIGHT)


        else:
            
            print("Server is not okay") 

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

    root.mainloop()


    print("Username ",username.get(), "\nPassword ",password.get(), "\nIP Address ",ip.get())

if __name__ == '__main__':
    main()
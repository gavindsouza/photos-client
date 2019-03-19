# imports - standard imports
import tkinter as tk
import sqlite3 as sq
import json
import os

# imports - third party imports
from PIL import ImageTk, Image
import requests
from argon2 import PasswordHasher


hasher = PasswordHasher()


def main():

    conn = sq.connect('client.db')
    connection = conn.cursor()

    root = tk.Tk()
    root.title("Desktop-Client")
    root.geometry("600x600")

    ######### IP ADDRESS OF SERVER ################

    def check_server_ip_address(address):
        print("Reached here ", address)
        print("http://"+address+":5000/hello")
        check_if_server = requests.get("http://"+address+":5000/hello")
        
        if check_if_server.status_code == 200:
            # if 1 == 1:
            print("Server is okay ")

            # CheckBox Image
            canvas = tk.Canvas(main_ip_frame)
            image = Image.open("checkmark.png")
            image = image.resize((20, 20))
            canvas.img = ImageTk.PhotoImage(image)
            canvas.create_image(10, 10, image=canvas.img)
            canvas.pack(side=tk.RIGHT)

            check_credentials['state'] = 'normal'
            check_token['state'] = 'normal'

        else:
            print("Server is not okay")

    def send_credentials(username, password, address):
        payload = {
            'username': username,
            'password': password
        }
        # receive_token= requests.post("http://"+address, data= payload)
        # print(receive_token.json())

        # token_from_server= json.loads(receive_token)
        token = "aaaa"
        print(username, password, token)
        connection.execute(
            "CREATE TABLE IF NOT EXISTS user_credentials (Username TEXT, Password TEXT, Token TEXT)")
        connection.execute('INSERT INTO user_credentials (Username, Password, Token) VALUES (?, ?, ?)',
                           (username, ph.hash(password), ph.hash(token)))
        conn.commit()

        send_pictures(token, address)

    def send_pictures(token, address):

        image = [
            "ase",
            "art",
            "bmp",
            "blp",
            "cd5",
            "cit",
            "cpt",
            "cr2",
            "cut",
            "dds",
            "dib",
            "djvu",
            "egt",
            "exif",
            "gif",
            "gpl",
            "grf",
            "icns",
            "ico",
            "iff",
            "jng",
            "jpeg",
            "jpg",
            "jfif",
            "jp2",
            "jps",
            "lbm",
            "max",
            "miff",
            "mng",
            "msp",
            "nitf",
            "ota",
            "pbm",
            "pc1",
            "pc2",
            "pc3",
            "pcf",
            "pcx",
            "pdn",
            "pgm",
            "PI1",
            "PI2",
            "PI3",
            "pict",
            "pct",
            "pnm",
            "pns",
            "ppm",
            "psb",
            "psd",
            "pdd",
            "psp",
            "px",
            "pxm",
            "pxr",
            "qfx",
            "raw",
            "rle",
            "sct",
            "sgi",
            "rgb",
            "int",
            "bw",
            "tga",
            "tiff",
            "tif",
            "vtf",
            "xbm",
            "xcf",
            "xpm",
            "3dv",
            "amf",
            "ai",
            "awg",
            "cgm",
            "cdr",
            "cmx",
            "dxf",
            "e2d",
            "egt",
            "eps",
            "fs",
            "gbr",
            "odg",
            "svg",
            "stl",
            "vrml",
            "x3d",
            "sxd",
            "v2d",
            "vnd",
            "wmf",
            "emf",
            "art",
            "xar",
            "png",
            "webp",
            "jxr",
            "hdp",
            "wdp",
            "cur",
            "ecw",
            "iff",
            "lbm",
            "liff",
            "nrrd",
            "pam",
            "pcx",
            "pgf",
            "sgi",
            "rgb",
            "rgba",
            "bw",
            "int",
            "inta",
            "sid",
            "ras",
            "sun",
            "tga"
        ]

        img = []

        def tree(path, *args):
            if path != '':
                path = path
            else:
                path = args
            try:
                for object in os.listdir(path):
                    if os.path.isdir(path + '/' + object):
                        tree(path + '/' + object)
                    elif os.path.isfile(path + '/' + object):
                        ext = object.split('.')[-1]
                        if ext in image:
                            img.append('{0}/{1}'.format(path, object))

            # except NotADirectoryError or FileNotFoundError or OSError or PermissionError:
            except Exception as e:
                pass

        path = "/home/aarish/aarish/mh2019"
        tree(path)
        print(img)

        for path in img:
            data = {
                'path': path,
                'media': open(path, 'rb'),
                'token': token,
                'enctype': 'multipart/form-data'
            }
            print(data)
            send_image = requests.post(
                "http://"+address+":5000/api/v1/upload", data=data)

    def send_token(token):
        payload = {
            'token': token
        }
        # send_token= requests.post("http://"+address, data= payload)
        print(token)

    main_ip_frame = tk.Frame()
    ip_frame = tk.Frame(main_ip_frame)
    ip = tk.StringVar(ip_frame)
    ip_label = tk.Label(ip_frame, text="Server IP Address")
    ip_entry = tk.Entry(ip_frame, textvariable=ip)
    ip_entry.pack(padx=5, pady=5, side=tk.RIGHT)
    ip_label.pack(padx=5, pady=5, side=tk.LEFT)
    ip_frame.bind(
        "<FocusOut>", lambda event: check_server_ip_address(address=ip.get()))
    ip_frame.pack(side=tk.LEFT)
    main_ip_frame.pack()

    ########## USERNAME ################

    username_frame = tk.Frame()
    username = tk.StringVar(username_frame)
    username_label = tk.Label(username_frame, text="User Name")
    username_entry = tk.Entry(username_frame, textvariable=username)
    username_entry.pack(padx=5, pady=5, side=tk.RIGHT)
    username_label.pack(padx=5, pady=5, side=tk.LEFT)
    username_frame.pack()

    ########## PASSWORD ##################

    password_frame = tk.Frame()
    password = tk.StringVar(password_frame)
    password_label = tk.Label(password_frame, text="Password")
    password_entry = tk.Entry(password_frame, show="*", textvariable=password)
    # password_entry.bind('<Return>',get_password)
    password_entry.pack(padx=5, pady=5, side=tk.RIGHT)
    password_label.pack(padx=5, pady=5, side=tk.LEFT)
    password_frame.pack()

    ########## CHECK CREDENTIALS OF USERNAME AND PASSWORD ######

    check_credentials = tk.Button(text="Check!", state=tk.DISABLED, command=lambda: send_credentials(
        username=username.get(), password=password.get(), address=ip.get()))
    check_credentials.pack()

    ########## TOKEN #####################

    token_frame = tk.Frame()
    token = tk.StringVar(token_frame)
    token_label = tk.Label(token_frame, text="Token")
    token_entry = tk.Entry(token_frame, textvariable=token)
    token_entry.pack(padx=5, pady=5, side=tk.RIGHT)
    token_label.pack(padx=5, pady=5, side=tk.LEFT)
    token_frame.pack()

    ########## CHECK TOKEN ######

    check_token = tk.Button(text="Check Token!", state=tk.DISABLED,
                            command=lambda: send_token(token=token.get()))
    check_token.pack()

    root.mainloop()

    print("Username ", username.get(), "\nPassword ", password.get(),
          "\nIP Address ", ip.get(), "\nToken ", token.get())


if __name__ == '__main__':
    conn = sq.connect('client.db')
    connection = conn.cursor()

    connection.execute("SELECT * FROM user_credentials")
    conn.commit()

    data = connection.fetchall()

    # if data:
    #     print("Not Empty")

    # else:
    print("Empty")
    main()

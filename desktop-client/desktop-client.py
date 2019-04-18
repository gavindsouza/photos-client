# imports - standard imports
import tkinter as tk
import sqlite3
import json
import os
import ntpath

# imports - third party imports
from PIL import ImageTk, Image
import requests
from argon2 import PasswordHasher


supported_img_list = [
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
hasher = PasswordHasher()


class Database(object):
    DB_LOCATION = 'client.db'

    def __init__(self):
        self.connection = sqlite3.connect(Database.DB_LOCATION)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS user_credentials (Username TEXT, Password TEXT, Token TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS img_path (Image TEXT)")
        self.commit()

    def commit(self):
        self.connection.commit()

    def get_user_credentials(self):
        self.cursor.execute("SELECT * FROM user_credentials")
        username, password, token = self.cursor.fetchall()

        return username, password, token

    def add_user_credentials(self, user_name, password, token):
        self.cursor.execute("INSERT INTO user_credentials (Username, Password, Token) VALUES (?, ?, ?)",
                            (user_name, hasher.hash(password), hasher.hash(token)))
        self.commit()

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()


def check_server_ip_address(address):
    check_if_server = requests.get("http://"+address+":5000/hello")

    if check_if_server.status_code == 200:
        print("Server exists!")
        return True

    else:
        print("Server is not okay")
        return False


def receive_token(username, password, address):
    payload = {
        'username': username,
        'password': password
    }

    receive_token = requests.post("http://"+address, data=payload)

    print(receive_token.json())
    token_from_server = json.loads(receive_token)

    return token_from_server
    


def gen_img_list(path, *args):
    img_path_list = []

    if path != '':
        path = path
    else:
        path = args
        try:
            for object in os.listdir(path):
                if os.path.isdir(path + '/' + object):
                    gen_img_list(path + '/' + object)
                elif os.path.isfile(path + '/' + object):
                    ext = object.split('.')[-1]
                    if ext in supported_img_list:
                        img_path_list.append('{0}/{1}'.format(path, object))

        # except NotADirectoryError or FileNotFoundError or OSError or PermissionError:
        except Exception:
            pass

    return img_path_list


def send_pictures(token, address, img_list):
    total_num = len(img_list)
    
    for curr_num, img_path in enumerate(img_list):
        data = {
            'path': img_path,
            'file_name' : ntpath.basename(img_path),
            'media': open(img_path, 'rb'),
            'token': token,
            'enctype': 'multipart/form-data'
        }
        print(data)
        send_image = requests.post(
            "http://"+address+":5000/api/v1/upload", data=data)


def send_token(token, address):
    payload = {
        'token': token
    }
    send_token = requests.post("http://"+address, data=payload)
    print(token)


def main():
    root = tk.Tk()
    root.title("Desktop-Client")
    root.geometry("600x600")

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
    path = "/home/gavin"
    img = gen_img_list(path)
    print(img)

    # Set up the database for credentials
    with Database() as db:
        db.commit()


    # Set up the database for img_path_list

    # Check connection to server
    #   input address
    #   if exists:
    #
        # # CheckBox Image
        # canvas = tk.Canvas(main_ip_frame)
        # image = Image.open("utils/checkmark.png")
        # image = image.resize((20, 20))
        # canvas.img = ImageTk.PhotoImage(image)
        # canvas.create_image(10, 10, image=canvas.img)
        # canvas.pack(side=tk.RIGHT)

        # check_credentials['state'] = 'normal'
        # check_token['state'] = 'normal'
    # else
    # dont

    main()

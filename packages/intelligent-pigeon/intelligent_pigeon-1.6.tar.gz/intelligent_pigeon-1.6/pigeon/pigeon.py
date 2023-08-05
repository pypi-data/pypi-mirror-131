from object_detector import *
import requests
from object_detector import *
import os
import sys
from getpass import getpass
from datetime import datetime
import cv2

class Server:
    def __init__(self,server_url):
        self.server_url = server_url
        if self.server_url[-1]!='/':
            self.server_url+='/'

    def register(self,first_name,last_name,username,password,re_password):
        content = {
            "first_name":first_name,
            "last_name":last_name,
            "username":username,
            "password":password,
            "re_password":re_password
        }
        r = requests.post(self.server_url+"account/register/",data=content)
        print(r.status_code)
        print(r.content)

    # register("Ujjwal","Kar","ujjwal","123456789","123456789")

    def send_file(self,username,password,location,image):
        content={
            "username":username,
            "password":password,
            "location":location,
        }

        files={
            "image":open(image,"rb")
        }
        r = requests.post(self.server_url+"post",data=content, files=files)
        print(r.status_code)
        print(r.content)

argv = sys.argv
task = argv[1]

if task=="extract":
    try:
        output_path = argv[3]
    except:
        sys.exit("""
Correct command is: 
    python pigeon.py extract video_path output_path
                or
    python pigeon.py extract 0 output_path
        """)
    
    try:    
        ext = ExtractImages(path=int(argv[2]),op=output_path)
    except ValueError:
        ext = ExtractImages(path=argv[2],op=output_path)
    ext.extract("A","B","C","D")

elif task=="send":
    labeled = False
    try:
        server_urls = argv[2]
        relative_path = argv[3]
        weights = argv[4]
        with open(argv[5],'r') as f:
            classes = f.read().splitlines()
        try:
            if (argv[4] == 'labeled'):
                labeled = True
        except:
            pass

    except IndexError:
        sys.exit(""" Correct command is...
        python pigeon.py send <server_name> <relarive path> weights classes.txt labeled
        """)
    s = Server(server_urls)
    username = input("Username: ")
    password = getpass()
    write_dir = "Temp"
    try:
        os.mkdir(write_dir)
    except FileExistsError:
        pass

    obj = ObjectDetector(weights=weights, cfg="yolov4-custom.cfg", classes=classes)

    for i in os.listdir(os.path.join(relative_path)):
        path = os.path.join(relative_path,i)
        img_arr = obj.detect_object(path,label=labeled,detected_only=True)
        os.remove(path)
        dt = datetime.now()
        img_nm = f'{dt.year}-{dt.month}-{dt.day}|{dt.hour}:{dt.minute}:{dt.second}::{dt.microsecond}.jpg'
        try:
            if img_arr.all() != None:
                cv2.imwrite(f"{write_dir}/{img_nm}", img_arr)
                s.send_file(username,password,"abc",f"{write_dir}/{img_nm}")
                os.remove(f"{write_dir}/{img_nm}")
        except AttributeError:
            pass      
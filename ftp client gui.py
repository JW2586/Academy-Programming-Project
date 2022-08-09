import tkinter
from tkinter import BOTH, END, LEFT
import ftplib
ftp = ftplib.FTP()

def connectServer():
    ip = ent_ip.get()
    port = int(ent_port.get())
    try:
        msg = ftp.connect(ip,port)
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,msg)
        lbl_login.place(x=150,y=20)
        ent_login.place(x=150,y=43)
        lbl_pass.place(x=150,y=70)
        ent_pass.place(x=150,y=93)
        btn_login.place(x=182,y=120)
        lbl_input.place(x=280,y=20)
        ent_input.place(x=280,y=43)
        btn_downfile.place(x=280,y=80)
        btn_quit.place(x=280,y=120)
    except:
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"Unable to connect")

def loginServer():
    user = ent_login.get()
    password = ent_pass.get()
    try:
        msg = ftp.login(user,password)
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,msg)
    except:
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"Unable to login")
    
def downloadFile():
    file = ent_input.get()
    ## file name validation here
    down = open(file, "wb")
    try:
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"Downloading " + file + "...")
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,ftp.retrbinary("RETR " + file, down.write))
    except:
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"Unable to download file")
    displayDir()
    
def closeConnection():
    try:
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"Closing connection...")
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,ftp.quit())
    except:
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"Unable to disconnect")

window = tkinter.Tk()
window.title("FTP Client")
window.wm_iconbitmap("favicon.ico")
window.geometry("420x600")
window.configure(bg='#2e2e2e')

#Connect
lbl_ip = tkinter.Label(window, text="IP Address")
ent_ip = tkinter.Entry(window)
lbl_port = tkinter.Label(window, text="Port")
ent_port = tkinter.Entry(window)
btn_connect = tkinter.Button(window, text="Connect", command=connectServer)

#Server response text box
text_servermsg = tkinter.Text(window,width=45,height=20)

#Login
lbl_login = tkinter.Label(window, text="Username")
ent_login = tkinter.Entry(window)
lbl_pass = tkinter.Label(window, text="Password")
ent_pass = tkinter.Entry(window)
btn_login = tkinter.Button(window, text="Login", command=loginServer)

#Directory listing
lbl_dir = tkinter.Label(window, text="Directory listing:")
libox_serverdir = tkinter.Listbox(window,width=40,height=14)

#Options
lbl_input = tkinter.Label(window, text="Input")
ent_input = tkinter.Entry(window)
btn_downfile = tkinter.Button(window, text="Download File", command=downloadFile,width=15)
btn_quit = tkinter.Button(window, text="Disconnect", command=closeConnection,width=15)

#Place widgits
lbl_ip.place(x=20,y=20)
ent_ip.place(x=20,y=43)
lbl_port.place(x=20,y=70)
ent_port.place(x=20,y=93)
btn_connect.place(x=52,y=120)
text_servermsg.place(x=20,y=150)

#Create
window.mainloop()

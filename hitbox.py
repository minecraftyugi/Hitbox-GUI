# -*- coding: utf-8 -*-
import logging
logging.basicConfig()
from Tkinter import *
from tkFont import *
from websocket import *
from threading import *
from PIL import ImageTk, Image
from StringIO import StringIO
import ttk, requests, sys, os, os.path, json, time, string, random, re, math, base64

base = "https://api.hitbox.tv/"
base2 = "http://edge.sf.ak.hitbox.tv/"
scrollClickCheck = 0
usercolor = ""

master = Tk()

def donothing():
    filewin = Toplevel()
    filewin.minsize(width=400,height=200)
    filewin.geometry("+0+0")
    filewin.resizable(0,0)
    button = Button(filewin, text="Do nothing button")
    button.pack()
    return

def colorEnter(event):
    global text2
    text2.config(state=NORMAL)
    text2.delete("1.0", END)
    text2.insert(END, "COLOR OPTIONS\n\n")
    text2.tag_config("bold", foreground="red", justify=CENTER, underline=TRUE)
    text2.tag_add("bold", "1.0", "1.end")
    text2.insert(END, "HEXCODE: ")
    text2.tag_config("optionList", foreground="red", font=font4)
    text2.tag_add("optionList", "3.0", "3.end")
    text2.insert(END, "Enter a valid 6 digit RGB hexcode as your username color. For example: ABC123.\n\n")
    text2.tag_config("black", font=font2)
    text2.tag_add("black", "3.0 + 9c", "3.end")
    text2.insert(END, "HITBOX: ")
    text2.tag_add("optionList", "5.0", "5.end")
    text2.insert(END, "Get a default random Hitbox color as your username color.")
    text2.tag_add("black", "5.0 + 8c", "5.end")
    text2.config(state=DISABLED)
    return

def eliteEnter(event):
    global text2
    text2.config(state=NORMAL)
    text2.delete("1.0", END)
    text2.insert(END, "ELITE SPEAK OPTIONS\n\n")
    text2.tag_config("bold", foreground="red", justify=CENTER, underline=TRUE)
    text2.tag_add("bold", "1.0", "1.end")
    text2.insert(END, "YES: ")
    text2.tag_config("optionList", foreground="red", font=font4)
    text2.tag_add("optionList", "3.0", "3.end") 
    text2.insert(END, "Convert your message into 3l173 5p34k.\n\n")
    text2.tag_config("black", font=font2)
    text2.tag_add("black", "3.0 + 5c", "3.end")
    text2.insert(END, "NO: ")
    text2.tag_add("optionList", "5.0", "5.end")
    text2.insert(END, "Leave your message the way it is typed.")
    text2.tag_add("black", "5.0 + 4c", "5.end")
    text2.config(state=DISABLED)
    return

def encodeEnter(event):
    global text2
    text2.config(state=NORMAL)
    text2.delete("1.0", END)
    text2.insert(END, "SCRAMBLE OPTIONS\n\n")
    text2.tag_config("bold", foreground="red", justify=CENTER, underline=TRUE)
    text2.tag_add("bold", "1.0", "1.end")
    text2.insert(END, "YES: ")
    text2.tag_config("optionList", foreground="red", font=font4)
    text2.tag_add("optionList", "3.0", "3.end") 
    text2.insert(END, "Scramble your message so only TB Hibox Client users can read it.\n\n")
    text2.tag_config("black", font=font2)
    text2.tag_add("black", "3.0 + 5c", "3.end")
    text2.insert(END, "NO: ")
    text2.tag_add("optionList", "5.0", "5.end")
    text2.insert(END, "Leave your message the way it is typed.")
    text2.tag_add("black", "5.0 + 4c", "5.end")
    text2.config(state=DISABLED)
    return

def ignoreEnter(event):
    global text2
    text2.config(state=NORMAL)
    text2.delete("1.0", END)
    text2.insert(END, "IGNORE OPTIONS\n\n")
    text2.tag_config("bold", foreground="red", justify=CENTER, underline=TRUE)
    text2.tag_add("bold", "1.0", "1.end")
    text2.insert(END, "YES: ")
    text2.tag_config("optionList", foreground="red", font=font4)
    text2.tag_add("optionList", "3.0", "3.end") 
    text2.insert(END, "Ignores all global chat messages. Useful for only reading whispers.\n\n")
    text2.tag_config("black", font=font2)
    text2.tag_add("black", "3.0 + 5c", "3.end")
    text2.insert(END, "NO: ")
    text2.tag_add("optionList", "5.0", "5.end")
    text2.insert(END, "Allow global chat messages to be seen.")
    text2.tag_add("black", "5.0 + 4c", "5.end")
    text2.config(state=DISABLED)
    return

def labelLeave(event):
    global text2
    text2.config(state=NORMAL)
    text2.delete("1.0", END)
    text2.insert(END, "CHAT COMMANDS\n\n")
    text2.tag_config("bold", foreground="red", justify=CENTER, underline=TRUE)
    text2.tag_add("bold", "1.0", "1.13")
    text2.insert(END, "/w user message ")
    text2.tag_config("bold2", foreground="red", font=font2)
    text2.tag_add("bold2", "3.0", "3.15")
    text2.insert(END, "Whisper a message to the specified user.\n\n")
    text2.tag_config("bold3", font=font3)
    text2.tag_add("bold3", "3.15", "3.56")
    text2.insert(END, "/wspam user ")
    text2.tag_add("bold2", "5.0", "5.12")
    text2.insert(END, "Whisper random symbols to the specified user at a rate of 8 whisper messages / second. Throttles chat.\n\n")
    text2.tag_add("bold3", "5.12", "5.114")
    text2.insert(END, "/wspam2 user ")
    text2.tag_add("bold2", "7.0", "7.13")
    text2.insert(END, "Whisper random symbols to the specified user at a rate of 8 whisper messages / second. Use if banned.\n\n")
    text2.tag_add("bold3", "7.13", "7.114")
    text2.insert(END, "/ignore user ")
    text2.tag_add("bold2", "9.0", "9.13")
    text2.insert(END, "Ignore the specified user's messages from appearing in chat. Whisper messages will still be shown. Typing /ignore user will unignore the user if already ignored.\n\n")
    text2.tag_add("bold3", "9.13", "9.174")
    text2.insert(END, "/follow user ")
    text2.tag_add("bold2", "11.0", "11.13")
    text2.insert(END, "Follow the specified user.\n\n")
    text2.tag_add("bold3", "11.13", "11.39")
    text2.insert(END, "/unfollow user ")
    text2.tag_add("bold2", "13.0", "13.15")
    text2.insert(END, "Unfollow the specified user.\n\n")
    text2.tag_add("bold3", "13.15", "13.43")

    text2.config(state=DISABLED)
    text2.yview("0")

    return

def scrollClickSet(event="event"):
    global scrollClickCheck
    scrollClickCheck = 1
    scrollClick()
    return

def scrollClick(event="event"):
    global scrollClickCheck
    global returnBtn

    if scrollClickCheck == 0:
        text.yview(END)
    else:
        text.update_idletasks()
        try:
            returnBtn
        except NameError:
            returnBtn = Button(text, text="Go To Bottom", relief="groove", command=bottomClick)
            returnBtn.place(x=text.winfo_width()-returnBtn.winfo_reqwidth()-2,y=text.winfo_height()-returnBtn.winfo_reqheight()-2)
            returnBtn.bind("<Enter>", bottomEnter)
            returnBtn.bind("<Leave>", bottomLeave)
            return
    return

def bottomEnter(event="event"):
    returnBtn.config(cursor="hand2")
    return

def bottomLeave(event="event"):
    returnBtn.config(cursor="")
    return

def bottomClick(event="event"):
    global scrollClickCheck
    global returnBtn
    returnBtn.destroy()
    scrollClickCheck = 0
    text.yview(END)
    del returnBtn
    return

def userOptions(event):
    userwindow = Toplevel()
    minwidth = 100
    minheight = 100
    userwindow.minsize(width=minwidth, height=minheight)
    x = (master.winfo_screenwidth() - minwidth)/2
    y = (master.winfo_screenheight() - minheight)/2
    userwindow.geometry("+"+str(x)+"+"+str(y))

    count = IntVar()
    pattern = r'[-\w]+'

    # find the beginning of the "word", starting _after_
    # the character clicked on
    start = "@%d,%d +1c" % (event.x, event.y)
    index1 = text3.search(pattern, start, backwards=True, regexp=True)

    # starting with the beginning, find the end and save
    # the number of characters that matched.
    text3.search(pattern, index1, regexp=True, count=count)

    # compute the ending index of the match
    index2=text3.index("%s+%s c" % (index1, count.get()))

    # get the text
    user = text3.get(index1, index2)
    print user

    def mentionBtn():
        entry.delete(0, END)
        entry.insert(0, "@"+user)
        userwindow.destroy()
        return

    def whisperBtn():
        entry.delete(0, END)
        entry.insert(0, "/w "+user)
        userwindow.destroy()
        return

    def ignoreBtn():
        entry.delete(0, END)
        entry.insert(0, "/ignore "+user)
        userwindow.destroy()
        return

    def followBtn():
        entry.delete(0, END)
        entry.insert(0, "/follow "+user)
        userwindow.destroy()
        return

    def unfollowBtn():
        entry.delete(0, END)
        entry.insert(0, "/unfollow "+user)
        userwindow.destroy()
        return
    
    label = Label(userwindow, text=user, font=font, padx=5)
    label.pack(side=TOP)
    payload = {"authToken" : token}
    results = requests.get(base + "user/" + user, params = payload).json()
    logo = results["user_logo_small"]
    amount = results["followers"]
    results = base2 + logo
    img = requests.get(results)
    img = Image.open(StringIO(img.content))
    img = ImageTk.PhotoImage(img)
    label2 = Label(userwindow, image=img, bd=10)
    label2.image = img
    label2.pack(side=TOP)
    label4 = Label(userwindow, text="Followers: "+str(amount), padx=5, font=font2)
    label4.pack(side=TOP)
    label3 = Label(userwindow)
    label3.pack(side=TOP)
    button = Button(label3, text="Mention", command=mentionBtn)
    button.pack(side=TOP, fill=X)
    button = Button(label3, text="Whisper", command=whisperBtn)
    button.pack(side=TOP, fill=X)
    button = Button(label3, text="Ignore/Unignore", command=ignoreBtn)
    button.pack(side=TOP, fill=X)
    button = Button(label3, text="Follow", command=followBtn)
    button.pack(side=TOP, fill=X)
    button = Button(label3, text="Unfollow", command=unfollowBtn)
    button.pack(side=TOP, fill=X)
  
    return

def userOptions2(event):
    userwindow = Toplevel()
    minwidth = 100
    minheight = 100
    userwindow.minsize(width=minwidth, height=minheight)
    x = (master.winfo_screenwidth() - minwidth)/2
    y = (master.winfo_screenheight() - minheight)/2
    userwindow.geometry("+"+str(x)+"+"+str(y))

    count = IntVar()
    pattern = r'[-\w]+'

    # find the beginning of the "word", starting _after_
    # the character clicked on
    start = "@%d,%d +1c" % (event.x, event.y)
    index1 = text.search(pattern, start, backwards=True, regexp=True)

    # starting with the beginning, find the end and save
    # the number of characters that matched.
    text.search(pattern, index1, regexp=True, count=count)

    # compute the ending index of the match
    index2=text.index("%s+%s c" % (index1, count.get()))

    # get the text
    user = text.get(index1, index2)
    print user

    def mentionBtn():
        entry.delete(0, END)
        entry.insert(0, "@"+user)
        userwindow.destroy()
        return

    def whisperBtn():
        entry.delete(0, END)
        entry.insert(0, "/w "+user)
        userwindow.destroy()
        return

    def ignoreBtn():
        entry.delete(0, END)
        entry.insert(0, "/ignore "+user)
        userwindow.destroy()
        return

    def followBtn():
        entry.delete(0, END)
        entry.insert(0, "/follow "+user)
        userwindow.destroy()
        return

    def unfollowBtn():
        entry.delete(0, END)
        entry.insert(0, "/unfollow "+user)
        userwindow.destroy()
        return
    
    label = Label(userwindow, text=user, font=font, padx=5)
    label.pack(side=TOP)
    payload = {"authToken" : token}
    results = requests.get(base + "user/" + user, params = payload).json()
    logo = results["user_logo_small"]
    amount = results["followers"]
    results = base2 + logo
    img = requests.get(results)
    img = Image.open(StringIO(img.content))
    img = ImageTk.PhotoImage(img)
    label2 = Label(userwindow, image=img, bd=10)
    label2.image = img
    label2.pack(side=TOP)
    label4 = Label(userwindow, text="Followers: "+str(amount), padx=5, font=font2)
    label4.pack(side=TOP)
    label3 = Label(userwindow)
    label3.pack(side=TOP)
    button = Button(label3, text="Mention", command=mentionBtn)
    button.pack(side=TOP, fill=X)
    button = Button(label3, text="Whisper", command=whisperBtn)
    button.pack(side=TOP, fill=X)
    button = Button(label3, text="Ignore/Unignore", command=ignoreBtn)
    button.pack(side=TOP, fill=X)
    button = Button(label3, text="Follow", command=followBtn)
    button.pack(side=TOP, fill=X)
    button = Button(label3, text="Unfollow", command=unfollowBtn)
    button.pack(side=TOP, fill=X)
  
    return

def userEnter(event):
    text.config(cursor="hand2")
    text3.config(cursor="hand2")
    return

def userLeave(event):
    text.config(cursor="arrow")
    text3.config(cursor="arrow")
    return

def btnEnter(event):
    inputbtn.config(cursor="hand2")
    return

def btnLeave(event):
    inputbtn.config(cursor="arrow")
    return

def closing():
    master.destroy()
    os._exit(0)
    return

def channel():
    return

def userlist():
    ws.send('5:::{"name":"message","args":[{"method":"getChannelUserList","params":{"channel":"'+channel+'"}}]}')
    return

def whisper(receiver, message, channel=channel()):
    return

def createspam():
    spam = ""
    for i in range(300):
        letter = random.SystemRandom().choice(string.ascii_uppercase)
        spam += letter
    return spam

def spam():
    for i in range(100000000):
        message = createspam()
        time.sleep(1.0001)
        ws.send('5:::{"name":"message","args":[{"method":"chatMsg","params":{"channel":"'+channel+'","name":"'+user+'","nameColor":"'+nameColor+'","text":"'+message+'"}}]}')
        message = createspam()
        time.sleep(0.0001)
        ws.send('5:::{"name":"message","args":[{"method":"chatMsg","params":{"channel":"'+channel+'","name":"'+user+'","nameColor":"'+nameColor+'","text":"'+message+'"}}]}')
    spam()
    return

def whisperspam(receiver):
    for i in range(100000000):
        message = createspam()
        time.sleep(0.05)
        ws.send('5:::{"name":"message","args":[{"method":"directMsg","params":{"channel":"'+channel+'","from":"'+user+'","to":"'+receiver+'","nameColor":"'+nameColor+'","text":"'+message+'"}}]}')
    whisperspam(receiver)
    return

def whisperspam2(receiver, channel=channel()):
    for i in range(4):
        message = createspam()
        time.sleep(0.005)
        ws.send('5:::{"name":"message","args":[{"method":"directMsg","params":{"channel":"'+channel+'","from":"'+user+'","to":"'+receiver+'","nameColor":"'+nameColor+'","text":"'+message+'"}}]}')
    whisperspam2()
    return

def elite(message):
    message = message.replace("a", "4")
    message = message.replace("e", "3")
    message = message.replace("g", "6")
    message = message.replace("i", "1")
    message = message.replace("o", "0")
    message = message.replace("s", "5")
    message = message.replace("t", "7")
    message = message.replace("A", "4")
    message = message.replace("E", "3")
    message = message.replace("G", "6")
    message = message.replace("I", "1")
    message = message.replace("O", "0")
    message = message.replace("S", "5")
    message = message.replace("T", "7")
    return message

def rainbow(**kwargs):
    values = {"freq1" : 0.1, "freq2" : 0.1, "freq3" : 0.1,
            "shift1" : 0, "shift2" : 2*math.pi/3, "shift3" : 4*math.pi/3,
            "center" : 128, "width" : 127, "length" : int(math.ceil(20*math.pi)),
            "start" : 0}

    for key, value in kwargs.iteritems():
        values[key] = value

    colorList = []    
    for i in range(values["start"], values["length"]+values["start"]):
        red = int(round(math.sin(values["freq1"]*i + values["shift1"]) * values["width"] + values["center"]))
        green = int(round(math.sin(values["freq2"]*i + values["shift2"]) * values["width"] + values["center"]))
        blue = int(round(math.sin(values["freq3"]*i + values["shift3"]) * values["width"] + values["center"]))
        color = '%02x%02x%02x' % (red, green, blue)
        colorList.append(color)
    return colorList

#Window operations
master.wm_title("TB Hitbox Client")
master.protocol("WM_DELETE_WINDOW",closing)
font=Font(family="Arial",size=12)
font2=Font(family="Arial",size=10)
font3=Font(family="Arial",size=10,slant=ITALIC)
font4=Font(family="Arial",size=10,weight=BOLD)
master.withdraw()
minwidth = master.winfo_screenwidth()/4*3
minheight = master.winfo_screenheight()/4*3
master.minsize(width=minwidth, height=minheight)
x = (master.winfo_screenwidth() - minwidth)/2
y = (master.winfo_screenheight() - minheight)/2
master.geometry("+"+str(x)+"+"+str(y))
master.deiconify()
master.resizable(0,0)
##width = master.winfo_screenwidth()
##height = master.winfo_screenheight()
##master.maxsize(width=width, height=height)

#Get logo
logo = requests.get("http://i.imgur.com/XlJvbit.png", headers={"user-agent": "curl/7.84.0"})
logo = Image.open(StringIO(logo.content))
logo = logo.resize((minwidth/2, minheight/2), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(logo)

#Home page
abc = Button(master, text="Hitbox")
abc.pack()

f1 = Frame(master, width=minwidth/2, height=minheight/2)
f1.pack(side=TOP)
f2 = Frame(master, width=minwidth/2, height=abc.winfo_reqheight())
f2.pack(side=TOP)
f3 = Frame(master, width=minwidth/2, height=abc.winfo_reqheight())
f3.pack(side=TOP)
f4 = Frame(master, width=minwidth/2, height=abc.winfo_reqheight())
f4.pack(side=TOP)
f5 = Frame(master, width=minwidth/4, height=abc.winfo_reqheight())
f5.pack(side=TOP)

abc.destroy()

l0 = Label(f1, image=logo)
l0.image = logo
l0.pack(fill=BOTH, expand=TRUE)
    
l1 = Label(f2, text="Hitbox Username:")
l2 = Label(f3, text="Hitbox Password:")
l3 = Label(f4, text="Hitbox Channel:")
l1.place(anchor="nw")
l2.place(anchor="nw")
l3.place(anchor="nw")

e1 = Entry(f2)
e2 = Entry(f3, show="*")
e3 = Entry(f4)
e1.place(x=l1.winfo_reqwidth()+10, width=(minwidth/2)-10-l1.winfo_reqwidth())
e2.place(x=l1.winfo_reqwidth()+10, width=(minwidth/2)-10-l1.winfo_reqwidth())
e3.place(x=l1.winfo_reqwidth()+10, width=(minwidth/2)-10-l1.winfo_reqwidth())

#Login File
if os.path.exists("login.txt") == True:
    loginFile = open("login.txt", "r")
    for line in loginFile:
        if "Username" in line:
            username = line.split(":")
            username = username[1].strip()
            e1.insert(END, username)
        if "Password" in line:
            password = line.split(":")
            password = password[1].strip()
            e2.insert(END, password)
        if "Channel" in line:
            channel = line.split(":")
            channel = channel[1].strip()
            e3.insert(END, channel)
    loginFile.close()
    try:
        username, password, channel
    except NameError:
        print "ERROR!"
        loginFile = open("login.txt", "w")
        loginFile.write("TB Hitbox Client\n")
        loginFile.write("Username:\n")
        loginFile.write("Password:\n")
        loginFile.write("Channel:\n")
        loginFile.close()
else:
    loginFile = open("login.txt", "w")
    loginFile.write("TB Hitbox Client\n")
    loginFile.write("Username:\n")
    loginFile.write("Password:\n")
    loginFile.write("Channel:\n")
    loginFile.close()

#TKinter login
def login():
    global user
    global password
    global channel
    global token
    global colorList
    user = e1.get()
    password = e2.get()
    channel = e3.get().lower()
    payload = {"login" : user, "pass" : password}
    
    #Send login
    login = requests.post(base + "auth/token", data = payload)
    response = login.json()

    if "authToken" in response:
        token = response["authToken"]
        loginFile = open("login.txt", "w")
        loginFile.write("TB Hitbox Client\n")
        loginFile.write("Username: "+user+"\n")
        loginFile.write("Password: "+password+"\n")
        loginFile.write("Channel: "+channel+"\n")
        loginFile.close()
        print token
        colorList = rainbow(center=158, width=97)
    else:
        print "Login failed!"
        closing()

    #Remove widgets
    f1.destroy()
    f2.destroy()
    f3.destroy()
    f4.destroy()
    f5.destroy()

    getserver()
    return

#Input button
inputbtn = Button(f5, text='CONNECT', command=login, bg="black", fg="white")
inputbtn.place(width=minwidth/4)
inputbtn.bind("<Enter>", btnEnter)
inputbtn.bind("<Leave>", btnLeave)

#Get server
def getserver():
    global entry
    global combo
    global combo2
    global combo3
    global combo4
    global text
    global text2
    global text3
    
    def sendmsg(event=""):
        global nameColor
        global rainbowColor
        colorCheck = combo.get()
        if colorCheck == "Red":
            nameColor = "FF0000"
        elif colorCheck == "Silver":
            nameColor = "C0C0C0"
        elif colorCheck == "Black":
            nameColor = "000000"
        else:
            try:
                rainbowColor
            except NameError:
                rainbowColor = random.SystemRandom().choice(colorList)
            nameColor = rainbowColor
        eliteCheck = combo2.get()
        encodeCheck = combo3.get()
        ignoreCheck = combo4.get()
        message = entry.get()
        entry.delete(0, END)
        message.strip()
        message = message.replace('\\', '\\\\')
        message = message.replace('"', '\\"')
        if message[:3] == "/w ":
            end = message.index(" ", 3)
            username = message[3:end]
            message = message[end+1:]
            if eliteCheck == "Yes":
                message = elite(message)
            whisper(username, message)
            pass
        
        elif message[:7] == "/wspam ":
            username = message[7:]
            whisperspam(username)
        
        elif message[:8] == "/wspam2 ":
            username = message[8:]
            whisperspam2(username)
        
        elif message[:8] == "/ignore ":
            username = message[8:]
            pass
        
        elif message[:8] == "/follow ":
            username = message[8:]
            userid = requests.get(base + "user/" + username).json()
            userid = userid["user_id"]
            if userid is not None:
                payload = {"type" : "user", "follow_id" : userid}
                follow = requests.post(base + "follow?authToken=" + token, data = payload)

        elif message[:10] == "/unfollow ":
            username = message[10:]
            userid = requests.get(base+"user/"+username).json()
            userid = userid["user_id"]
            if userid is not None:
                payload = {"authToken" : token, "follow_id" : userid, "type" : "user"}
                unfollow = requests.delete(base + "follow", params = payload)

        else:
            if eliteCheck == "Yes":
                message = elite(message)
                print "checker"
            if encodeCheck == "Yes":
                try:
                    message.encode(encoding="ascii")
                except UnicodeDecodeError:
                    text.config(state=NORMAL)
                    text.insert(END, "Only Keyboard characters allowed for encoding!")
                    text.config(state=DISABLED)
                    text.yview(END)
                else:
                    if len(message) > 220:
                        text.config(state=NORMAL)
                        text.insert(END, "Message is too long!")
                        text.config(state=DISABLED)
                        text.yview(END)
                    else:
                        message = "TB"+user[0]+message
                        message = list(base64.b64encode(message))
                        shift = ord(user[0]) - len(user)
                        if shift % 2 == 0:
                            shift += 1
                        for i in range(shift):
                            first = message.pop(0)
                            message.append(first)
                        message = "".join(message)
            ws.send('5:::{"name":"message","args":[{"method":"chatMsg","params":{"channel":"'+channel+'","name":"'+user+'","nameColor":"'+usercolor+'","text":"'+message+'"}}]}')
        return
    
    def on_message(ws, message):
        global usercolor
        #text.update_idletasks()
        scrollClick()
        
        if message == "1::":
            ws.send('5:::{"name":"message","args":[{"method":"joinChannel","params":{"channel":"'+channel+'","name":"'+user+'","token":"'+token+'","isAdmin":true}}]}')
            text.config(state=NORMAL)
            text.insert(END, message+"\n")
            text.tag_config("blue", font=font2, foreground="blue")
            text.tag_add("blue", "end -2c linestart", "end -2c lineend")                
            sendmsg()
        elif message == "2::":
            ws.send("2::")
            text.config(state=NORMAL)
            text.insert(END, message+"\n")
            text.tag_config("blue", font=font2, foreground="blue")
            text.tag_add("blue", "end -2c linestart", "end -2c lineend")                
            userlist()
        else:
            message = message[4:]
            message1 = json.loads(message)
            message1 = message1["args"][0]
            message1 = json.loads(message1)
            if message1["method"] == "infoMsg":
                message = message1["params"]["text"]
                text.config(state=NORMAL)
                text.insert(END, message+"\n")
                pass
            elif message1["method"] == "directMsg":
                message1 = message1["params"]
                username = message1["from"]
                usercolor = message1["nameColor"]
                message = message1["text"]
                message = "Whisper from: " + username + " " + message
                text.config(state=NORMAL)
                text.insert(END, message+"\n")
                pass
            elif message1["method"] == "slowMsg":
                message = message1["params"]["text"]
                text.config(state=NORMAL)
                text.insert(END, message+"\n")
                pass
            elif message1["method"] == "serverMsg":
                pass
            elif message1["method"] == "loginMsg":
                message = "Successfully logged in!"
                text.config(state=NORMAL)
                text.insert(END, message+"\n")
                userlist()
                pass
            elif message1["method"] == "motdMsg":
                message = message1["params"]["text"]
                text.config(state=NORMAL)
                text.insert(END, message+"\n")
                userlist()
                pass            
            elif message1["method"] == "pollMsg":
                pass
            elif message1["method"] == "raffleMsg":
                pass
            elif message1["method"] == "userList":
                message1 = message1["params"]["data"]
                adminList = message1["admin"]
                staffList = message1["isStaff"]
                communityList = message1["isCommunity"]
                modList = message1["user"]
                subList = message1["isSubscriber"]
                userList = message1["anon"]                
                adminList.sort(key = lambda s: s.lower())
                staffList.sort(key = lambda s: s.lower())
                communityList.sort(key = lambda s: s.lower())
                modList.sort(key = lambda s: s.lower())
                userList.sort(key = lambda s: s.lower())
                text3.config(state=NORMAL)
                text3.delete("1.0", END)
                text3.insert(INSERT, "USER LIST\n\n")
                text3.tag_config("bold", foreground="red", justify=CENTER, underline=TRUE)
                text3.tag_add("bold", "1.0", "1.end")
                adminList = list(x for x in adminList if x not in staffList and x not in communityList and x not in modList)
                #print adminList
                for viewer in adminList:
                    text3.insert(END, "ADM")
                    text3.tag_config("special", font=font4, foreground="red")
                    text3.tag_add("special", "end -1c linestart", "end -1c lineend")
                    text3.insert(END, " "+viewer)
                    text3.tag_config("click", font=font2)
                    text3.tag_add("click", "end -1c linestart +4c", "end -1c lineend")
                    text3.tag_bind("click", "<Enter>", userEnter)
                    text3.tag_bind("click", "<Leave>", userLeave)
                    text3.tag_bind("click", "<Button-1>", userOptions)
                    text3.insert(END, "\n")          
                for viewer in staffList:
                    text3.insert(END, "STAFF")
                    text3.tag_config("special", font=font4, foreground="red")
                    text3.tag_add("special", "end -1c linestart", "end -1c lineend")
                    text3.insert(END, " "+viewer)
                    text3.tag_config("click", font=font2)
                    text3.tag_add("click", "end -1c linestart +6c", "end -1c lineend")
                    text3.tag_bind("click", "<Enter>", userEnter)
                    text3.tag_bind("click", "<Leave>", userLeave)
                    text3.tag_bind("click", "<Button-1>", userOptions)
                    text3.insert(END, "\n")
                for viewer in communityList:
                    text3.insert(END, "AMB")
                    text3.tag_config("special", font=font4, foreground="red")
                    text3.tag_add("special", "end -1c linestart", "end -1c lineend")
                    text3.insert(END, " "+viewer)
                    text3.tag_config("click", font=font2)
                    text3.tag_add("click", "end -1c linestart +4c", "end -1c lineend")
                    text3.tag_bind("click", "<Enter>", userEnter)
                    text3.tag_bind("click", "<Leave>", userLeave)
                    text3.tag_bind("click", "<Button-1>", userOptions)
                    text3.insert(END, "\n")
                for viewer in modList:
                    text3.insert(END, "MOD")
                    text3.tag_config("special", font=font4, foreground="red")
                    text3.tag_add("special", "end -1c linestart", "end -1c lineend")
                    text3.insert(END, " "+viewer)
                    text3.tag_config("click", font=font2)
                    text3.tag_add("click", "end -1c linestart +4c", "end -1c lineend")
                    text3.tag_bind("click", "<Enter>", userEnter)
                    text3.tag_bind("click", "<Leave>", userLeave)
                    text3.tag_bind("click", "<Button-1>", userOptions)
                    text3.insert(END, "\n") 
                for viewer in userList:
                    if viewer in subList:
                        text3.insert(END, "SUB")
                        text3.tag_config("special", font=font4, foreground="red")
                        text3.tag_add("special", "end -1c linestart", "end -1c lineend")
                        text3.insert(END, " "+viewer)
                        text3.tag_config("click", font=font2)
                        text3.tag_add("click", "end -1c linestart +4c", "end -1c lineend")
                        text3.tag_bind("click", "<Enter>", userEnter)
                        text3.tag_bind("click", "<Leave>", userLeave)
                        text3.tag_bind("click", "<Button-1>", userOptions)
                        text3.insert(END, "\n")
                    else:
                        text3.insert(END, viewer)
                        text3.tag_add("click", "end -1c linestart", "end -1c lineend")
                        text3.tag_bind("click", "<Enter>", userEnter)
                        text3.tag_bind("click", "<Leave>", userLeave)
                        text3.tag_bind("click", "<Button-1>", userOptions)
                        text3.insert(END, "\n")
                text3.config(state=DISABLED)
                text3.yview("0")
                message = "User list received"
                text.config(state=NORMAL)
                text.insert(END, message+"\n")
                pass
            elif message1["method"] == "banList":
                message = "Banned users list received"
                text.config(state=NORMAL)
                text.insert(END, message+"\n")
                pass
            elif message1["method"] == "chatMsg":
                message1 = message1["params"]
                username = message1["name"]
                usercolor = message1["nameColor"]
                time = message1["time"]
                role = message1["role"]
                admCheck = message1["isOwner"]
                staffCheck = message1["isStaff"]
                ambCheck = message1["isCommunity"]
                subCheck = message1["isSubscriber"]
                #print usercolor
                message = message1["text"]
                message2 = list(message)
                shift = ord(username[0]) - len(username)
                if shift % 2 == 0:
                    shift += 1
                for i in range(shift):
                    last = message2.pop()
                    message2 = [last]+message2
                try:
                    base64.b64decode("".join(message2))
                except TypeError:
                    print "non-ascii"
                    pass
                else:
                    message2 = base64.b64decode("".join(message2))
                if message2[:3] == "TB"+username[0]:
                    message = message2[3:]
                message = message.replace("&lt;", "<")
                message = message.replace("&gt;", ">")
                message = message.replace("&amp;", "&")
                #message = username + " " + str(time) + " " + message
                if role == "admin" and admCheck is True:
                    #print "admin"
                    pass
                elif role == "admin" and admCheck is False and staffCheck is False and ambCheck is False:
                    #print "editor"
                    pass
                elif staffCheck is True:
                    #print "staff"
                    pass
                elif ambCheck is True:
                    #print "ambassador"
                    pass
                elif role == "user":
                    #print "moderator"
                    pass
                elif subCheck is True:
                    #print "subscriber"
                    pass
                else:
                    #print subCheck
                    #print type(subCheck)
                    pass
                text.config(state=NORMAL)
                text.insert(END, username)
                text.tag_config(usercolor, font=font2, foreground="#"+usercolor)
                text.tag_add(usercolor, "end -1c linestart", "end -1c lineend")
                text.tag_bind(usercolor, "<Enter>", userEnter)
                text.tag_bind(usercolor, "<Leave>", userLeave)
                text.tag_bind(usercolor, "<Button-1>", userOptions2)
                #text.tag_delete("color")
                usernameLen = str(len(username))
                text.insert(END, ": "+str(time)+" "+message+"\n")
                text.tag_config("black", font=font2, foreground="black")
                text.tag_add("black", "end -2c linestart +"+usernameLen+"c", "end -2c lineend")
                pass
            else:   
                text.config(state=NORMAL)
                text.insert(END, message+"\n")
                text.tag_config("red", font=font2, foreground="blue")
                text.tag_add("red", "end -2c linestart", "end -2c lineend")                      

            text.config(state=DISABLED)
            
        return

    def on_error(ws, error):
        text.config(state=NORMAL)
        text.insert(END, error)
        text.config(state=DISABLED)
        text.yview(END)
        #print error
        return
    
    def on_close(ws):
        text.config(state=NORMAL)
        text.insert(END, "Connection closed!")
        text.config(state=DISABLED)
        text.yview(END)
        ws.close()
        closing()
        #print "### closed ###"
        return

    def on_open(ws):
        text.config(state=NORMAL)
        text.insert(END, "Connecting...\n")
        text.config(state=DISABLED)
        return
    
    #Add widgets
    filemenu = Menu(master, tearoff=0)
    filemenu.add_command(label="Refresh User List", command=userlist)
    filemenu.add_command(label="Banned Users List", command=donothing)
    filemenu.add_command(label="Blacklisted Words List", command=donothing)
    filemenu.add_command(label="Exit", command=master.quit)
    master.config(menu=filemenu)
    
    entry = Entry(master, width=60)
    entry.pack()
    button = Button(master, text="Send", padx=5, relief=GROOVE)
    button.pack()
    frame1 = Frame(master)
    frame1.place(x=0,y=minheight-(entry.winfo_reqheight()*3),width=entry.winfo_reqwidth(),height=entry.winfo_reqheight()*2)
    frame2 = Frame(master)
    frame2.place(x=0,y=minheight-entry.winfo_reqheight(),width=minwidth/4*3,height=entry.winfo_reqheight())
    frame5 = Frame(master)
    frame5.place(x=entry.winfo_reqwidth(),y=minheight-(entry.winfo_reqheight()*3),width=button.winfo_reqwidth(),height=entry.winfo_reqheight()*2)
    frame6 = Frame(master)
    frame6.place(x=entry.winfo_reqwidth()+button.winfo_reqwidth(),y=minheight-(entry.winfo_reqheight()*3),width=minwidth/4*3-(entry.winfo_reqwidth()+button.winfo_reqwidth()),height=entry.winfo_reqheight())
    frame7 = Frame(master)
    frame7.place(x=entry.winfo_reqwidth()+button.winfo_reqwidth(),y=minheight-(entry.winfo_reqheight()*2),width=minwidth/4*3-(entry.winfo_reqwidth()+button.winfo_reqwidth()),height=entry.winfo_reqheight())

    #Buttons
    button2 = Button(frame2, text="Spam Chat", relief=GROOVE, command=spam)
    button2.pack(side=LEFT, expand=YES, fill=X)
    button3 = Button(frame2, text="Whisper All", relief=GROOVE, command=send)
    button3.pack(side=LEFT, expand=YES, fill=X)
    button4 = Button(frame2, text="Whisper All 2", relief=GROOVE, command=send)
    button4.pack(side=LEFT, expand=YES, fill=X)

    #Destroy entry, button and remake
    entry.destroy()
    button.destroy
    entry = Entry(frame1, width=60, fg="red")
    entry.pack(side=TOP)
    entry.bind("<Return>", sendmsg)
    xscrollbar = Scrollbar(frame1, orient=HORIZONTAL, command=entry.xview)
    xscrollbar.pack(side=TOP, fill=BOTH)
    entry["xscrollcommand"] = xscrollbar.set
    button = Button(frame5, text="Send", padx=5, relief=GROOVE, command=sendmsg)
    button.pack(expand=YES, fill=BOTH)
    colors = ["Hitbox", "Red", "Silver", "Black"]
    combo = ttk.Combobox(frame7, state="readonly", values=colors, width=6)
    combo.set("Hitbox")
    #print combo.get()
    combo.pack(side=LEFT, expand=YES)
    combo.bind("<Enter>", colorEnter)
    combo.bind("<Leave>", labelLeave)
    label = Label(frame6, text="User Color")
    label.pack(side=LEFT, expand=YES)
    label.bind("<Enter>", colorEnter)
    label.bind("<Leave>", labelLeave)
    options = ["Yes", "No"]
    combo2 = ttk.Combobox(frame7, state="readonly", values=options, width=3) 
    combo2.set("No")
    #print combo2.get()
    combo2.pack(side=LEFT, expand=YES)
    combo2.bind("<Enter>", eliteEnter)
    combo2.bind("<Leave>", labelLeave)
    label2 = Label(frame6, text="L337 5P34K")
    label2.pack(side=LEFT, expand=YES)
    label2.bind("<Enter>", eliteEnter)
    label2.bind("<Leave>", labelLeave)
    combo3 = ttk.Combobox(frame7, state="readonly", values=options, width=3) 
    combo3.set("No")
    #print combo3.get()
    combo3.pack(side=LEFT, expand=YES)
    combo3.bind("<Enter>", encodeEnter)
    combo3.bind("<Leave>", labelLeave)
    label3 = Label(frame6, text="Scramble")
    label3.pack(side=LEFT, expand=YES)
    label3.bind("<Enter>", encodeEnter)
    label3.bind("<Leave>", labelLeave)
    combo4 = ttk.Combobox(frame7, state="readonly", values=options, width=3) 
    combo4.set("No")
    #print combo4.get()
    combo4.pack(side=LEFT, expand=YES)
    combo4.bind("<Enter>", ignoreEnter)
    combo4.bind("<Leave>", labelLeave)
    label4 = Label(frame6, text="Ignore All")
    label4.pack(side=LEFT, expand=YES)
    label4.bind("<Enter>", ignoreEnter)
    label4.bind("<Leave>", labelLeave)

    frame = Frame(master)
    frame.place(x=0,y=0,width=minwidth/4*3,height=minheight-(entry.winfo_reqheight()*3))
    yscrollbar = Scrollbar(frame)
    yscrollbar.pack()
    text = Text(frame, font=font4, wrap=WORD, foreground="red")
    text.place(x=0,y=0,width=minwidth/4*3-yscrollbar.winfo_reqwidth(),height=minheight-(entry.winfo_reqheight()*3))
    yscrollbar.destroy()
    yscrollbar = Scrollbar(frame, orient=VERTICAL, command=text.yview)
    yscrollbar.pack(side=RIGHT, fill=Y)
    yscrollbar.bind("<ButtonRelease-1>", scrollClickSet)
    text["yscrollcommand"] = yscrollbar.set

    frame3 = Frame(master)
    frame3.place(x=minwidth/4*3,y=0,width=minwidth/4,height=minheight/2)
    yscrollbar2 = Scrollbar(frame3)
    yscrollbar2.pack()
    text2 = Text(master, font=font, wrap=WORD)
    text2.place(x=minwidth/4*3,y=0,width=minwidth/4-yscrollbar2.winfo_reqwidth(),height=minheight/2)
    yscrollbar2.destroy()
    yscrollbar2 = Scrollbar(frame3, orient=VERTICAL, command=text2.yview)
    yscrollbar2.pack(side=RIGHT, fill=Y)
    text2["yscrollcommand"] = yscrollbar2.set

    frame4 = Frame(master)
    frame4.place(x=minwidth/4*3,y=minheight/2,width=minwidth/4,height=minheight/2)
    yscrollbar3 = Scrollbar(frame4)
    yscrollbar3.pack()
    text3 = Text(master, font=font, wrap=WORD)
    text3.place(x=minwidth/4*3,y=minheight/2,width=minwidth/4-yscrollbar3.winfo_reqwidth(),height=minheight/2)
    yscrollbar3.destroy()
    yscrollbar3 = Scrollbar(frame4, orient=VERTICAL, command=text3.yview)
    yscrollbar3.pack(side=RIGHT, fill=Y)
    text3["yscrollcommand"] = yscrollbar3.set

    #Chat Commands
    text2.config(state=NORMAL)
    text2.insert(END, "CHAT COMMANDS\n\n")
    text2.tag_config("bold", foreground="red", justify=CENTER, underline=TRUE)
    text2.tag_add("bold", "1.0", "1.13")
    text2.insert(END, "/w user message ")
    text2.tag_config("bold2", foreground="red", font=font2)
    text2.tag_add("bold2", "3.0", "3.15")
    text2.insert(END, "Whisper a message to the specified user.\n\n")
    text2.tag_config("bold3", font=font3)
    text2.tag_add("bold3", "3.15", "3.56")
    text2.insert(END, "/wspam user ")
    text2.tag_add("bold2", "5.0", "5.12")
    text2.insert(END, "Whisper random symbols to the specified user at a rate of 8 whisper messages / second. Throttles chat.\n\n")
    text2.tag_add("bold3", "5.12", "5.114")
    text2.insert(END, "/wspam2 user ")
    text2.tag_add("bold2", "7.0", "7.13")
    text2.insert(END, "Whisper random symbols to the specified user at a rate of 8 whisper messages / second. Use if banned.\n\n")
    text2.tag_add("bold3", "7.13", "7.114")
    text2.insert(END, "/ignore user ")
    text2.tag_add("bold2", "9.0", "9.13")
    text2.insert(END, "Ignore the specified user's messages from appearing in chat. Whisper messages will still be shown. Typing /ignore user will unignore the user if already ignored.\n\n")
    text2.tag_add("bold3", "9.13", "9.174")
    text2.insert(END, "/follow user ")
    text2.tag_add("bold2", "11.0", "11.13")
    text2.insert(END, "Follow the specified user.\n\n")
    text2.tag_add("bold3", "11.13", "11.39")
    text2.insert(END, "/unfollow user ")
    text2.tag_add("bold2", "13.0", "13.15")
    text2.insert(END, "Unfollow the specified user.\n\n")
    text2.tag_add("bold3", "13.15", "13.43")

    text2.config(state=DISABLED)
    text2.yview("0")

    text3.config(state=DISABLED)
    
    def client():
        global base
        serverList = requests.get(base + "chat/servers?redis=true")
        response = serverList.json()
        serverIP = response[0]["server_ip"]
        server = requests.get("http://" + serverIP + "/socket.io/1/")
        ID = server.text
        ID = ID.split(":")
        ID = ID[0]
        websocket = "ws://" + serverIP + "/socket.io/1/websocket/" + ID

        def connection():
            global ws
            #enableTrace(True)
            ws = WebSocketApp(websocket, on_message = on_message, on_error = on_error, on_close = on_close)
            ws.on_open = on_open
            ws.run_forever()
            return

        t = Thread(target=connection)
        t.start()

        return
    
    client()
    
    return

master.mainloop()

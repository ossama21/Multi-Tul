##################### the 3 problem line 184 (weather not working) ####################################
########### the 4 problem line311/314 (find a way to turn the app to dark mode and creat a X/O game)###
############# la preumier itulisation durer de pc #################


from tkinter import *
from tkinter import ttk
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter import filedialog
import platform
import psutil
import wmi
# brightness
import screen_brightness_control as pct

# audio
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import win32api
import pythoncom
import pywintypes
import win32com.client
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

# weater
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

# clock
from time import strftime

# calendar
from tkcalendar import *

# open google
import pyautogui

import subprocess
import webbrowser as wb
import random
import time

root = Tk()
root.title('mac-soft TooL')
root.geometry("850x500+300+170")
root.resizable(False, False)
root.configure(bg='#292e2e')

# icon
image_icon = PhotoImage(file="Image/icon.png")
root.iconphoto(False, image_icon)

Body = Frame(root, width=900, height=600, bg="#d6d6d6")
Body.pack(pady=20, padx=20)

# --------------------------------------------------------------------
LHS = Frame(Body, width=310, height=435, bg="#f4f5f5", highlightbackground='#adacb1', highlightthickness=1)
LHS.place(x=10, y=10)

# Logo
photo = PhotoImage(file="Image/laptop.png")
myimage = Label(LHS, image=photo, background="#f4f5f5")
myimage.place(x=2, y=20)

# Get system information using WMI
c = wmi.WMI()
my_system = c.Win32_ComputerSystem()[0]
os = c.Win32_OperatingSystem()[0]
processor = c.Win32_Processor()[0]
gpu = c.Win32_VideoController()[0]

l1 = Label(LHS, text=my_system.Name, bg="#f4f5f5", font=("Acumin Variable Concept", 15, "bold"), justify="center")
l1.place(x=20, y=200)

l2 = Label(LHS, text=f"Version:{os.Caption} {os.Version}", bg='#f4f5f5', font=("Acumin Variable Concept", 8),
           justify="center")
l2.place(x=20, y=230)

l3 = Label(LHS, text=f"RAM Installed:{round(int(my_system.TotalPhysicalMemory) / (1024 ** 3), 2)} GB", bg='#f4f5f5',
           font=("Acumin Variable Concept", 15), justify="center")
l3.place(x=20, y=250)

l4 = Label(LHS, text=f"Processor:{processor.Name}", bg='#f4f5f5', font=("Acumin Variable Concept", 9),
           justify="center")
l4.place(x=9, y=295)

l5 = Label(LHS, text=f"GPU:{gpu.Name}", bg='#f4f5f5',
           font=("acumin Variabel Concept", 9), justify="center")
l5.place(x=9, y=340)

# ---------------------------------------------------------------------
RHS = Frame(Body, width=470, height=235, bg="#f4f5f5", highlightbackground='#adacb1', highlightthickness=1)
RHS.place(x=330, y=10)

system = Label(RHS, text='System', font=("Acumin Variabele Concept", 15), bg='#f4f5f5')
system.place(x=10, y=10)


########################### BATTERY ####################################
def convertTime(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)


def none():
    global battery_png
    global battery_label
    battery = psutil.sensors_battery()
    percent = battery.percent
    time = convertTime(battery.secsleft)

    lbl['text'] = f"{percent}%"
    lbl_plug.config(text=f'Plug in:{str(battery.power_plugged)}')
    lbl_time.config(text=f'{time}remaining')

    battery_label = Label(RHS, background="#f4f5f5")
    battery_label.place(x=15, y=50)

    lbl.after(1000, none)

    if battery.power_plugged:
        battery_png = PhotoImage(file="Image/charging.png")
        battery_label.config(image=battery_png)

    else:
        battery_png = PhotoImage(file='Image/battery.png')
        battery_label.config(image=battery_png)


lbl = Label(RHS, font=("Acumen Variable Concept", 40, 'bold'), bg='#f4f5f5')
lbl.place(x=200, y=40)

lbl_plug = Label(RHS, font=("Acumen Variable Concept", 10, 'bold'), bg='#f4f5f5')
lbl_plug.place(x=20, y=100)

lbl_time = Label(RHS, font=("Acumen Variable Concept", 15, 'bold'), bg='#f4f5f5')
lbl_time.place(x=200, y=110)

none()

#################################################################################

############################ SPEAKER ############################################

volume_value = tk.DoubleVar()
lbl_speaker = Label(RHS, text="Speaker:{}%".format(int(volume_value.get())), font=('arial', 10, 'bold'), bg="#f4f5f5")
lbl_speaker.place(x=10, y=150)


def get_current_volume_value():
    return '{: .2f}'.format(volume_value.get())


def volume_changed(value):
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            volume.SetMasterVolume(float(value) / 100, None)
        lbl_speaker.config(text="Speaker:{}%".format(int(float(value))))
    except Exception as e:
        print(f"Error setting volume: {e}")


style = ttk.Style()
style.configure("TScale", background='#f4f5f5')

volume = ttk.Scale(RHS, from_=0, to=100, orient='horizontal', command=volume_changed, variable=volume_value)
volume.place(x=120, y=150)
volume.set(50)
################################################################################
################################BRIGHTNESS######################################
lbl_brightness = Label(RHS, text='Brightness: ', font=('arial', 10, 'bold'), bg="#f4f5f5")
lbl_brightness.place(x=10, y=190)
current_value = tk.DoubleVar()


def get_current_value():
    return '{: .2f}'.format(current_value.get())


def brightness_changed(event):
    pct.set_brightness(get_current_value())


brightness = ttk.Scale(RHS, from_=0, to=100, orient='horizontal',
                       command=brightness_changed, variable=current_value)
brightness.place(x=105, y=190)


########################################################################

def weather():
    root.iconify()
    app1 = Toplevel()
    app1.geometry('850x500+300+170')
    app1.title('Weather')
    app1.configure(bg="#f4f5f5")
    app1.resizable(False, False)

    # icon
    image_icon = PhotoImage(file='Image/App1.png')
    app1.iconphoto(False, image_icon)

    def getweather():
        try:
            city = textfield.get()
            if not city:
                messagebox.showerror("Weather App", 'Please enter a city')
                return
            geolocator = Nominatim(user_agent="geopiExercises")
            lacation = geolocator.geocode(city)
            obj = TimezoneFinder()
            result = obj.timezone_at(lng=lacation.longitude, lat=lacation.latitude)

            home = pytz.timezone(result)
            local_time = datetime.now(home)
            current_time = local_time.strftime('%I:%M:%P')
            clock.config(text=current_time)
            name.config(text="CURRENT WEATHER")

            # weather(not working cause not paid)
            api = "https://api.openweathermap.org/data/3.0/onecall?q=" + city + "&appid=20d7008629a045a1b4571129230804"

        except Exception as e:
            messagebox.showerror("Weather App", 'Invalid Entry')

    # search_box
    Search_image = PhotoImage(file="Image/search.png")
    myimage = Label(app1, image=Search_image, bg='#f4f5f5')
    myimage.place(x=20, y=20)

    textfield = tk.Entry(app1, justify='center', width=17, font=('poppins', 25, 'bold'), bg='#404040', border=0,fg='white')
    textfield.place(x=50, y=40)
    textfield.focus()

    # bind <Return> event to search_box
    textfield.bind('<Return>', lambda event: getweather())

    Search_icon = PhotoImage(file='Image/search_icon.png')
    myimage_icon = Button(app1, image=Search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getweather)
    myimage_icon.place(x=400, y=34)

    # LOGO
    logo_image = PhotoImage(file="Image/logo.png")
    logo = Label(app1, image=logo_image, bg="#f4f5f5")
    logo.place(x=150, y=100)

    # Botton Box
    frame_image = PhotoImage(file="Image/box.png")
    frame_myimage = Label(app1, image=frame_image, bg='#f4f5f5')
    frame_myimage.pack(padx=5, pady=5, side=BOTTOM)

    # time
    name = Label(app1, font=('arial', 15, 'bold'), bg='#f4f5f5')
    name.place(x=30, y=130)
    clock = Label(app1, font=('Helvetica', 20), bg='#f4f5f5')
    clock.place(x=30, y=130)

    # Label
    label1 = Label(app1, text="WIND", font=("Helvatica", 15, 'bold'), fg="white", bg='#1ab5ef')
    label1.place(x=120, y=400)

    label2 = Label(app1, text="HUMIDITY", font=("Helvatica", 15, 'bold'), fg="white", bg='#1ab5ef')
    label2.place(x=250, y=400)

    label3 = Label(app1, text="DESCRIPTION", font=("Helvatica", 15, 'bold'), fg="white", bg='#1ab5ef')
    label3.place(x=430, y=400)

    label4 = Label(app1, text="PRESSURE", font=("Helvatica", 15, 'bold'), fg="white", bg='#1ab5ef')
    label4.place(x=650, y=400)

    t = Label(app1, font=('arial', 70, 'bold'), fg='#ee666d', bg='#f4f5f5')
    t.place(x=400, y=150)

    c = Label(app1, font=('arial', 70, 'bold'), bg='#f4f5f5')
    c.place(x=400, y=250)

    w = Label(app1, text="...", font=('arial', 20, 'bold'), bg="#1ab5ef")
    w.place(x=120, y=430)
    h = Label(app1, text="...", font=('arial', 20, 'bold'), bg="#1ab5ef")
    h.place(x=280, y=430)
    d = Label(app1, text="...", font=('arial', 20, 'bold'), bg="#1ab5ef")
    d.place(x=450, y=430)
    p = Label(app1, text="...", font=('arial', 20, 'bold'), bg="#1ab5ef")
    p.place(x=670, y=430)

    app1.mainloop()


def clock():
    app2 = Toplevel()
    app2.geometry("850x110+300+10")
    app2.title('Clock')
    app2.configure(bg="#292e2e")
    app2.resizable(False, False)
    # icon
    image_icon = PhotoImage(file="Image/App2.png")
    app2.iconphoto(False, image_icon)

    def clock():
        text = strftime('%H:%M:%S %p')
        lbl.config(text=text)
        lbl.after(1000, clock)

    lbl = Label(app2, font=('digital-7', 50, 'bold'), width=20, bg="#f4f5f5", fg="#292e2e")
    lbl.pack(anchor='center', pady=20)
    clock()

    app2.mainloop()


def calendar():
    app3 = Toplevel()
    app3.geometry("300x300+-10+10")
    app3.title('Calendar')
    app3.configure(bg="#292e2e")
    app3.resizable(False, False)

    # icon
    image_icon = PhotoImage(file="Image/App3.png")
    app3.iconphoto(False, image_icon)
    mycal = Calendar(app3, setmode='day', date_pattern='d/m/yy')
    mycal.pack(padx=15, pady=35)
    app3.mainloop()


def Dark_mode():
    pass


def Game():
    pass


def screenshot():
    root.iconify()
    myScreenshot = pyautogui.screenshot()
    file_path = filedialog.asksaveasfilename(defaultextension='.png')
    myScreenshot.save(file_path)


def file():
    subprocess.Popen(r'explorer /select, "C:\path\of\folder\file"')


def google():
    wb.register('chrome', None)
    wb.open('https://www.google.com/')


def youtube():
    wb.register('chrome', None)
    wb.open('https://www.youtube.com')


def close_window():
    root.destroy()


# ----------------------------------------------------------------------
RHB = Frame(Body, width=470, height=190, bg="#f4f5f5", highlightbackground='#adacb1', highlightthickness=1)
RHB.place(x=330, y=255)

apps = Label(RHB, text='Apps', font=('Acumen Variable Concept', 15), bg='#f4f5f5')
apps.place(x=10, y=10)

app1_image = PhotoImage(file="Image\App1.png")
app1 = Button(RHB, image=app1_image, bd=0, command=weather)
app1.place(x=15, y=50)

app2_image = PhotoImage(file="Image\App2.png")
app2 = Button(RHB, image=app2_image, bd=0, command=clock)
app2.place(x=100, y=50)

app3_image = PhotoImage(file="Image\App3.png")
app3 = Button(RHB, image=app3_image, bd=0, command=calendar)
app3.place(x=185, y=50)

app4_image = PhotoImage(file="Image\App4.png")
app4 = Button(RHB, image=app4_image, bd=0, command=Dark_mode)
app4.place(x=270, y=50)

app5_image = PhotoImage(file="Image\App5.png")
app5 = Button(RHB, image=app5_image, bd=0)
app5.place(x=355, y=50)

app6_image = PhotoImage(file="Image\App6.png")
app6 = Button(RHB, image=app6_image, bd=0, command=screenshot)
app6.place(x=15, y=120)

app7_image = PhotoImage(file="Image\App7.png")
app7 = Button(RHB, image=app7_image, bd=0, command=file)
app7.place(x=100, y=120)

app8_image = PhotoImage(file="Image\App8.png")
app8 = Button(RHB, image=app8_image, bd=0, command=google)
app8.place(x=185, y=120)

app9_image = PhotoImage(file="Image\App9.png")
app9 = Button(RHB, image=app9_image, bd=0, command=youtube)
app9.place(x=270, y=120)

app10_image = PhotoImage(file="Image\App10.png")
app10 = Button(RHB, image=app10_image, bd=0, command=close_window)
app10.place(x=355, y=120)

root.mainloop()

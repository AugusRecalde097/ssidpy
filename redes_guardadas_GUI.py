from tkinter import *
from tkinter import ttk
import subprocess
import re
import qrcode
import tkinter as tk 

# Función para generar un código qr
def generate_qr_code(ssid, password, image=True):
    # Source: https://git.io/JtLIv
    text = f"WIFI:T:WPA;S:{ssid};P:{password};;"

    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10,
                       border=4)
    qr.add_data(text)

    if image:
        file_name = ssid.replace(" ", "_") + ".png"
        img = qr.make_image()
        img.save("./redes_guardadas/"+file_name)
        img.show("./redes_guardadas/"+file_name)
        print(f"QR code has been saved to {file_name}")
    else:
        qr.make()
        qr.print_tty()
# =================================================================
def Buscarred_label(name):
    profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profiles", name,"key=clear"], capture_output = True).stdout.decode('latin-1')
    error =  re.findall('No se encuentra el perfil', profile_info_pass)
    
    if(len(error) > 0):
        red_label['text'] = 'Error: No se encuentra el perfil'
        red_label['fg'] = "white"
        red_label['bg'] = "red_label"

    else:
        password = re.findall("Contenido de la clave  : (.*)\r", profile_info_pass)
        cifrado = re.findall("Autenticaci¢n                  : (.*)\r", profile_info_pass)

        pass_label['text'] = "Contraseña: "+password[0]
        pass_label['fg'] = "white"
        pass_label['bg'] = "#5fb878"
        
        red_label['text'] = "SSID: "+name
        red_label['fg'] = "white"
        red_label['bg'] = "#5fb878"
        print(cifrado)
        cifrado_label['text'] = "Cifrado: "+cifrado[0]
        cifrado_label['fg'] = "white"
        cifrado_label['bg'] = "#5fb878"

        generate_qr_code(name, password[0])
        

def mostrar_perfiles():
    profiles_info = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode('latin-1')
    lista_perfiles = re.findall("Perfil de todos los usuarios     : (.*)\r", profiles_info)

    namesArray = []
    i=0
    for perfil in lista_perfiles:
        namesArray.append(perfil)
        i+=1 
    # get first 3 letters of every month name
    profiles_combo['values'] = namesArray
    # prevent typing a value
    profiles_combo['state'] = 'readonly'
    # place the widget
    profiles_combo.pack(fill=tk.X, padx=5, pady=5)
    profiles_combo.bind('<<ComboboxSelected>>', mostrar_text)
    profiles_combo.place(x=10,y=30,width=280,height=30)

def mostrar_text(self):
    name = selected_profile.get()
    Buscarred_label(name)

# ====================================== #
#         Configuraciones generales      #
# ====================================== #
window = Tk()
window.geometry("300x250")
# Titulo
etiqueta = Label(window, text="Lista de red_labeles guardadas")
etiqueta.pack(side=TOP)
selected_profile= tk.StringVar()

canvas = Canvas(window, bg="yellow",
		height=250, width=300)
canvas.pack()


# LISTA DE red_labelES.
profiles_combo = ttk.Combobox(window, textvariable=selected_profile)
 # NOMBRE DE LA red_label.
red_label = Label(window)
red_label.pack()
red_label.place(x=30,y=100,width=240,height=30)
# CONTRASEÑA DE LA red_label. 
pass_label = Label(window)
pass_label.pack()
pass_label.place(x=30,y=150,width=240,height=30)

cifrado_label = Label(window)
cifrado_label.pack()
cifrado_label.place(x=30, y=200, width=240,height=30)

mostrar_perfiles()

window.mainloop()

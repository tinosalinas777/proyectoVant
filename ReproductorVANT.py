import tkinter as tk 
from tkinter import *
from tkinter import messagebox
from urllib import request
import cv2
import imutils
from PIL import Image, ImageTk
import requests


ventana=Tk()                     #aca creamos la ventana
ventana.geometry("900x500")      #le damos un tamaño a la ventana
ventana.title("Testing ")        #ponemos un titulo a la ventana
ventana.config(bg="gray14")      #color de fondo de la ventana
ventana.resizable(False,False)   #esta opcion hace que no se pueda cambiar el tamaño de la ventana
foto=PhotoImage(file="dron.png") #imagen del icono dentro de la ventana
ventana.iconphoto(False,foto)    #carga el icono en la ventana
fondo=tk.PhotoImage(file="1.png") #carga imagen en el reproductor para no ver un fondo negro
etiq_de_video=Label(ventana, image=fondo) #nombre aplicado al reproductor
etiq_de_video.place(x=170, y=50, relwidth = 0.8, relheight = 0.8)#ubicacion del reproductor de video


try:
    request= requests.get("https://google.com",timeout=5)# esto hace ping a google y si no hay respuesta sale un cartel "sin internet"
    def visualizar():
        global cap
        ret, frame= cap.read()
        if ret==True:
            frame=imutils.resize(frame, width=730, height=730)#tamaño del reproductor
            frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            im=Image.fromarray(frame)
            img=ImageTk.PhotoImage(image=im)

            etiq_de_video.configure(image=img)
            etiq_de_video.image=img
            etiq_de_video.after(10, visualizar)
        else:
            etiq_de_video.image=""
            cap.release()
    
except(requests.ConnectionError, requests.Timeout):
    messagebox.showinfo("Error","Sin conexion a Internet")#si no hay internet muestra este mensaje
    


    
def iniciar():  # esta funcion inicia la captura de video recepcionado por el servidor
    try:
        if(btnIniciar['state']== tk.NORMAL):
            btnIniciar['state']= tk.DISABLED
            button2['state']= tk.NORMAL
        else:
            btnIniciar['state'] = tk.NORMAL
            
        request= requests.get("https://google.com",timeout=5)#nuevamente verifica connecion a internet
        
        global cap
        cap=cv2.VideoCapture("rtmp://192.168.0.23/live/stream")#direccion de server rtsp o rtmp
        visualizar()
        
    except(requests.ConnectionError, requests.Timeout):
        messagebox.showinfo("Error","Sin conexion a Internet")

def control():
    global cap
    cap = cv2.imread("stopp.jpg")
    
    if(btnIniciar['state']== tk.DISABLED):
        btnIniciar['state']= tk.NORMAL
        button2['state']= tk.DISABLED
    else:
        btnIniciar['state'] = tk.DISABLED
        
    
    
#el siguiente codigo es para localizar losbotones y los titulos del programa
etiqueta4=Label(ventana,text="Testing VANT 4g",bg="gray14",fg="white",font="none 20 bold")#titulo del programa superior
etiqueta4.place(x=400,y=10)


btnIniciar=Button(ventana,text="Iniciar Test",command=iniciar, bg="green",font="none 12 bold",width=12,height=2,state=NORMAL)#este boton llama a la funcion iniciar
btnIniciar.place(x=10, y=70)

button2 = tk.Button(ventana, text="Parar", command = control,bg="green",font="none 12 bold",width=12,height=2,state=DISABLED)#este boton inicia la funcion control
button2.place(x=10,y=150)


etiqueta5=Label(ventana,text="V1 testing ",bg="gray14",fg="yellow",font="none 8 bold")#titulo del programa
etiqueta5.place(x=400,y=460)


ventana.mainloop()

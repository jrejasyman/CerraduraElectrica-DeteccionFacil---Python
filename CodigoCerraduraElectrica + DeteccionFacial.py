#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Importamos la extension de numpy y los paquetes de python
import numpy as np
import cv2

#Importamos la biblioteca de imagenes de python
from PIL import Image
import serial, time

#cargamos la plantilla e inicializamos la webcam:
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap = cv2.VideoCapture(0)

#iniciamos la comunicacion con el arduino el puerto 3 y el tiempo
arduino = serial.Serial("COM3", 9600)
time.sleep(2)


while(True):
    #leemos un frame y lo guardamos 
    ret, img = cap.read()
 
    #convertimos la imagen a blanco y negro
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
    #buscamos las coordenadas de los rostros (si los hay) y
    #guardamos su posicion
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
 
    #Dibujamos un rectangulo en las coordenadas de cada rostro
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(125,255,0),2)

    #Mostramos la imagen
    cv2.imshow('img',img)
    
    #Guarda la foto tomada en el directorio
    cv2.imwrite("foto.png", img)
    
    
    #Comparamos las fotos 
    i1 = Image.open("foto.png")
    i2 = Image.open("foto2.png")
    assert i1.mode == i2.mode, "Diferentes tipos de imágenes."
    assert i1.size == i2.size, "Diferentes tamaños."
 
    pairs = zip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
 
    #La diferencia del porcentaje para que pueda abrir la puerta o cerrar
    ncomponents = i1.size[0] * i1.size[1] * 3
    diferencia = (dif / 255.0 * 100) / ncomponents
    print ("Porcentaje de diferencia", diferencia)
    
   
    if diferencia <= 15:
        arduino.write(b'1')
        print("Abrir puerta")
    else:
        arduino.write(b'0')
        print("Mantener la puerta cerrada")
     
    #con la tecla 'q' salimos del programa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2-destroyAllWindows()


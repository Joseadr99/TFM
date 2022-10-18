#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 12:37:47 2022

@author: joseadr
"""

import os
from tqdm import tqdm

def parse_pascal(ruta,nombre_imagen):
    boxes = []    
    with open('%s' % ruta) as fichero:
       linea = fichero.readline() 
       contador = 1
       persona = 0
       while linea:
          if contador==3:
             tamaño = linea.split(': ')[1]
             ancho = int(tamaño.split(" x ")[0])
             largo = int(tamaño.split(" x ")[1])
             
          elif contador == 11:
             clases = linea.split('"')[1]
             print(clases)
             if clases == "PASpersonWalking":
                 clase = 0
             else:
                 clase = 1
             bb = linea.split(': ')[1]
             mini = bb.split(" - ")[0]
             maxi = bb.split(" - ")[1]
             mini2 = mini.split("(")[1]
             maxi2 = maxi.split("(")[1]
             
             xmin = int(mini2.split(",")[0])
             ymin = int(mini2.split(",")[1].split(")")[0])

             xmax = int(maxi2.split(",")[0])
             ymax = int(maxi2.split(",")[1].split(")")[0])
             persona +=1
             dw = 1./ancho
             dh = 1./largo
             x = (xmin + xmax)/2.0 - 1
             y = (ymin + ymax)/2.0 - 1
             w = xmax - xmin
             h = ymax - ymin
             x = x*dw
             w = w*dw
             y = y*dh
             h = h*dh
             boundingbox = [clase, x,y,w,h]
             boxes.append(boundingbox)
             
          elif contador == 13: # Si es que cuenta la línea vacia
             contador = 8
             
          linea = fichero.readline()          
          contador += 1
    #print("La imagen ",nombre_imagen," tiene ", persona, "personas, por lo tanto ",len(boxes), " boxes") 
    return boxes

def archivo_YOLO(ruta,boxes):
    with open('%s' % ruta,"w" ) as fichero:
        for box in boxes:
            fichero.write("%d %f %f %f %f\n" % (box[0],box[1],box[2],box[3],box[4]))
    print("ha finalizado fichero YOLO")
    
def parse_dataset(directorio):

    folderPath = os.path.join(directorio,'Annotation')
    
    for j in tqdm(os.listdir(folderPath)):
        ruta2 = directorio + "Annotation/"
        folderPath2 = os.path.join(ruta2,j) 
        boxes = parse_pascal(folderPath2,j)
        
        ruta3 = directorio + "Yolo/"
        folderPath3 = os.path.join(ruta3,j)
        archivo_YOLO(folderPath3, boxes)
        
        print("imagen", j ," pasada a yolo")


#archivo_YOLO("hola.txt", [[0,0.5,0.2,0.23,0.7],[0,0.7,0.3,0.7,0.6]])
#boxee = parse_pascal("./PennFudanPed/Annotation/FudanPed00001.txt", "FudanPed00001")
#print(boxee)
parse_dataset("./PennFudanPed/")

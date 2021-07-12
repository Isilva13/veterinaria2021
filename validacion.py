from flask import Flask, render_template, request, redirect, url_for, flash
import re

 #Se reciben los datos dato(lista de campos con datos), categora(lo utiliza Flash), tam(tamaño de los campos en la base),
 # grab(marca un 1 si se graba en la base o un 0 si no se debe grabar)
def validardatos(dato,categoria,tam,grab,oblig,tipo):
    #Se arma la lista con los posibles errores   
     mensaje=["El campo no puede estar vacio!","Cantidad de caracteres maximo superado!","Ingrese solamente letras","Ingrese solamente numeros","Ingrese un correo valido"] 
     #Se prepara la lista para identificar con un 1 si encontro error o con un 0 sino econtro, para luego determinar si graban los datos
     errores=[0]
     while True:           
         #Se recorre en paralelo la lista dato(a), categoria(b) y tam(c), para luego utilizar los datos de la lista si estan ok para guardar en la base,
         #la categoria para imprimir el mensaje en la etiqueta correcta del HTML y el tam para verificar que los datos no superen la definion de la base
         for a,b,c,d,e in zip(dato,categoria,tam,oblig,tipo):  
             #Se verifica si el campo obligatorio no se encuentra en blanco            
             if not a and d==1:   
                 print(mensaje[0])
                #Se imprime el mensaje correspondiente de la lista de mensajes definidas arriba
                 print(b)
                 flash(str(mensaje[0]), category=str(b))
                 #Se arma la lista de errores con 1 en caso que encuentre errores y luego en el for con un 1 es suficiente para no grabar en la base
                 errores.append(1)   
             #Se verifica si el largo del camp es igual al de la base
             elif len(a) > c:
                 print(mensaje[1]) 
                 print(b)
                 flash(str(mensaje[1]), category=str(b)) 
                 errores.append(1) 
             #Se verifica si el dato ingresado contiene unicamente letras
             elif not a.isalpha() and a!="" and e=="c":
                 print(mensaje[2]) 
                 print(b)
                 flash(str(mensaje[2]), category=str(b))                 
                 errores.append(1) 
             #Se verifica si el dato ingresado contiene unicamente letras
             elif not a.isdigit() and len(a)!=0 and e=="n":                 
                 print(mensaje[3]) 
                 print(b)
                 flash(str(mensaje[3]), category=str(b))
                 errores.append(1)  
             #Se verifica si el campo es del tipo email (definido en la lista de llamada)
             elif e=="e" and a!="": 
                 #En la variable compa, se arma el formato que se va a comparar con el email ingresado
                 compa = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$' 
                 #Si el formato es el adecuado no se generara e codigo de error en la lista errores
                 if re.search(compa,a)==None:
                     flash(str(mensaje[4]), category=str(b))
                     print("Correo invalido")
                     errores.append(1) 
             
        #Se cambia la variable a 1 para poder salir del bucle       
         break
     #Se recorre la lista de errores y en caso de encontrar un 1 se guarda en la variable grab para determinar si se guarda
     # o no los datos de entrada la base de datos
     for j in errores:
         if j==1:
             grab=0
         else:
             grab=1

     #flash(mensaje, category=categoria)        
     print(grab)     
     return grab 
    
 
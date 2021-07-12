from MySQLdb import DATETIME
from flask import Flask, render_template, request, redirect, url_for, flash, send_file,json, jsonify
from flask_mysqldb import MySQL
from datetime import datetime, date, timedelta
import os
from werkzeug.utils import secure_filename
import io
import pandas as pd
import shutil
from flask import make_response
from os import mkdir
from validacion import validardatos
import base64
import webbrowser
from PIL import Image
from distutils.dir_util import copy_tree



mascota = ""
numeromascota = ""
nsocio = ""
nmascota = ""
#Variable que indica ruta a guardar fotos de las mascotas que se suben al programa en esa ruta
UPLOAD_FOLDER = 'static/fotos'
#Variable que indica ruta a guardar de todo tipo de archivos que se adjuntan en a historia clinica de las mascotas
UPLOAD_FOLDER2 = 'static/Adjuntos'
#Define que tipos de extensiones de archivos permite subir al sistema
UPLOAD_FOLDER3 = 'static/fotos/productos'
UPLOAD_FOLDER10 = 'C:/xampp/htdocs/fotos'
UPLOAD_FOLDER11 = 'C:/xampp/fotos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', "pdf", "doc", "docx", "xls", "xlsx", "txt"}    

# initializations
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2
app.config['UPLOAD_FOLDER3'] = UPLOAD_FOLDER3
app.config['UPLOAD_FOLDER10'] = UPLOAD_FOLDER10
app.config['UPLOAD_FOLDER11'] = UPLOAD_FOLDER11
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'prueba'
app.config['MYSQL_PASSWORD'] = 'veterinaria'
app.config['MYSQL_DB'] = 'veterinaria'
mysql = MySQL(app)

# inicia sesión para envio de mesnsajes por flash
app.secret_key  =  "mysecretkey"

user = ''
admin1 = ''


# routes
@app.route("/")
def Index():
    error =  "No hay conexión con la Base de Datos"
    classe = " width='100' height='100' "
    src = "src='/static/img/triste.jpg'" 
    div = "<div align='center'> "
    divc = "</div>"
    try:
        per = mysql.connection.cursor()
    except :
        return "<br><br><br><br><br><br><br><br><br><br>{} <img {} {} ><h1>No hay conexión con la Base de Datos</h1> {}".format(div, classe, src, divc)
    else:
        
        per = mysql.connection.cursor()
        per.execute("SELECT a.IDanimal, a.nombre, a.foto, a.numsocio, m.mensajeSocio FROM animal a JOIN avisos m  ON a.IDanimal = m.IDanimal WHERE visto = %s ", ("no",) )
        mensajeSocio = per.fetchall()
        per.close()
        
        per = mysql.connection.cursor()
        per.execute("SELECT DATE_ADD(fecha,INTERVAL 358 DAY), DATE_ADD(fecha,INTERVAL 350 DAY), DATE_ADD(fecha,INTERVAL 334 DAY) FROM vacuna WHERE fecha <> %s ORDER BY fecha;", (" "))
        mascotas = per.fetchall()
        per.close()
        
        fecha1 = date.today()
        fechaFinal = []
        fechaFinal15 = []
        fechaFinal30 = []
        for m in mascotas:
            if m[0] == fecha1:
                fecha = "si"
                fechaFinal.append(fecha)
                return render_template('index.html', admin1 = admin1,  user = user, mensajeSocio = mensajeSocio, fechaFinal = fechaFinal)
            if m[1] == fecha1:
                fecha = "si"
                fechaFinal15.append(fecha)
                return render_template('index.html', admin1 = admin1,  user = user, mensajeSocio = mensajeSocio, fechaFinal15 = fechaFinal15)
            if m[2] == fecha1:
                fecha = "si"
                fechaFinal30.append(fecha)
                return render_template('index.html', admin1 = admin1,  user = user, mensajeSocio = mensajeSocio, fechaFinal30 = fechaFinal30)
        return render_template('index.html', admin1 = admin1,  user = user, mensajeSocio = mensajeSocio, fechaFinal = fechaFinal)
    
@app.route("/sinConexion")
def sinConexion():
    error = "No hay conexión con la Base de Datos"
    return render_template('sinConexión.html', error = error)

@app.route("/android", methods = ["POST", "GET"])
def android():
    if request.method == 'POST':
        global nsocio
        global CIsocio
        usuario = request.form['usuario']
        
        clave = request.form['password']
        per = mysql.connection.cursor()
        per.execute("SELECT nombre, apellido, numsocio, CIpersona FROM persona WHERE usuario = %s AND clave = %s", (usuario, clave,))
        validacion = per.fetchall()
        per.close()
        per = mysql.connection.cursor()
        
        nombredic = "nombre"
        apellidodic = "apellido"
        numsociodic = "socio"
        for x in validacion:
          xx = x
        nsocio = xx[2]
        CIsocio = xx[3]
        
            
        js3 = {nombredic:xx[0], apellidodic:xx[1], numsociodic:xx[2], "success": True}
        
        validacion1= jsonify(js3)
        
        return validacion1
    return render_template('android.html')

@app.route("/androidMascotas/<string:id>", methods = ["POST", "GET"])
def androidMascotas(id):
        
        per = mysql.connection.cursor() 
        per.execute("SELECT nombre, descripcionespecie, descripcionraza, peso, foto, IDanimal FROM animal WHERE numsocio = %s", (nsocio,))
        mascota = per.fetchall()
        per.close()
        js2 = []
        if (len(mascota) == 0):
            js1 = {"nombre": "Sin Mascotas", "especie": "Sin Mascotas", "raza": "Sin Mascotas", "nombrefoto": "http://192.168.43.57/fotos/ninguna.jpg", "idanimal": "Sin Mascotas",  "success":True}
            js2.append(js1)
            js3 = {"usuario":js2}
           
          
            print(js3)
            mascota1= jsonify(js3)
        
            print(mascota1)
            return mascota1
        for f in mascota:
            ff = f
            js1 = {"nombre": ff[0], "especie": ff[1], "raza": ff[2], "nombrefoto": "http://192.168.43.57/fotos/"+ ff[4], "idanimal": ff[5],  "success":True}
        
            js2.append(js1)
        js3 = {"usuario":js2}
           
        #js = js2    
        print(js3)
        mascota1= jsonify(js3)
        
        print(mascota1)
        return mascota1
    #return render_template('android.html')

@app.route("/androidMascotas2/<string:id>", methods = ["POST", "GET"])
def androidMascotas2(id):
    #if request.method == 'POST':
        global nmascota
        nmascota = id
        
        per = mysql.connection.cursor() 
        per.execute("SELECT nombre, descripcionespecie, descripcionraza, peso, foto, color, sexo, IDanimal FROM animal WHERE IDanimal = %s", (nmascota,))
        mascota = per.fetchall()
        per.close()
        
        per = mysql.connection.cursor()
        per.execute("SELECT  fechaNacimiento FROM animal WHERE IDanimal = %s", (nmascota,))
        fechaNac = per.fetchone()
        per.close()
        
        per = mysql.connection.cursor()
        per.execute("SELECT  hora FROM agendas WHERE mascota = %s ORDER BY IDagenda DESC;", (nmascota,))
        cons = per.fetchone()
        per.close()
        
        
        per = mysql.connection.cursor()
        per.execute("SELECT  mensajeVeterinaria FROM avisos WHERE IDanimal = %s ORDER BY fecha DESC;", (nmascota,))
        aviso = per.fetchone()
        per.close()
        if(aviso):
            for av in aviso:
                mensaje = av 
        else:
            mensaje = "No hay mensajes"
            print(mensaje)
        per = mysql.connection.cursor()
        per.execute("SELECT  vacunaAnual FROM consulta WHERE IDanimal = %s ORDER BY vacunaAnual DESC;", (nmascota,))
        vacuna = per.fetchone()
        per.close()
        print(vacuna)
        
        if vacuna:
            for fechaV in vacuna:
                fechaVacuna = fechaV
            anoVacuna = fechaVacuna.year
            print(anoVacuna)
        else:
            anoVacuna = 0000
        if anoVacuna != 1111:
            proximo = anoVacuna + 1
            proximoAno = str(proximo)
            mesVacuna = fechaVacuna.month
            proximoMes = str(mesVacuna)
            diaVacuna = fechaVacuna.day
            proximoDia = str(diaVacuna)
            nuevaVacuna = proximoDia + "/" + proximoMes + "/" + proximoAno
        else:
            nuevaVacuna = "No hay registro"
        
        per = mysql.connection.cursor()
        per.execute("SELECT fecha FROM agendas WHERE mascota = %s ORDER BY IDagenda DESC;", (nmascota,))
        fechaConsulta = per.fetchone()
        per.close()
        
        per = mysql.connection.cursor()
        per.execute("SELECT motivo, anamnesia, eog, consulta, diagnostico, pronostico, colaterales, CIpersonaVeterinario, fechaConsulta, IDanimal, diagnosticorecortado, IDconsulta, cantidadAdjuntos FROM consulta WHERE IDanimal = %s ORDER BY IDconsulta DESC;", (nmascota,))
        historia = per.fetchall()
        per.close()
        
        per = mysql.connection.cursor()
        per.execute("SELECT adjunto, fechaAdjunto, tituloAdjunto FROM archivos WHERE IDanimal = %s ORDER BY IDconsulta DESC;", (nmascota,))
        adjuntos = per.fetchall()
        per.close()
        
        for i in adjuntos:
            if i is None:
                adjuntos = ""
                
        #Si existe al menos un registro de consulta clínica para esta mascota, se crea un archivo en excel que puede ser accedido por el usuário.
        if historia:
            per = mysql.connection.cursor()
            per.execute("SELECT motivo, anamnesia, eog, consulta, diagnostico, colaterales, fechaConsulta FROM consulta WHERE IDanimal = %s ORDER BY  fechaConsulta DESC;", (nmascota,) )
            historia2 = per.fetchall()
            per.close()
            per2 = pd.DataFrame(historia2)
            per2.columns=["Motivo de Consulta", "Anamnnesis","EOG","EOP","Diagnóstico Presuntivo", "Colaterales Sugeridos", "Fecha de consulta"]
            per2.reset_index (drop=True).to_excel("static/fotos/Consultas.xlsx", header=True, index= False)
            
        else:
            shutil.copy('static/excel/Consultas.xlsx', 'static/fotos')
        
        if  fechaNac != "":
            global fechaActual
            fechaActual = date.today()
            for fecha in fechaNac:
                fechaNac2 = fecha
            anoActual = fechaActual.year
            mesActual = fechaActual.month
            diaActual = fechaActual.day
            anoInicial = fechaNac2.year
            mesInicial = fechaNac2.month
            anoFinal = anoActual - anoInicial
            mesFinal = mesActual - mesInicial
        
        if anoFinal == 0:
            anoFinal = 0
        if mesFinal == 0:
            mesFinal = 0 
        if mesInicial > mesActual and anoFinal == 0:
            mesAno = 12 - mesInicial 
            mesFinal = mesActual + mesAno
        if mesInicial > mesActual and anoFinal != 0:
            mesAno = 12 - mesInicial 
            mesFinal = mesActual + mesAno
            anoFinal = anoFinal - 1
        
            anoFinal = str(anoFinal)
            mesFinal = str(mesFinal)
        fechaFinal = (anoFinal)
        
        js2 = []
        
        for f in mascota:
            ff = f
        
        if  fechaConsulta != None:
            for fechaC in fechaConsulta:
                fechaConsulta2 = fechaC
                anoConsulta = fechaConsulta2.year
                mesConsulta = fechaConsulta2.month
                diaConsulta = fechaConsulta2.day
                anoConsulta2 = str(fechaConsulta2.year)
                mesConsulta2 = str(fechaConsulta2.month)
                diaConsulta2 = str(fechaConsulta2.day)
                print(anoConsulta2)
            
                
            if anoConsulta >= anoActual and mesConsulta >= mesActual:
                for cons2 in cons:
                    cons3 = cons2
                cons3 = str(cons2)
                print(cons3)
                fechaFinal = str(fechaFinal)
                
                js1 = {"nombre": ff[0], "especie": "Espécie: " + ff[1], "raza": "Raza: " + ff[2], "nombrefoto": "http://192.168.43.57/fotos/"+ ff[4], "sexo": "Sexo: " + ff[6], "edad": "Edad: " + fechaFinal + " año", "peso": "Peso: " + ff[3] + "Kg", "color": "Color: " + ff[5], "consulta": ff[0] + " tiene consulta agendada para el dia: " + diaConsulta2 + "/" +  mesConsulta2 + "/" + anoConsulta2 + " a la hora " + cons3, "aviso": mensaje, "vacuna": "Vencimiento de vacuna anual: " + nuevaVacuna, "success":True}
                
                js2.append(js1)
                js3 = {"usuario":js2}
                    
                mascota1= jsonify(js3)
                    
                return mascota1
        
        fechaFinal = str(fechaFinal)
        js1 = {"nombre": ff[0], "especie": "Espécie: " + ff[1], "raza": "Raza: " + ff[2], "nombrefoto": "http://192.168.43.57/fotos/"+ ff[4], "sexo": "Sexo " +  ff[6], "edad": "Edad: " + fechaFinal + "año",  "peso": "Peso: " + ff[3] + "Kg", "color": "Color: " + ff[5], "consulta": ff[0] + " no tiene consultas agendadas", "aviso": mensaje, "vacuna": "Vencimiento de vacuna anual: " + nuevaVacuna,"success":True}
        js2.append(js1)
        js3 = {"usuario":js2}
        
        mascota1= jsonify(js3)
        
        return mascota1

@app.route('/registroUsuario')
def registroUsuario():
    return render_template('registroUsuario.html')

@app.route('/inicio')
def inicio():
    per = mysql.connection.cursor()
    per.execute("SELECT a.IDanimal, a.nombre, a.foto, a.numsocio, m.mensajeSocio FROM animal a JOIN avisos m  ON a.IDanimal = m.IDanimal WHERE visto = %s ", ("no",) )
    mensajeSocio = per.fetchall()
    per.close()
    #per = mysql.connection.cursor()
    #per.execute("SELECT * FROM avisos WHERE visto = %s ORDER BY  fecha DESC;", ("no",) )
    #mensajeSocio = per.fetchone()
    #print(mensajeSocio)
    return render_template('index.html', admin1 = admin1,  user = user, mensajeSocio = mensajeSocio)

@app.route('/reportesR2')
def reportesR2():
    fecha = datetime.now()
    ano = fecha.strftime("%Y")
    mesActual = fecha.strftime("%m")
    meses = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    mesActual = meses[fecha.month - 1]
    return render_template('reportesR2.html', mesActual = mesActual)

@app.route('/respaldar')
def respaldar():
    mensaje = " "
    return render_template('respaldo.html', mensaje = mensaje)

@app.route('/respaldo', methods = ["POST", "GET"])
def respaldo():
    if request.method == 'POST':
        respaldo = request.form['respaldo']
        fecha2 = datetime.now()
        dia = str(fecha2.day)
        mes = str(fecha2.month)
        anio = str(fecha2.year)
        hora = str(fecha2.hour)
        minuto = str(fecha2.minute)
        
        fecha = dia + "_" + mes + "_" + anio + "_" + hora + "_" + minuto  
        ruta = '{}:/Respaldo/Respaldo{}.sql'.format(respaldo, fecha)
        print(ruta)
        if os.path.isdir("{}:/Respaldo/".format(respaldo)):
            dumpcmd = 'mysqldump -h 127.0.0.1 -u prueba -pveterinaria veterinaria > {}'.format(ruta)
            print(dumpcmd)
            os.system(dumpcmd)
            mensaje = "Respaldo exitoso"
            return render_template('respaldo.html', mensaje = mensaje)
        
        if os.path.isdir("{}:/".format(respaldo)):
            mkdir("{}:/Respaldo/".format(respaldo))
            dumpcmd = 'mysqldump -h 127.0.0.1 -u prueba -pveterinaria veterinaria > {}'.format(ruta)
            os.system(dumpcmd)
            mensaje = "Creacion de carpeta y Respaldo exitosos"
            return render_template('respaldo.html', mensaje = mensaje)    

         
        mensaje2 = "No se puede respaldar. Verifique la letra de la unidad o que el dispositivo externo este conectado"
        return render_template('respaldo.html', mensaje2 = mensaje2)

@app.route('/ayuda_video')
def ayuda_video():
    return render_template('ayuda_video.html', admin1 = admin1,  user = user)

@app.route('/estadisticas')
def estadisticas():
    per = mysql.connection.cursor()
    per.execute("SELECT numsocio FROM persona_cliente WHERE categoria = %s OR categoria = %s", ("A", "C",))
    socioTotal = per.fetchall()
    per.close()
    if socioTotal:
        socioTotal = len(socioTotal)
        
        per = mysql.connection.cursor()
        per.execute("SELECT numsocio FROM persona_cliente WHERE categoria = %s", ("A",))
        socioCategoriaA = per.fetchall()
        per.close()
        if (len(socioCategoriaA)!=0):
            socioCategoriaA = len (socioCategoriaA)
            socioCategoriaAp = (socioCategoriaA/socioTotal)*100
            socioCategoriaAp = round(socioCategoriaAp)
        else:
            socioCategoriaAp = 0
        per = mysql.connection.cursor()
        per.execute("SELECT numsocio FROM persona_cliente WHERE categoria = %s", ("C",))
        socioCategoriaC = per.fetchall()
        per.close()
        if (len(socioCategoriaC)!=0):
            socioCategoriaC = len (socioCategoriaC)
            socioCategoriaCp = (socioCategoriaC/socioTotal)*100
            socioCategoriaCp = round(socioCategoriaCp)
        else:
            socioCategoriaCp = 0
        per = mysql.connection.cursor()
        per.execute("SELECT numsocio FROM persona_cliente WHERE categoria = %s", ("P",))
        particular = per.fetchall()
        per.close()
        particular = len (particular)
        per = mysql.connection.cursor()
        per.execute("SELECT IDanimal FROM animal WHERE activo <> %s", ("-",))
        mascotasTotal = per.fetchall()
        per.close()
        print(mascotasTotal)
        mascotasTotal = len(mascotasTotal) 
        per = mysql.connection.cursor()
        per.execute("SELECT IDanimal FROM animal WHERE activo = %s", ("Si",))
        mascotasActivas = per.fetchall()
        per.close()
        if(len(mascotasActivas) !=0):
            mascotasActivas = len(mascotasActivas)
            mascotasActivasp = (mascotasActivas/mascotasTotal)*100
            mascotasActivasp  = round(mascotasActivasp)
        else:
            mascotasActivasp = 0
        per = mysql.connection.cursor()
        per.execute("SELECT IDanimal FROM animal WHERE activo = %s", ("No",))
        mascotasInactivas = per.fetchall()
        per.close()
        if(len(mascotasInactivas) !=0):
            mascotasInactivas = len(mascotasInactivas)
            mascotasInactivasp = (mascotasInactivas/mascotasTotal)*100
            mascotasInactivasp  = round(mascotasInactivasp)
        else:
            mascotasInactivasp = 0
        per = mysql.connection.cursor()
        per.execute("SELECT IDanimal FROM animal WHERE descripcionespecie = %s", ("Perro",))
        mascotasPerro = per.fetchall()
        per.close()
        mascotasPerro2 = len(mascotasPerro)
        if(len(mascotasPerro) !=0):
            mascotasPerro = len(mascotasPerro)
            mascotasPerrop = (mascotasPerro/mascotasTotal)*100
            mascotasPerrop  = round(mascotasPerrop)
        else:
            mascotasPerrop = 0
        per = mysql.connection.cursor()
        per.execute("SELECT IDanimal FROM animal WHERE descripcionespecie = %s", ("Gato",))
        mascotasGato = per.fetchall()
        per.close()
        mascotasGato2 = len(mascotasGato)
        if(len(mascotasGato) !=0):
            mascotasGato = len(mascotasGato)
            mascotasGatop = (mascotasGato/mascotasTotal)*100
            mascotasGatop  = round(mascotasGatop)
        else:
            mascotasGatop = 0
        otros = mascotasTotal - mascotasGato2 - mascotasPerro2
        print(otros)
        if otros != 0:
            otrosp = (otros/mascotasTotal)*100
            otrosp = round(otrosp)
            return render_template('estadisticas.html', otrosp = otrosp, otros = otros, mascotasPerrop = mascotasPerrop, mascotasGatop = mascotasGatop, mascotasActivasp = mascotasActivasp, mascotasInactivasp = mascotasInactivasp, socioCategoriaCp = socioCategoriaCp, socioCategoriaAp = socioCategoriaAp, mascotasGato = mascotasGato, mascotasPerro = mascotasPerro, mascotasActivas = mascotasActivas, mascotasInactivas = mascotasInactivas, mascotasTotal = mascotasTotal, particular = particular, socioCategoriaA = socioCategoriaA, socioCategoriaC = socioCategoriaC, socioTotal = socioTotal )
        return render_template('estadisticas.html', otros = otros, mascotasPerrop = mascotasPerrop, mascotasGatop = mascotasGatop, mascotasActivasp = mascotasActivasp, mascotasInactivasp = mascotasInactivasp, socioCategoriaCp = socioCategoriaCp, socioCategoriaAp = socioCategoriaAp, mascotasGato = mascotasGato, mascotasPerro = mascotasPerro, mascotasActivas = mascotasActivas, mascotasInactivas = mascotasInactivas, mascotasTotal = mascotasTotal, particular = particular, socioCategoriaA = socioCategoriaA, socioCategoriaC = socioCategoriaC, socioTotal = socioTotal )
    return render_template('estadisticas.html')

@app.route('/agregarCliente')
def agregarCliente():
    per = mysql.connection.cursor()
    per.execute("SELECT numsocio FROM persona ORDER BY numsocio DESC;")
    sigsocio = per.fetchone() 
    per.close()
    
    if sigsocio:
      return render_template('agregarCliente.html', sigsocio = sigsocio, admin1 = admin1,  user = user)
    return render_template('agregarCliente.html', admin1 = admin1,  user = user)

@app.route('/agenda', methods = ['POST','GET' ])
def agenda():
    if request.method == 'POST':
        horas = ["9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30"]
        id = request.form['id']
        print(id)
        per = mysql.connection.cursor()
        per.execute("SELECT fecha FROM agendas WHERE fecha = %s", (id,))
        agenda = per.fetchall() 
        per.close()
        if len(agenda) == 0:
            horas = ["9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30"]
            horas2= jsonify(horas)
            return horas2
        if len(agenda) != 0:
            per = mysql.connection.cursor()
            per.execute("SELECT hora FROM agendas WHERE fecha = %s", (id,))
            hora = per.fetchall() 
            per.close()
            for i in hora:
                for x in i:
                    hora3 = [x]
        if x in horas:
            horas.remove(x)
        horas2= jsonify(horas)
        return horas2
            
                
            


    
    return render_template('agenda.html')  

@app.route('/agenda2', methods = ['POST','GET' ])
def agenda2():
    if request.method == 'POST':
        global nmascota
        #print(nmascota)
        fecha = request.form['fecha']
        #numsocio = request.form['numsocio']
        #foto = request.files['foto']
        #print(foto)
        hora = request.form['horaReserva']
        motivo = request.form['motivo']
        per = mysql.connection.cursor()
        per.execute("SELECT numsocio FROM animal WHERE IDanimal = %s", (nmascota,))
        persona = per.fetchone()
        per.close()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO agendas (socio, mascota, fecha, hora, motivo) VALUE (%s,%s,%s,%s,%s)", (persona, nmascota, fecha, hora, motivo))
        mysql.connection.commit()
        for r in persona:
            numsocio = r
        ok = {"success":True, "socio": nmascota, "idanimal": nmascota}
        print(ok)   
        mascota1= jsonify(ok)
        
        return mascota1
        
    return render_template('agenda.html')  
        
@app.route('/mensajeSocio', methods = ['POST','GET' ])
def mensajeSocio():
    if request.method == 'POST':
        mensaje = request.form['mensaje']
        print(mensaje)
        print (nmascota)
        fecha = datetime.now()
        fechadia = str(fecha.day)
        fechames = str(fecha.month)
        fechaano = str(fecha.year)
        fechaAlta = fechadia + "/" + fechames + "/" + fechaano
        idanimal = nmascota
        visto = "no"
        per = mysql.connection.cursor()
        per.execute("SELECT numsocio FROM animal WHERE IDanimal = %s", (nmascota,))
        socioMensaje = per.fetchone()
        per.close()
        print(socioMensaje)
        print(idanimal)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO avisos (mensajeSocio, fecha, IDanimal, visto, IDsocio) VALUE (%s,%s,%s,%s,%s)", (mensaje, fechaAlta, idanimal, visto, socioMensaje))
        mysql.connection.commit()
    return ("Hora agendada")

@app.route('/mensajeVeterinaria', methods = ['POST','GET' ])
def mensajeVeterinaria():
    if request.method == 'POST':
        mensaje = request.form['mensaje']
        IDsocio = request.form['socio']
        IDanimal = request.form['animal']
        print(mensaje)
        fecha = datetime.now()
        fechadia = str(fecha.day)
        fechames = str(fecha.month)
        fechaano = str(fecha.year)
        fechaAlta = fechadia + "/" + fechames + "/" + fechaano
        idanimal = nmascota
        visto = "si"
        
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM avisos ")
        mysql.connection.commit()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO avisos (mensajeVeterinaria, fecha, IDanimal, visto, IDsocio) VALUE (%s,%s,%s,%s,%s)", (mensaje, fechaAlta, IDanimal, visto, IDsocio))
        mysql.connection.commit()
        
        per = mysql.connection.cursor()
        per.execute("SELECT a.IDanimal, a.nombre, a.foto, a.numsocio, m.mensajeSocio FROM animal a JOIN avisos m  ON a.IDanimal = m.IDanimal WHERE visto = %s ", ("no",) )
        mensajeSocio = per.fetchall()
        per.close()
        
        print(mensajeSocio)
        return render_template('index.html', admin1 = admin1,  user = user, mensajeSocio = mensajeSocio)

@app.route('/productosAndroid', methods = ['POST','GET' ])
def productosAndroid():
    #if request.method == 'POST':
        per = mysql.connection.cursor()
        per.execute("SELECT nombre, descripcion, marca, precioFinal, foto FROM producto WHERE categoria = %s", ("Productos",) )
        productos = per.fetchall()
        per.close()
        
        js2 = []
        for f in productos:
            ff = f
            precio2 = int(ff[3])
            precio1 = str(precio2)
            precio = ("$ " + precio1)
            js1 = {"nombre": ff[0], "descripcion": ff[1], "marca": ff[2], "nombrefoto": "http://192.168.43.57/fotos/"+ ff[4], "precioFinal": precio, "precioint": precio2, "success":True}
        #js1 = [ff[0], ff[1], ff[2]]
            js2.append(js1)
        js3 = {"productos":js2}
           
        #js = js2    
        print(js3)
        mascota1= jsonify(js3)
        print(mascota1)
        return mascota1
        

@app.route('/mascotas', methods = ['POST','GET' ])
def mascotas():
#permite cargar el select de especie en la plantilla mascotas.
    if request.method == 'POST':
        numsocio = request.form['numsocio']
        per = mysql.connection.cursor()
        per.execute("SELECT IDespecie, descripcion FROM especie")
        especie = per.fetchall()
        per.close()
        per = mysql.connection.cursor()
        per.execute("SELECT numsocio FROM persona_cliente WHERE numsocio = %s", (numsocio,))
        persona = per.fetchone()
        per.close()
        per = mysql.connection.cursor()
        per.execute("SELECT CIpersonaCliente FROM persona_cliente WHERE numsocio = %s", (numsocio,))
        persona2 = per.fetchone()
        per.close()
        print(persona)
        return render_template('mascotas.html',  tabper = persona, tabper2 = persona2, especie = especie, admin1 = admin1,  user = user)
    else:
        per = mysql.connection.cursor()
        per.execute("SELECT IDespecie, descripcion FROM especie")
        especie = per.fetchall()
        per.close()
        per = mysql.connection.cursor()
        per.execute("SELECT socio FROM  mensaje")
        persona = per.fetchone()
        per.close()
        per = mysql.connection.cursor()
        per.execute("SELECT cedula FROM mensaje")
        persona2 = per.fetchone()
        per.close()
        print(persona)
        return render_template('mascotas.html',  tabper = persona, tabper2 = persona2, especie = especie, admin1 = admin1,  user = user)

@app.route('/mascotas2/<string:id>', methods = ['POST','GET' ])
def mascotas2(id):
#permite cargar el select de especie en la plantilla mascotas.
        numsocio = id
        print(numsocio)
        per = mysql.connection.cursor()
        per.execute("SELECT IDespecie, descripcion FROM especie")
        especie = per.fetchall()
        per.close()
        per = mysql.connection.cursor()
        per.execute("SELECT numsocio FROM persona_cliente WHERE numsocio = %s", (numsocio,))
        persona = per.fetchone()
        per.close()
        per = mysql.connection.cursor()
        per.execute("SELECT CIpersonaCliente FROM persona_cliente WHERE numsocio = %s", (numsocio,))
        persona2 = per.fetchone()
        per.close()
        print(persona)
        print(persona2)
        return render_template('mascotas.html',  tabper = persona, tabper2 = persona2, especie = especie, admin1 = admin1,  user = user)
#carga el select de raza en base al select de especie. Trabaja con ajax , un metodo que esta 
#en la carpeta static-
@app.route('/raza', methods = ['POST'])
def raza():
    if request.method == 'POST':
       id = request.form['id']
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM raza WHERE IDespecie = %s', (id))
    raza = cur.fetchall()
    cur.close()
    print(raza)
    raza1= jsonify(raza)
    return raza1
   # return json.dumps(response)

    return render_template('mascotas.html')

@app.route('/especie', methods = ['POST'])
def especie():
    if request.method == 'POST':
       idid = request.form['id']
    cur = mysql.connection.cursor()
    cur.execute('SELECT IDespecie, descripcion FROM especie WHERE IDespecie = %s', (idid))
    id2 = cur.fetchall()
    cur.close()
    print(id2)
    especie = jsonify(id2)
    print(especie)
    return especie
    # return json.dumps(response)

    return render_template('mascotas.html')

@app.route('/categoria', methods = ['POST'])
def categoria():
    if request.method == 'POST':
        id = request.form['id']
        
        p = ("0")
        a = ("10", "5", "2")
        for x in id:    
            if x == "P":
                radio = jsonify(p)
            if x == "A" or x == "C":
                print(a)
                radio = jsonify(a)
                print(a)
        return radio
    
    
   # return json.dumps(response
    return render_template('agregarCliente.html')

@app.route('/agregarEspecieRaza')
def agregarEspecieRaza():
    per = mysql.connection.cursor()
    per.execute("SELECT IDespecie, descripcion FROM especie")
    especie = per.fetchall()
    per.close()
   # return render_template('mascotas.html',  especie = especie)
    return render_template('agregarEspecieRaza.html', especie = especie , admin1 = admin1,  user = user)

@app.route('/agregarEspecie', methods = ['POST','GET' ] )
def agregarEspecie():
    if request.method == 'POST':
       mensajeci = ""
       mensajeciok = ""
       mensajeaddmascota = ""
       mensajecimascotaok = "" 
       mensajeaddmascotano = ""
       nsocioR = request.form['soc']
       try:
            mascota = request.form['mascota']
       except :
            
            descripcion = request.form['descripcion']
            per = mysql.connection.cursor()
            per.execute("SELECT descripcion FROM especie WHERE descripcion = %s", (descripcion,))
            despecie = per.fetchall()
            per.close()
            if len(despecie) != 0:
                mensajeaddmascotano = "Espécie ya registrada"
                print(despecie)
                return busqueda3(nsocioR, mensajeaddmascotano, mensajeaddmascota)
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO especie (descripcion) VALUE (%s)", (descripcion,))
            mysql.connection.commit()
            
            mensajeaddmascota = "Espécie agregada correctamente" 
            return busqueda3(nsocioR, mensajeaddmascotano, mensajeaddmascota)
           
       else:
            mascota = request.form['mascota']
            descripcion = request.form['descripcion']
            per = mysql.connection.cursor()
            per.execute("SELECT descripcion FROM especie WHERE descripcion = %s", (descripcion,))
            despecie = per.fetchall()
            per.close()
            if len(despecie) != 0:
                mensajeaddmascotano = "Espécie ya registrada"
                print(despecie)
                return editar_mascota(mascota, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano)
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO especie (descripcion) VALUE (%s)", (descripcion,))
            mysql.connection.commit()
            
            mensajeaddmascota = "Espécie agregada correctamente" 
            return editar_mascota(mascota, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano)
            

@app.route('/agregarRaza', methods = ['POST','GET' ] )
def agregarRaza():
    if request.method == 'POST':
       mensajeci = ""
       mensajeciok = ""
       mensajeaddmascota = ""
       mensajecimascotaok = "" 
       mensajeaddmascotano = ""
       nsocioR = request.form['soc']
       try:
         mascota = request.form['mascota']
       except :
            mascota = nsocioR
            descripcion = request.form['descripcion']
            print(descripcion)
            numidespecie = request.form['idespecie']
            print(numidespecie)
            if len(numidespecie) == 0:
                mensajeaddmascotano = "Debe indicar Espécie a asignar"
                mensajeaddmascota = ""
                return busqueda3(nsocioR, mensajeaddmascotano)
            per = mysql.connection.cursor()
            per.execute("SELECT descripcion FROM raza  WHERE IDespecie = %s AND descripcion = %s ", (numidespecie, descripcion))
            raza = per.fetchall()
            per.close()
            print(raza)
            if len(raza) != 0:
                mensajeaddmascotano = "Raza ya registrada para esta espécie"
                mensajeaddmascota = ""
                print(raza)
                return busqueda3(nsocioR, mensajeaddmascotano, mensajeaddmascota)
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO raza (descripcion, IDespecie) VALUE (%s,%s)", (descripcion, numidespecie,))
            mysql.connection.commit()
            mensajeaddmascotano = ""
            mensajeaddmascota = "Raza agregada correctamente" 
            
            return busqueda3(nsocioR, mensajeaddmascotano, mensajeaddmascota)
       else:
       
        descripcion = request.form['descripcion']
        print(descripcion)
        numidespecie = request.form['idespecie']
        print(numidespecie)
        if len(numidespecie) == 0:
            mensajeaddmascotano = "Debe indicar Espécie a asignar"
            return editar_mascota(mascota, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano)
        per = mysql.connection.cursor()
        per.execute("SELECT descripcion FROM raza  WHERE IDespecie = %s AND descripcion = %s ", (numidespecie, descripcion))
        raza = per.fetchall()
        per.close()
        print(raza)
        if len(raza) != 0:
            mensajeaddmascotano = "Raza ya registrada para esta espécie"
            print(raza)
            return editar_mascota(mascota, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO raza (descripcion, IDespecie) VALUE (%s,%s)", (descripcion, numidespecie,))
        mysql.connection.commit()
        
        mensajeaddmascota = "Raza agregada correctamente" 
        
        return editar_mascota(mascota, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano)
       
       
           

@app.route('/search')
def search():
    return render_template('busqueda.html')



@app.route("/buscar", methods=["POST", "GET"])
def buscar():
    per = mysql.connection.cursor()
    per.execute("SELECT IDespecie, descripcion FROM especie ORDER BY descripcion;")
    especie = per.fetchall()
    per.close()
    per = mysql.connection.cursor()
    per.execute("SELECT IDraza, descripcion FROM raza ORDER BY descripcion;")
    raza = per.fetchall()
    per.close()
    print(raza)
    return render_template('mascotas.html', especie = especie , raza = raza, admin1 = admin1,  user = user)


#Esto es para el ingreso al programa     
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong... 
    msg = ''
    global user  
    global admin1 
    # Check
    if request.method == 'POST':
       username = request.form['usuario']
       password = request.form['password']
       #print(id)
       cur = mysql.connection.cursor()
       cur.execute('SELECT p.nombre,p.contrasenia,p.CIpersona, pa.CIpersonaAdministrador'
       ' FROM persona p JOIN persona_administrador pa on p.CIpersona = pa.CIpersonaAdministrador'
       ' WHERE p.CIpersona = %s AND p.contrasenia = %s', (username, password))

       admin = cur.fetchall()
       cur.close() 

       per = mysql.connection.cursor()
       per.execute('SELECT p.nombre,p.contrasenia,p.CIpersona, pv.CIpersonaVeterinario'
       ' FROM persona p JOIN persona_veterinario pv on p.CIpersona = pv.CIpersonaVeterinario'
       ' WHERE p.CIpersona = %s AND p.contrasenia = %s', (username, password))

       usuario = per.fetchall()
       per.close() 
      
       if admin: # Create session data, we can access this data in other routes
         # session['loggedin'] = True 
         # session['nombre'] = admin['nombre']
         # session['username'] = admin['CIpersona']
           # Redirect to home page 
        user = 'Admin:' 
        admin1 = admin[0]        
                    
          #return 'Logged in successfully!'
        return render_template('busqueda.html',  admin1 = admin1,  user = user) 
       elif usuario:
           user = 'Usuario:' 
           admin1 = usuario[0]        
                    
           #return 'Logged in successfully!'
           return render_template('busqueda.html',  admin1 = admin1,  user = user) 
       else:
          # Account doesnt exist or username/password incorrect 
          msg = 'Usuario o Password incorrectos!' 
          # Show the login form with message (if any)
    return render_template('index.html', msg=msg) 

#Envia a la página de reportes.html una lista completa de todos los Clientes. Consulta a la base las columnas de las tablas persona y persona_cliente. 
@app.route('/reportes')
def reportes():
    per = mysql.connection.cursor()
    per.execute("SELECT pc.numsocio, pc.CIpersonaCliente, pc.nombre, pc.snombre, pc.apellido, pc.sapellido, pc.correoElectronico, pc.calle, pc.numero, pc.apto, pc.esquina, pc.telefono1, pc.telefono2, pc.fechaAlta, pc.socio, pc.categoria, pc.r FROM persona_cliente pc  ORDER BY pc.numsocio; ")
    persona = per.fetchall()
    per.close()
    #Toma los datos de la variable persona y por intermedio de la libreria pandas, permite crear un documento excel con ellos. Ese documento se guarda en la carpeta mencionada y luego desde el template se le permite acceder.
    if persona:    
        per2 = pd.DataFrame(persona)
        per2.columns=["Número de socio","Cédula","Nombre", "Segundo Nombre","Apellido", "Segundo Apellido", "Email","Calle","Numero", "Apto.", "Esquina","Telefono 1","Telefono 2","Fecha de alta","Socio", "Categoria", "R" ]
        per2.reset_index (drop=True).to_excel("static/img/DatosClientes.xlsx", header=True, index= False)
    return render_template('reportes.html', tabper = persona,  admin1 = admin1,  user = user )

@app.route('/reportesOrden/<string:id>', methods = ["POST","GET"])
def reportesOrden(id):
    orden = id
    per = mysql.connection.cursor()
    per.execute("SELECT pc.numsocio, pc.CIpersonaCliente, pc.nombre, pc.snombre, pc.apellido, pc.sapellido, pc.correoElectronico, pc.calle, pc.numero, pc.esquina, pc.telefono1, pc.telefono2, pc.fechaAlta, pc.socio, pc.categoria, pc.r FROM persona_cliente pc  ORDER BY pc.{}; ".format(orden))
    persona = per.fetchall()
    per.close()
    #Toma los datos de la variable persona y por intermedio de la libreria pandas, permite crear un documento excel con ellos. Ese documento se guarda en la carpeta mencionada y luego desde el template se le permite acceder.
    if persona:
        per2 = pd.DataFrame(persona)
        per2.columns=["Número de socio","Cédula","Nombre", "Segundo Nombre","Apellido", "Segundo Apellido", "Email","Calle","Numero","Esquina","Telefono 1","Telefono 2","Fecha de alta","Socio", "Categoria", "R"]
        per2.reset_index (drop=True).to_excel("static/img/DatosClientes.xlsx", header=True, index= False)
    return render_template('reportes.html', tabper = persona,  admin1 = admin1,  user = user )

@app.route('/reportesBajas')
def reportesBajas():
    per = mysql.connection.cursor()
    per.execute("SELECT pc.numsocio, pc.CIpersonaCliente, pc.nombre, pc.snombre, pc.apellido, pc.sapellido, pc.correoElectronico, pc.calle, pc.numero, pc.esquina, pc.telefono1, pc.telefono2, pc.fechaAlta, pc.socio, pc.categoria,  pc.r, DATE_FORMAT(pc.fechaBaja ,GET_FORMAT(DATE,'EUR')), pc.motivoBaja FROM persona_cliente pc  WHERE pc.categoria = %s AND pc.motivoBaja <> %s AND pc.motivoBaja <> %s ORDER BY pc.fechaBaja DESC; ", ("P", " ", "-"))
    persona = per.fetchall()
    per.close()
    #Toma los datos de la variable persona y por intermedio de la libreria pandas, permite crear un documento excel con ellos. Ese documento se guarda en la carpeta mencionada y luego desde el template se le permite acceder.
    if persona:
        per2 = pd.DataFrame(persona)
        per2.columns=["Número de socio","Cédula","Nombre", "Segundo Nombre","Apellido", "Segundo Apellido", "Email","Calle","Numero","Esquina","Telefono 1","Telefono 2","Fecha de alta","Socio", "Categoria", "R", "Fecha de Baja", "Motivo de Baja"]
        per2.reset_index (drop=True).to_excel("static/img/DatosClientes.xlsx", header=True, index= False)
    return render_template('reportesBajas.html', tabper = persona,  admin1 = admin1,  user = user )

@app.route('/reportesBajasOrden/<string:id>', methods = ["POST","GET"])
def reportesBajasOrden(id):
    orden = id
    per = mysql.connection.cursor()
    per.execute("SELECT pc.numsocio, pc.CIpersonaCliente, pc.nombre, pc.snombre, pc.apellido, pc.sapellido, pc.correoElectronico, pc.calle, pc.numero, pc.esquina, pc.telefono1, pc.telefono2, pc.fechaAlta, pc.socio, pc.categoria,  pc.r, DATE_FORMAT(pc.fechaBaja ,GET_FORMAT(DATE,'EUR')), pc.motivoBaja FROM persona_cliente pc  WHERE pc.categoria = %s AND pc.motivoBaja <> %s AND pc.motivoBaja <> %s ORDER BY {} ".format(orden), ("P", " ", "-"))
    persona = per.fetchall()
    per.close()
    #Toma los datos de la variable persona y por intermedio de la libreria pandas, permite crear un documento excel con ellos. Ese documento se guarda en la carpeta mencionada y luego desde el template se le permite acceder.
    if persona:    
        per2 = pd.DataFrame(persona)
        per2.columns=["Número de socio","Cédula","Nombre", "Segundo Nombre","Apellido", "Segundo Apellido", "Email","Calle","Numero","Esquina","Telefono 1","Telefono 2","Fecha de alta","Socio", "Categoria", "R", "Fecha de Baja", "Motivo de Baja"]
        per2.reset_index (drop=True).to_excel("static/img/DatosClientes.xlsx", header=True, index= False)
    return render_template('reportesBajas.html', tabper = persona,  admin1 = admin1,  user = user )
#Envia a la página de reportesMascotas.html una lista completa de todos las Mascotas. Consulta a la base las columnas de las tablas animal, persona, especie y raza. 
@app.route('/reportesMascotas')
def reportesMascotas():
    per = mysql.connection.cursor()
    per.execute("SELECT m.nombre, e.descripcion, r.descripcion, m.sexo,  m.color, m.peso, m.talla, m.activo, m.categoria, DATE_FORMAT(m.fechaNacimiento ,GET_FORMAT(DATE,'EUR')),  pc.nombre, pc.apellido, pc.CIpersonaCliente, pc.numsocio, m.fechaAfiliacion, m.IDanimal, DATE_FORMAT(c.fecha ,GET_FORMAT(DATE,'EUR'))  FROM animal m, persona_cliente pc, raza r, especie e, vacuna c  WHERE m.IDclianimal  = pc.CIpersonaCliente AND m.IDraza = r.IDraza AND r.IDespecie = e.IDespecie AND c.IDanimal = m.IDanimal ORDER BY fecha;")
    mascotas = per.fetchall()
    per.close()
 
    #Toma los datos de la variable persona y por intermedio de la libreria pandas, permite crear un documento excel con ellos. Ese documento se guarda en la carpeta mencionada y luego desde el template se le permite acceder.
    if mascotas:
        per2 = pd.DataFrame(mascotas)
        per2.columns=["Nombre","Espécie","Raza","Sexo","Color","Peso","Talla","Activo","Categoria","Fecha de nacimiento","Nombre cliente/dueño","Apellido","Número Cédula", "Número de Socio", "Ingreso", "ID Animal", "Vacuna Anual"]
        per2.reset_index (drop=True).to_excel("static/img/DatosMascotas.xlsx", header=True, index= False)
    return render_template('reportesMascotas.html', tabmascota = mascotas, admin1 = admin1,  user = user)

@app.route('/reportesMascotasOrden/<string:id>', methods = ["POST","GET"])
def reportesMascotasOrden(id):
    orden = id
    per = mysql.connection.cursor()
    per.execute("SELECT m.nombre, e.descripcion, r.descripcion, m.sexo,  m.color, m.peso, m.talla, m.activo, m.categoria, DATE_FORMAT(m.fechaNacimiento ,GET_FORMAT(DATE,'EUR')),  pc.nombre, pc.apellido, pc.CIpersonaCliente, pc.numsocio, m.fechaAfiliacion, m.IDanimal, DATE_FORMAT(c.fecha ,GET_FORMAT(DATE,'EUR'))  FROM animal m, persona_cliente pc, raza r, especie e, vacuna c  WHERE m.IDclianimal  = pc.CIpersonaCliente AND m.IDraza = r.IDraza AND r.IDespecie = e.IDespecie AND c.IDanimal = m.IDanimal ORDER BY {};".format(orden))
    mascotas = per.fetchall()
    per.close()
 
    #Toma los datos de la variable persona y por intermedio de la libreria pandas, permite crear un documento excel con ellos. Ese documento se guarda en la carpeta mencionada y luego desde el template se le permite acceder.
    if mascotas:    
        per2 = pd.DataFrame(mascotas)
        per2.columns=["Nombre","Espécie","Raza","Sexo","Color","Peso","Talla","Activo","Categoria","Fecha de nacimiento","Nombre cliente/dueño","Apellido","Número Cédula", "Número de Socio", "Ingreso", "ID Animal", "Vacuna Anual"]
        per2.reset_index (drop=True).to_excel("static/img/DatosMascotas.xlsx", header=True, index= False)
    return render_template('reportesMascotas.html', tabmascota = mascotas, admin1 = admin1,  user = user)

@app.route('/reportesVacunas')
def reportesVacunas():
    per = mysql.connection.cursor()
    per.execute("SELECT m.nombre, r.descripcion, e.descripcion, m.sexo,  DATE_ADD(c.fecha,INTERVAL 365 DAY), m.peso, m.talla, m.activo, m.categoria, DATE_FORMAT(m.fechaNacimiento ,GET_FORMAT(DATE,'EUR')), pc.nombre, pc.apellido, pc.CIpersonaCliente, pc.numsocio, m.fechaAfiliacion, m.IDanimal, DATE_FORMAT(c.fecha ,GET_FORMAT(DATE,'EUR')), c.vacunaProxima, pc.telefono1  FROM animal m, persona_cliente pc, raza r, especie e, vacuna c  WHERE m.IDclianimal  = pc.CIpersonaCliente AND m.IDraza = r.IDraza AND r.IDespecie = e.IDespecie AND c.IDanimal = m.IDanimal AND c.fecha <> %s ORDER BY c.fecha;", (" "))
    mascotas = per.fetchall()
    per.close()
    print(mascotas)
    fecha1 = date.today()
    fechaFinal = []
    fechaFinal2 = []
    if mascotas:
        for m in mascotas:
            fecha = m[4] - fecha1
            #fechaF.append(fecha)
            
            fechaF = (m[0], m[1], m[2], m[17], m[3], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[12], m[13], m[14], m[15], m[16], m[18], fecha)
            fechaFinal.append(fechaF)
            print(fechaFinal)
            fechaF2 = (m[0], m[2], m[1], m[3], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[12], m[13], m[14], m[18], m[16],m[17], fecha)
            fechaFinal2.append(fechaF2)
          
    #Toma los datos de la variable persona y por intermedio de la libreria pandas, permite crear un documento excel con ellos. Ese documento se guarda en la carpeta mencionada y luego desde el template se le permite acceder.
        per2 = pd.DataFrame(fechaFinal2)
        per2.columns=["Nombre","Espécie","Raza","Sexo","Peso","Talla","Activo","Categoria","Fecha de nacimiento","Nombre cliente/dueño","Apellido","Número Cédula", "Número de Socio", "Ingreso", "Teléfono", "Vacuna Anual", "Próxima Vacuna", "Restan próxima vacuna (dias)"]
        per2.reset_index (drop=True).to_excel("static/img/DatosMascotas.xlsx", header=True, index= False)
    return render_template('reportesMascotasVacunas.html', tabmascota = mascotas, admin1 = admin1,  user = user, fechaFinal = fechaFinal)

@app.route('/reportesMascotasVacunasOrden/<string:id>', methods = ["POST","GET"])
def reportesMascotasVacunasOrden(id):
    orden = id
    per = mysql.connection.cursor()
    per.execute("SELECT m.nombre, r.descripcion, e.descripcion, m.sexo,  DATE_ADD(c.fecha,INTERVAL 365 DAY), m.peso, m.talla, m.activo, m.categoria, DATE_FORMAT(m.fechaNacimiento ,GET_FORMAT(DATE,'EUR')), pc.nombre, pc.apellido, pc.CIpersonaCliente, pc.numsocio, m.fechaAfiliacion, m.IDanimal, DATE_FORMAT(c.fecha ,GET_FORMAT(DATE,'EUR')), c.vacunaProxima, pc.telefono1  FROM animal m, persona_cliente pc, raza r, especie e, vacuna c  WHERE m.IDclianimal  = pc.CIpersonaCliente AND m.IDraza = r.IDraza AND r.IDespecie = e.IDespecie AND c.IDanimal = m.IDanimal AND fecha <> %s ORDER BY {};".format(orden), (" "))
    mascotas = per.fetchall()
    per.close()
    
    fecha1 = date.today()
    fechaFinal = []
    fechaFinal2 = []
    if mascotas:
        for m in mascotas:
            fecha = m[4] - fecha1
            #fechaF.append(fecha)
            
            fechaF = (m[0], m[1], m[2], m[17], m[3], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[12], m[13], m[14], m[15], m[16], m[18], fecha)
            fechaFinal.append(fechaF)
            print(fechaFinal)
            fechaF2 = (m[0], m[2], m[1], m[3], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[12], m[13], m[14], m[18], m[16],m[17], fecha)
            fechaFinal2.append(fechaF2)
        print(fechaFinal)   
        #Toma los datos de la variable persona y por intermedio de la libreria pandas, permite crear un documento excel con ellos. Ese documento se guarda en la carpeta mencionada y luego desde el template se le permite acceder.
        per2 = pd.DataFrame(fechaFinal2)
        per2.columns=["Nombre","Espécie","Raza","Sexo","Peso","Talla","Activo","Categoria","Fecha de nacimiento","Nombre cliente/dueño","Apellido","Número Cédula", "Número de Socio", "Ingreso", "Teléfono", "Vacuna Anual", "Próxima Vacuna", "Restan próxima vacuna (dias)"]
        per2.reset_index (drop=True).to_excel("static/img/DatosMascotas.xlsx", header=True, index= False)
    return render_template('reportesMascotasVacunas.html', tabmascota = mascotas, admin1 = admin1,  user = user, fechaFinal = fechaFinal)

@app.route('/reportesVacunasVencimiento')
def reportesVacunasVencimiento():
    per = mysql.connection.cursor()
    per.execute("SELECT m.nombre, r.descripcion, e.descripcion, m.sexo,  DATE_ADD(c.fecha,INTERVAL 358 DAY), m.peso, m.talla, m.activo, m.categoria, DATE_FORMAT(m.fechaNacimiento ,GET_FORMAT(DATE,'EUR')), pc.nombre, pc.apellido, pc.CIpersonaCliente, pc.numsocio, m.fechaAfiliacion, m.IDanimal, DATE_FORMAT(c.fecha ,GET_FORMAT(DATE,'EUR')), c.vacunaProxima, pc.telefono1, DATE_ADD(c.fecha,INTERVAL 350 DAY), DATE_ADD(c.fecha,INTERVAL 334 DAY)  FROM animal m, persona_cliente pc, raza r, especie e, vacuna c  WHERE m.IDclianimal  = pc.CIpersonaCliente AND m.IDraza = r.IDraza AND r.IDespecie = e.IDespecie AND c.IDanimal = m.IDanimal AND c.fecha <> %s ORDER BY fecha;", (" "))
    mascotas = per.fetchall()
    per.close()
    fecha1 = date.today()
    fechaFinal7 = []
    fechaFinal2 = []
    fechaFinal15 = []
    fechaFinal30 = []
    if mascotas:
        for m in mascotas:
            if m[4] == fecha1:
                fecha7 = "En 7 dias"
                fechaF7 = (m[0], m[1], m[2], m[17], m[3], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[12], m[13], m[14], m[15], m[16], m[18], fecha7)
                fechaFinal7.append(fechaF7)
                fechaF7Excel = (m[0], m[2], m[1], m[3], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[12], m[13], m[14], m[18], m[16],m[17], fecha7)
                fechaFinal2.append(fechaF7Excel)
                
            if m[19] == fecha1:
                fecha15 = "En 15 dias"
                fechaF15 = (m[0], m[1], m[2], m[17], m[3], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[12], m[13], m[14], m[15], m[16], m[18], fecha15)
                fechaFinal15.append(fechaF15)
                fechaF15Excel = (m[0], m[2], m[1], m[3], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[12], m[13], m[14], m[18], m[16],m[17], fecha15)
                fechaFinal2.append(fechaF15Excel)
                
            if m[20] == fecha1:
                
                fecha30 = "En 1 mes"
                fechaF30 = (m[0], m[1], m[2], m[17], m[3], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[12], m[13], m[14], m[15], m[16], m[18], fecha30)
                fechaFinal30.append(fechaF30)
                fechaF30Excel = (m[0], m[2], m[1], m[3], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[12], m[13], m[14], m[18], m[16],m[17], fecha30)
                fechaFinal2.append(fechaF30Excel)
                print(fecha30)
            
        #Toma los datos de la variable persona y por intermedio de la libreria pandas, permite crear un documento excel con ellos. Ese documento se guarda en la carpeta mencionada y luego desde el template se le permite acceder.
        per2 = pd.DataFrame(fechaFinal2)
        per2.columns=["Nombre","Espécie","Raza","Sexo","Peso","Talla","Activo","Categoria","Fecha de nacimiento","Nombre cliente/dueño","Apellido","Número Cédula", "Número de Socio", "Ingreso", "Teléfono", "Vacuna Anual", "Próxima Vacuna", "Restan próxima vacuna (dias)"]
        per2.reset_index (drop=True).to_excel("static/img/DatosMascotas.xlsx", header=True, index= False)
    return render_template('reportesVacunasVencimiento.html', tabmascota = mascotas, admin1 = admin1,  user = user, fechaFinal7 = fechaFinal7, fechaFinal15 = fechaFinal15, fechaFinal30 = fechaFinal30)

@app.route('/reportesMascotasVacunasVencimientoOrden/<string:id>', methods = ["POST","GET"])
def reportesMascotasVacunasVencimientoOrden(id):
    orden = id
    per = mysql.connection.cursor()
    per.execute("SELECT m.nombre, r.descripcion, e.descripcion, m.sexo,  DATE_ADD(c.fecha,INTERVAL 358 DAY), m.peso, m.talla, m.activo, m.categoria, DATE_FORMAT(m.fechaNacimiento ,GET_FORMAT(DATE,'EUR')), pc.nombre, pc.apellido, pc.CIpersonaCliente, pc.numsocio, m.fechaAfiliacion, m.IDanimal, DATE_FORMAT(c.fecha ,GET_FORMAT(DATE,'EUR')), c.vacunaProxima, pc.telefono1, DATE_ADD(c.fecha,INTERVAL 350 DAY), DATE_ADD(c.fecha,INTERVAL 334 DAY)  FROM animal m, persona_cliente pc, raza r, especie e, vacuna c  WHERE m.IDclianimal  = pc.CIpersonaCliente AND m.IDraza = r.IDraza AND r.IDespecie = e.IDespecie AND c.IDanimal = m.IDanimal AND c.fecha <> %s ORDER BY {};".format(orden), (" "))
    mascotas = per.fetchall()
    per.close()
    fecha1 = date.today()
    fechaFinal7 = []
    fechaFinal2 = []
    fechaFinal15 = []
    fechaFinal30 = []
    if mascotas:
        for m in mascotas:
            if m[4] == fecha1:
                fecha7 = "En 7 dias"
                fechaF7 = (m[0], m[1], m[2], m[17], m[3], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[12], m[13], m[14], m[15], m[16], m[18], fecha7)
                fechaFinal7.append(fechaF7)
                fechaF7Excel = (m[0], m[2], m[1], m[3], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[12], m[13], m[14], m[18], m[16],m[17], fecha7)
                fechaFinal2.append(fechaF7Excel)
                
            if m[19] == fecha1:
                fecha15 = "En 15 dias"
                fechaF15 = (m[0], m[1], m[2], m[17], m[3], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[12], m[13], m[14], m[15], m[16], m[18], fecha15)
                fechaFinal15.append(fechaF15)
                fechaF15Excel = (m[0], m[2], m[1], m[3], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[12], m[13], m[14], m[18], m[16],m[17], fecha15)
                fechaFinal2.append(fechaF15Excel)
                
            if m[20] == fecha1:
                
                fecha30 = "En 1 mes"
                fechaF30 = (m[0], m[1], m[2], m[17], m[3], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[12], m[13], m[14], m[15], m[16], m[18], fecha30)
                fechaFinal30.append(fechaF30)
                fechaF30Excel = (m[0], m[2], m[1], m[3], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[12], m[13], m[14], m[18], m[16],m[17], fecha30)
                fechaFinal2.append(fechaF30Excel)
                print(fecha30)
            
        #Toma los datos de la variable persona y por intermedio de la libreria pandas, permite crear un documento excel con ellos. Ese documento se guarda en la carpeta mencionada y luego desde el template se le permite acceder.
        per2 = pd.DataFrame(fechaFinal2)
        per2.columns=["Nombre","Espécie","Raza","Sexo","Peso","Talla","Activo","Categoria","Fecha de nacimiento","Nombre cliente/dueño","Apellido","Número Cédula", "Número de Socio", "Ingreso", "Teléfono", "Vacuna Anual", "Próxima Vacuna", "Restan próxima vacuna (dias)"]
        per2.reset_index (drop=True).to_excel("static/img/DatosMascotas.xlsx", header=True, index= False)
    return render_template('reportesVacunasVencimiento.html', tabmascota = mascotas, admin1 = admin1,  user = user, fechaFinal7 = fechaFinal7, fechaFinal15 = fechaFinal15, fechaFinal30 = fechaFinal30)

@app.route('/reportesR', methods = ["POST"])
def reportesR():
    if request.method == 'POST':
        r2 = "2"
        r10 = "10"
        fecha = datetime.now()
        ano = fecha.strftime("%Y")
        mesActual = fecha.strftime("%m")
        meses = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
        mesActual = meses[fecha.month - 1]
        
        r = request.form['r']
        mes = request.form['mes']
        
        if r == "1":    
            per = mysql.connection.cursor()
            per.execute("SELECT  p.nombre, p.snombre, p.apellido, p.sapellido, p.calleC, p.numeroC, p.categoria, p.r, p.numsocio, a.precio, a.impuestos, a.precioFinal, p.aptoC FROM persona_cliente p RIGHT OUTER JOIN producto a ON p.categoria = a.categoria WHERE p.r = %s ORDER BY calle, numero; ", (r2,))
            datosr2 = per.fetchall()
            per.close()
            print(mesActual)
            return render_template('reportesR.html', datosr2 = datosr2, ano = ano, mes = mes, mesActual = mesActual)
        if r == "2":    
            per = mysql.connection.cursor()
            per.execute("SELECT  p.nombre, p.snombre, p.apellido, p.sapellido, p.calleC, p.numeroC, p.categoria, p.r, p.numsocio, a.precio, a.impuestos, a.precioFinal, p.aptoC FROM persona_cliente p RIGHT OUTER JOIN producto a ON p.categoria = a.categoria WHERE p.r = %s ORDER BY numsocio; ", (r2,))
            datosr2 = per.fetchall()
            per.close()
            return render_template('reportesR.html', datosr2 = datosr2, ano = ano, mes = mes, mesActual = mesActual)
        if r == "5":    
            per = mysql.connection.cursor()
            per.execute("SELECT  p.nombre, p.snombre, p.apellido, p.sapellido, p.calleC, p.numeroC, p.categoria, p.r, p.numsocio, a.precio, a.impuestos, a.precioFinal, p.aptoC FROM persona_cliente p RIGHT OUTER JOIN producto a ON p.categoria = a.categoria WHERE p.r = %s ORDER BY apellido; ", (r2,))
            datosr2 = per.fetchall()
            per.close()
            return render_template('reportesR.html', datosr2 = datosr2, ano = ano, mes = mes, mesActual = mesActual)
        if r == "3":    
            per = mysql.connection.cursor()
            per.execute("SELECT  p.nombre, p.snombre, p.apellido, p.sapellido, p.calleC, p.numeroC, p.categoria, p.r, p.numsocio, a.precio, a.impuestos, a.precioFinal, p.aptoC FROM persona_cliente p RIGHT OUTER JOIN producto a ON p.categoria = a.categoria WHERE p.r = %s ORDER BY calle, numero; ", (r10,))
            datosr2 = per.fetchall()
            per.close()
            return render_template('reportesR.html', datosr2 = datosr2, ano = ano, mes = mes, mesActual = mesActual)
        if r == "4":    
            per = mysql.connection.cursor()
            per.execute("SELECT  p.nombre, p.snombre, p.apellido, p.sapellido, p.calle, p.numero, p.categoria, p.r, p.numsocio, a.precio, a.impuestos, a.precioFinal, p.aptoC FROM persona_cliente p RIGHT OUTER JOIN producto a ON p.categoria = a.categoria WHERE p.r = %s ORDER BY numsocio; ", (r10,))
            datosr2 = per.fetchall()
            per.close()
            return render_template('reportesR.html', datosr2 = datosr2, ano = ano, mes = mes, mesActual = mesActual)
        if r == "6":    
            per = mysql.connection.cursor()
            per.execute("SELECT  p.nombre, p.snombre, p.apellido, p.sapellido, p.calleC, p.numeroC, p.categoria, p.r, p.numsocio, a.precio, a.impuestos, a.precioFinal, p.aptoC FROM persona_cliente p RIGHT OUTER JOIN producto a ON p.categoria = a.categoria WHERE p.r = %s ORDER BY apellido; ", (r10,))
            datosr2 = per.fetchall()
            per.close()
            return render_template('reportesR.html', datosr2 = datosr2, ano = ano, mes = mes, mesActual = mesActual)
        
    return "error"

@app.route('/reportesMascotasBuscar/<string:id>', methods = ["POST","GET"])
def reportesMascotasBuscar(id):
           mensajeci = ""
           mensajeciok = ""
           mensajeaddmascota = ""
           mensajecimascotaok = ""
           mensajeaddmascotano = ""
           return editar_mascota(id, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano )

@app.route('/seleccionarMascota/<string:id>', methods = ["POST","GET"])
def seleccionarMascota(id):
           mascota = id
           mensajeci = ""
           mensajeciok = ""
           mensajeaddmascota = ""
           mensajecimascotaok = ""
           mensajeaddmascotano = ""
           print(mascota) 
           return editar_mascota(mascota, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano) 

@app.route('/busqueda2/<string:id>', methods = ["POST","GET"])
def busqueda2(id):
           mensajeci = ""
           mensajeciok = ""
           mensajeaddmascota = ""
           mensajecimascotaok = ""
           mensajeaddmascotano = ""
           numsocio = id  
           global sociox
           sociox = numsocio
           if busqueda!=0:
               per = mysql.connection.cursor()
               per.execute("SELECT pc.CIpersonaCliente, pc.nombre, pc.apellido, pc.correoElectronico, pc.calle, pc.esquina, pc.numero, pc.telefono1, pc.telefono2, pc.fechaAlta, pc.socio, pc.numsocio, pc.snombre, pc.sapellido FROM  persona_cliente pc  WHERE pc.numsocio = %s", (numsocio,))
               global persona
               persona = per.fetchall()
               per.close()
               per = mysql.connection.cursor()
               per.execute("SELECT m.IDanimal, m.nombre, m.sexo, m.tipoPelo, m.color, m.talla, m.peso, m.activo, m.categoria, m.edadAlAfiliarse, m.fechaNacimiento, r.IDraza, r.descripcion, e.descripcion, m.foto FROM animal m  RIGHT OUTER JOIN raza r ON r.IDraza = m.IDraza RIGHT JOIN especie e ON r.IDespecie = e.IDespecie WHERE numsocio = %s", (numsocio,))
               global mascota
               mascota = per.fetchall()
               per.close()
               per = mysql.connection.cursor()
               per.execute("SELECT c.IDanimal FROM consulta c RIGHT OUTER JOIN animal a ON a.IDanimal = c.IDanimal RIGHT JOIN persona p ON a.numsocio = p.numsocio WHERE p.numsocio = %s ORDER BY c.IDconsulta DESC;", (numsocio,))
               numanimales = per.fetchone()
               per.close()
               if mascota == ():
                    numsocio = 0
                    per = mysql.connection.cursor()
                    per.execute("SELECT IDanimal FROM animal WHERE numsocio = %s", (numsocio,))
                    mascota = per.fetchone()
                    per.close()
                    return editar_mascota(1, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano)
               for x in numanimales:
                   if x == None:
                        per = mysql.connection.cursor()
                        per.execute("SELECT IDanimal FROM animal WHERE numsocio = %s", (numsocio,))
                        mascota = per.fetchone()
                        per.close()
                        return editar_mascota(mascota, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota,mensajeaddmascotano )
               return editar_mascota(numanimales, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano)
               
               
@app.route("/busqueda3/<string:id>", methods=["POST"])
def busqueda3(id, mensajeaddmascotano, mensajeaddmascota):
   if request.method == 'POST':
       mensajeci = ""
       mensajeciok = ""
       mensajeaddmascota = mensajeaddmascota
       mensajecimascotaok = ""
       mensajeaddmascotano = mensajeaddmascotano
       numsocio = id
       
       if len(numsocio)!=0  and numsocio.isdigit():
           per = mysql.connection.cursor()
           busqueda= per.execute("SELECT numsocio FROM persona_cliente  WHERE numsocio = %s", (numsocio,))           
           global sociox
           sociox = numsocio
           if busqueda!=0:
               per.execute("SELECT CIpersonacliente, nombre, apellido, correoElectronico, calle, esquina, numero, telefono1, telefono2, fechaAlta, socio, numsocio, snombre, sapellido FROM persona_cliente WHERE numsocio = %s", (numsocio,))
               global persona
               persona = per.fetchall()
               per.close()
               
               per = mysql.connection.cursor()
               per.execute("SELECT m.IDanimal, m.nombre, m.sexo, m.tipoPelo, m.color, m.talla, m.peso, m.activo, m.categoria, m.edadAlAfiliarse, m.fechaNacimiento, r.IDraza, r.descripcion, e.descripcion, m.foto FROM animal m  RIGHT OUTER JOIN raza r ON r.IDraza = m.IDraza RIGHT JOIN especie e ON r.IDespecie = e.IDespecie WHERE numsocio = %s", (numsocio,))
               global mascota
               mascota = per.fetchall()
               per.close()
               
               per = mysql.connection.cursor()
               per.execute("SELECT c.IDanimal FROM consulta c RIGHT OUTER JOIN animal a ON a.IDanimal = c.IDanimal RIGHT JOIN persona_cliente p ON a.numsocio = p.numsocio WHERE p.numsocio = %s ORDER BY c.IDconsulta DESC;", (numsocio,))
               numanimales = per.fetchone()
               per.close()
               if mascota == ():
                    numsocio = 0
                    per = mysql.connection.cursor()
                    per.execute("SELECT IDanimal FROM animal WHERE numsocio = %s", (numsocio,))
                    mascota = per.fetchone()
                    per.close()
                    return editar_mascota(1, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano)
               for x in numanimales:
                   if x == None:
                        per = mysql.connection.cursor()
                        per.execute("SELECT IDanimal FROM animal WHERE numsocio = %s", (numsocio,))
                        mascota = per.fetchone()
                        per.close()
                        return editar_mascota(numanimales, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota,mensajeaddmascotano )
               return editar_mascota(numanimales, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano)
               
           else:
               mensajeBusqueda=("No hay resultado para este número!")
               mensajeBusqueda2 = ("Hacer click para ingresar nuevo cliente")
               print(mensajeBusqueda)
               flash(mensajeBusqueda, category="categoria")
               flash(mensajeBusqueda2, category="volverinicio")
               return render_template("busqueda.html")
       else:
           print("ingresar cedula para busqueda")
           return render_template('inicio.html')          
        
                    
#Toma el valor que se ingresa en el campo "Busqueda Cliente" en las paginas. Hace la busqueda en la base de las tablas persona y persona_cliente extrayendo solo el cliente asociado a la cedula ingresada con los datos de las columnas solicitadas y devuelve el resultado a mostrarClientes2.html. Tambien la misma función trae las mascotas del cliente en base a la cedula del cliente (tabla animal/columna IDclianimal).]
@app.route("/busqueda", methods=["POST"])
def busqueda():
   if request.method == 'POST':
       mensajeci = ""
       mensajeciok = ""
       mensajeaddmascota = ""
       mensajecimascotaok = ""
       mensajeaddmascotano = ""
       numsocio = request.form['numsocio']
       global soc
       soc = numsocio
       if len(numsocio)!=0  and numsocio.isdigit():
           per = mysql.connection.cursor()
           busqueda= per.execute("SELECT numsocio FROM persona_cliente  WHERE numsocio = %s", (numsocio,))           
           global sociox
           sociox = numsocio
           if busqueda!=0:
               per.execute("SELECT CIpersonacliente, nombre, apellido, correoElectronico, calle, esquina, numero, telefono1, telefono2, fechaAlta, socio, numsocio, snombre, sapellido FROM persona_cliente WHERE numsocio = %s", (numsocio,))
               global persona
               persona = per.fetchall()
               per.close()
               
               per = mysql.connection.cursor()
               per.execute("SELECT m.IDanimal, m.nombre, m.sexo, m.tipoPelo, m.color, m.talla, m.peso, m.activo, m.categoria, m.edadAlAfiliarse, m.fechaNacimiento, r.IDraza, r.descripcion, e.descripcion, m.foto FROM animal m  RIGHT OUTER JOIN raza r ON r.IDraza = m.IDraza RIGHT JOIN especie e ON r.IDespecie = e.IDespecie WHERE numsocio = %s", (numsocio,))
               global mascota
               mascota = per.fetchall()
               per.close()
               
               per = mysql.connection.cursor()
               per.execute("SELECT c.IDanimal FROM consulta c RIGHT OUTER JOIN animal a ON a.IDanimal = c.IDanimal RIGHT JOIN persona_cliente p ON a.numsocio = p.numsocio WHERE p.numsocio = %s ORDER BY c.IDconsulta DESC;", (numsocio,))
               numanimales = per.fetchone()
               per.close()
               if mascota == ():
                    numsocio = 0
                    per = mysql.connection.cursor()
                    per.execute("SELECT IDanimal FROM animal WHERE numsocio = %s", (numsocio,))
                    mascota = per.fetchone()
                    per.close()
                    return editar_mascota(1, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano)
               for x in numanimales:
                   if x == None:
                        per = mysql.connection.cursor()
                        per.execute("SELECT IDanimal FROM animal WHERE numsocio = %s", (numsocio,))
                        mascota = per.fetchone()
                        per.close()
                        return editar_mascota(numanimales, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota,mensajeaddmascotano )
               return editar_mascota(numanimales, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano)
               
           else:
               mensajeBusqueda=("No hay resultado para este número!")
               mensajeBusqueda2 = ("Hacer click para ingresar nuevo cliente")
               print(mensajeBusqueda)
               flash(mensajeBusqueda, category="categoria")
               flash(mensajeBusqueda2, category="volverinicio")
               return render_template("busqueda.html")
       else:
           print("ingresar cedula para busqueda")
           return render_template('inicio.html')

@app.route('/filtro', methods=['POST'])
def filtro():
    if request.method == 'POST':
        CIpersonaCliente=request.form['CIpersonaCliente']
        numsocio=request.form['numsocio']
        nombre=request.form['nombre']
        apellido=request.form['apellido']
        snombre=request.form['snombre']
        sapellido=request.form['sapellido']
        correoElectronico = request.form['correoElectronico'] 
        calle = request.form['calle']
        esquina = request.form['esquina']
        
        telefono1 = request.form['telefono']
        telefono2 = request.form['telefono']             
        datos = CIpersonaCliente + nombre + apellido + correoElectronico + calle + esquina + telefono1 + telefono2 + snombre + sapellido + numsocio
        #socio = request.form['socio']
        print(datos)
        if (len(datos) ==0):
            persona = datos
            mensajeBusqueda=("Debe haber al menos un parámetro!")
            flash(mensajeBusqueda, category="buscarcliente")
            return render_template("busqueda.html")
    per = mysql.connection.cursor()
    per.execute("SELECT numsocio, CIpersonaCliente, nombre, snombre, apellido, sapellido, correoElectronico, calle, numero, esquina, telefono1, telefono2, fechaAlta, socio, categoria, r FROM persona_cliente WHERE CIpersonaCliente = %s OR nombre = %s OR apellido =%s OR correoElectronico = %s OR calle =%s OR esquina =%s  OR telefono1 =%s OR telefono2 =%s OR snombre =%s OR sapellido =%s OR numsocio =%s ", (CIpersonaCliente, nombre, apellido, correoElectronico, calle,  esquina, telefono1, telefono2, snombre, sapellido, numsocio, )) 
    persona = per.fetchall()
    per.close()
    if (len(persona) ==0):   
        mensajeBusqueda=("No se encontraron resultados!")
        flash(mensajeBusqueda, category="buscarcliente")
        return render_template("busqueda.html")
    per2 = pd.DataFrame(persona)
    per2.columns=["Número de socio","Cédula","Nombre", "Segundo Nombre","Apellido", "Segundo Apellido", "Email","Calle","Esquina", "Numero","Telefono 1","Telefono 2","Fecha de alta","Socio", "Categoria", "R"]
    per2.reset_index (drop=True).to_excel("static/img/DatosClientes.xlsx", header=True, index= False)
    return render_template('reportes.html', tabper = persona,  admin1 = admin1,  user = user )

@app.route('/filtro2', methods=['POST'])
def filtro2():
    if request.method == 'POST':
        nombre=request.form['nombre']
        descripcione=request.form['descripcione']
        descripcionr=request.form['descripcionr']
        color = request.form['color']
        sexo = request.form['sexo']
        peso = request.form['peso']
        categoria = request.form['categoria']
        talla = request.form['talla'] 
        edadAlAfiliarse = request.form['edadAlAfiliarse']            
        datos = nombre + color  + peso + categoria + talla + edadAlAfiliarse + descripcione + descripcionr + sexo
        if (len(datos) ==0):
            mascota = datos
            mensajeBusqueda=("Debe haber al menos un parámetro!")
            flash(mensajeBusqueda, category="buscarmascota")
            return render_template('busqueda.html', tabmascota = mascota,  admin1 = admin1,  user = user )
        per = mysql.connection.cursor()
        per.execute("SELECT a.nombre, a.descripcionespecie, a.descripcionraza, a.sexo, a.color, a.peso, a.talla, a.activo, a.categoria, a.fechaNacimiento, a.nombrecli, a.apellidocli, a.IDclianimal, a.numsocio, a.fechaAfiliacion,  a.IDanimal, DATE_FORMAT(v.fecha ,GET_FORMAT(DATE,'EUR')) FROM animal a RIGHT OUTER JOIN vacuna v ON a.IDanimal = v.IDanimal WHERE a.nombre = %s  OR a.color = %s OR a.peso =%s OR a.talla =%s  OR a.edadAlAfiliarse=%s OR a.descripcionespecie=%s OR a.descripcionraza=%s OR a.categoria=%s OR a.sexo=%s", (nombre, color, peso, talla, edadAlAfiliarse, descripcione, descripcionr, categoria, sexo,)) 
        mascota = per.fetchall()
        per.close()
        if (len(mascota) ==0):
            mensajeBusqueda=("No se econtraron resultados!")
            flash(mensajeBusqueda, category="buscarmascota")
            return render_template("busqueda.html")
        per2 = pd.DataFrame(mascota)
        per2.columns=["Nombre","Espécie","Raza","Sexo","Color","Peso","Talla","Activo","Categoria","Fecha de nacimiento","Nombre cliente/dueño","Apellido","Número Cédula", "Número de Socio", "Ingreso", "ID Animal", "Fecha Vacuna"]
        per2.reset_index (drop=True).to_excel("static/img/DatosMascotas.xlsx", header=True, index= False)
        return render_template('reportesMascotas.html', tabmascota = mascota, admin1 = admin1,  user = user )

@app.route('/androidRegistro', methods=['POST', 'GET'])
def androidRegistro():   
    if request.method == 'POST':  
                 CIpersona=request.form['ci']
                 #numsocio = request.form['numsocio']
                 nombre=request.form['nombre']
                 print(nombre)
                 snombre = "-"
                 apellido=request.form['apellido']
                 sapellido = "-"
                 correoElectronico = request.form['email'] 
                 if (len(correoElectronico) ==0):
                    correoElectronico = "-"
                 calle = request.form['direccion']
                 if (len(calle) ==0):
                    calle = "-"
                 esquina = "-"
                 numero = "-"
                 telefono1 = request.form['telefono']
                 if (len(telefono1) ==0):
                    telefono1 = "-"
                 #telefono2 = request.form['telefono2']
                 #if (len(telefono2) ==0):
                 telefono2 = "-"  
                 cat = "P"
                 
                 #r = request.form["pago"]
                 
                 fecha = datetime.now()
                 fechadia = str(fecha.day)
                 fechames = str(fecha.month)
                 fechaano = str(fecha.year)
                 fechaAlta = fechadia + "/" + fechames + "/" + fechaano
                 per = mysql.connection.cursor()
                 per.execute("SELECT numsocio FROM persona ORDER BY numsocio DESC;")
                 sigsocio = per.fetchone() 
                 per.close()
                 for x in sigsocio:
                     num = int(x)
                     numsocio = num + 1
                 clave = "primera1"
                 usuario = nombre[0] + apellido
                 print (usuario)
                 cur = mysql.connection.cursor()
                 cur.execute("INSERT INTO persona (CIpersona, nombre, apellido, numsocio, snombre, sapellido, clave, usuario) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (CIpersona, nombre, apellido, numsocio, snombre, sapellido, clave, usuario))
                 mysql.connection.commit()
                 cur = mysql.connection.cursor()
                 cur.execute("INSERT INTO persona_cliente (CIpersonaCliente, correoElectronico, calle, esquina, numero, telefono1, telefono2, nombre, apellido, numsocio, snombre, sapellido, categoria, fechaAlta, clave, usuario) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (CIpersona, correoElectronico, calle, esquina, numero, telefono1, telefono2, nombre, apellido, numsocio, snombre, sapellido, cat, fechaAlta, clave, usuario))
                 mysql.connection.commit()
                 #mensaje = "Usuario ingresado correctamente"
                 usuario2 = {"user": usuario, "success": True}
                 ok= jsonify(usuario2)
                 print(usuario2)
                 print(ok)
                 return (ok)

#Espera los datos ingresados en el formulario en la pagina clientes. Con cada uno de esos datos, envia la orden en la base de datos e ingresa un cliente nuevo. Envia mensaje de ok y refresca la página.
@app.route('/add_contact', methods=['POST'])
def add_contact():   
    if request.method == 'POST':
        mensajeciok = ""
        mensajeci = ""
        mensajeaddmascota = ""
        mensajecimascotaok = ""
        mensajeaddmascotano = ""
        CIpersona=request.form['CIpersona']
        numsocio = request.form['numsocio']
        id = numsocio
        if len(numsocio)!=0 and numsocio.isdigit() and len(CIpersona)!=0 and len(CIpersona)<=8 and CIpersona.isdigit() :
            per = mysql.connection.cursor()
            busqueda= per.execute("SELECT numsocio FROM persona  WHERE numsocio = %s", (numsocio,))           
            per = mysql.connection.cursor()
            busqueda2= per.execute("SELECT CIpersonacliente FROM persona_cliente  WHERE CIpersonacliente = %s", (CIpersona,)) 
            if busqueda==0 and busqueda2==0: 
                 #Se crea variable para indicar si al final de la validacion se va a grabar los datos y seguir o no en el loop
                 """grab=0
                 while grab==0:
                     #Se  crea la lista con los datos a validar
                     dato=[(request.form['CIpersona']),(request.form['correoElectronico']),(request.form['calle']),(request.form['esquina']),
                           (request.form['numero']),(request.form['telefono1']),(request.form['telefono2']),
                           (request.form['nombre']),(request.form['apellido']), (request.form['numsocio']),(request.form['snombre']), (request.form['sapellido'])]                        
                     #Se crea la lista con las categorias que va utilizar Flash para mostrar los mensajes
                     categoria=['CIpersona','correoElectronico','calle','esquina','numero','telefono1','telefono2','socio','nombre', 'apellido', 'numsocio','snombre', 'sapellido' ]
                     #Se indica el tamaño de cada campo para validar luego
                     tam=[8,60,20,20,10,9,9,20,20,10,20,20]
                     #Se debe indicar por cada campo a controlar un 1 si es campo obligatorio o 0 si no lo es
                     oblig=[1,0,0,0,0,0,0,1,1,1,0,0,1,1]
                     #Se define el tipo del campo "c" caracter, "n" numerico, "a" alfanumerico, "b" boton, "e" para email se utilizara en la funcion de validacion
                     tipo=["n","e","a","a","a","n","n","c","c","c","n","c","c"]
                     #Se llamara la funcion validar y devolver un 1 o 0 e indicara si se puede grabar los datos, pasando por parametros las listas creadas
                     grab=validardatos(dato,categoria,tam,grab,oblig,tipo)            
                     if grab==1:
                         CIpersona=request.form['CIpersona']
                         numsocio = request.form["numsocio"]"""
                 nombre=request.form['nombre']
                 snombre=request.form['snombre']
                 if (len(snombre) ==0):
                    snombre = "-"
                 apellido=request.form['apellido']
                 sapellido=request.form['sapellido']
                 if (len(sapellido) ==0):
                    sapellido = "-"
                 correoElectronico = request.form['correoElectronico'] 
                 if (len(correoElectronico) ==0):
                    correoElectronico = "-"
                 calle = request.form['calle']
                 if (len(calle) ==0):
                    calle = "-"
                 esquina = request.form['esquina']
                 if (len(esquina) ==0):
                    esquina = "-"
                 numero = request.form['numero']
                 if (len(numero) ==0):
                    numero = "-"
                 apto = request.form['apto']
                 if (len(apto) ==0):
                    apto = "-"
                 numeroC = request.form['numeroC']
                 esquinaC = request.form['esquinaC']
                 aptoC = request.form['aptoC']
                 calleC = request.form['calleC']
                 if (len(calleC) ==0):
                    calleC = calle
                    numeroC = numero
                    aptoC = apto
                    esquinaC = esquina
                 if (len(calleC) !=0 ):
                    calleC = calleC
                    if (len(numeroC) ==0 ):
                        numeroC = "-"
                    if (len(aptoC) ==0 ):
                        aptoC = "-"
                    if (len(esquinaC) ==0 ):
                        esquinaC = "-"
                 telefono1 = request.form['telefono1']
                 if (len(telefono1) ==0):
                    telefono1 = "-"
                 telefono2 = request.form['telefono2']
                 if (len(telefono2) ==0):
                    telefono2 = "-"  
                 cat = request.form["cat"]
                 r = request.form["r"]
                 motivo = "-"
                 fecha = datetime.now()
                 fechadia = str(fecha.day)
                 fechames = str(fecha.month)
                 fechaano = str(fecha.year)
                 fechaAlta = fechadia + "/" + fechames + "/" + fechaano
                 
                 cur = mysql.connection.cursor()
                 cur.execute("INSERT INTO persona (CIpersona, nombre, apellido, numsocio, snombre, sapellido) VALUES (%s,%s,%s,%s,%s,%s)", (CIpersona, nombre, apellido, numsocio, snombre, sapellido))
                 mysql.connection.commit()
                 cur = mysql.connection.cursor()
                 cur.execute("INSERT INTO persona_cliente (CIpersonaCliente, correoElectronico, calle, esquina, numero, telefono1, telefono2, nombre, apellido, numsocio, snombre, sapellido, categoria, r, fechaAlta, motivoBaja, mascotaTitular, calleC, esquinaC, numeroC, apto, aptoC) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (CIpersona, correoElectronico, calle, esquina, numero, telefono1, telefono2, nombre, apellido, numsocio, snombre, sapellido, cat, r, fechaAlta, motivo, 1, calleC, esquinaC, numeroC, apto, aptoC))
                 mysql.connection.commit()                         
                 global sociox
                 sociox = numsocio
                 return editar_mascota(1, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano)
            else:
                print("Cliente ya ingresado")
                flash("Socio y/o CI ya ingresado/s",category="numsocio")                
                return redirect(url_for ("agregarCliente"))               
    per = mysql.connection.cursor()
    per.execute("SELECT numsocio FROM persona  WHERE numsocio = %s", (numsocio,))
    persona = per.fetchone()
    per.close()
    print(persona)
    return editar_mascota(nummascota, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano)



#Cuando se seleccion el boton editar en pagina Clientes.HTML. Se abre un popup con los datos del cliente preseleccionado. Al apretar Guardar cambios, envia por formulario a esta funcion, quien se conecta a la base y actualiza los cambios.
@app.route('/actualizar_cliente/<id>', methods=['POST'])
def actualizar_cliente(id):
    if request.method == 'POST':
        mensajeciok = ""
        mensajeci = ""
        mensajeaddmascota = ""
        mensajecimascotaok = ""
        mensajeaddmascotano = ""
        CIpersona = request.form['CIpersona']
        numsocio = request.form['numsocio']
        
        
        for x in id:
            
            for i in numsocio:
                
                if x != i:
                   
                    per = mysql.connection.cursor()
                    per.execute("SELECT numsocio FROM persona  WHERE numsocio = %s", (numsocio,)) 
                    busqueda = per.fetchall()
                    per.close()
                    
                    if len(busqueda)==0:
                            numsocio = numsocio
                            
                    else: 
                            
                        mensajeci = "Número ya asignado a otro sócio"               
                        return editar_mascota(nummascota, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano ) 
        
                else:
                    per = mysql.connection.cursor()
                    per.execute("SELECT CIpersonacliente FROM persona_cliente  WHERE CIpersonaCliente = %s", (CIpersona,))
                    busqueda2 = per.fetchall()
                    per.close()
                    
                    if len(busqueda2)==0:
                        CIpersona = CIpersona
                    
                    if len(busqueda2) != 0: 
                        per = mysql.connection.cursor()
                        per.execute("SELECT CIpersonaCliente FROM persona_cliente  WHERE CIpersonaCliente = %s AND numsocio = %s", (CIpersona, id,))
                        busqueda3 = per.fetchall()
                        per.close()
                        
                        if len(busqueda3) == 0:
                                    
                                    mensajeci = "CI ya asignada a otro sócio"               
                                    return editar_mascota(nummascota, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano)
                    categoria = request.form['categoria']
                    correoElectronico = request.form['correoElectronico'] 
                    calle = request.form['calle']
                    esquina = request.form['esquina']
                    numero = request.form['numero']
                    apto = request.form['apto']
                    calleC = request.form['calleC']
                    esquinaC = request.form['esquinaC']
                    aptoC = request.form['aptoC']
                    numeroC = request.form['numeroC']
                    telefono1 = request.form['telefono1']
                    telefono2 = request.form['telefono2']
                    r = request.form['r']
                    nombre = request.form['nombre']
                    apellido = request.form['apellido']
                    sapellido = request.form['sapellido']
                    snombre = request.form['snombre']
                    baja = request.form['baja']
                    mascotaTitular = request.form['mascotaTitular']
                    print(mascotaTitular)
                    if baja:
                        fecha = date.today()
                    else:
                        fecha = 0000-00-00
                    
                    if categoria == "A" or categoria == "C":
                        baja = "-"

                    if categoria == "P":
                        mascotaTitular = 0

                    cur = mysql.connection.cursor()
                    cur.execute("""
                                UPDATE persona
                                SET CIpersona = %s,
                                    nombre = %s,
                                    apellido = %s,
                                    numsocio = %s,
                                    sapellido = %s,
                                    snombre = %s
                                WHERE numsocio = %s
                            """, (CIpersona, nombre, apellido, numsocio, sapellido, snombre, id))
                    mysql.connection.commit()
                    cur = mysql.connection.cursor()
                    cur.execute("""
                                UPDATE persona_cliente
                                SET CIpersonacliente = %s,
                                    calle = %s,
                                    numero = %s,
                                    esquina = %s,
                                    telefono1 = %s,
                                    telefono2 = %s,
                                    correoElectronico = %s,
                                    numsocio = %s,
                                    sapellido = %s,
                                    snombre = %s,
                                    categoria = %s,
                                    r = %s,
                                    nombre = %s,
                                    apellido = %s,
                                    fechaBaja = %s,
                                    motivoBaja = %s,
                                    calleC = %s,
                                    numeroC = %s,
                                    esquinaC = %s,
                                    mascotaTitular = %s,
                                    apto = %s,
                                    aptoC = %s
                                WHERE numsocio = %s
                            """, (CIpersona, calle, numero, esquina, telefono1, telefono2, correoElectronico, numsocio, sapellido, snombre, categoria, r, nombre, apellido, fecha, baja, calleC, numeroC, esquinaC, mascotaTitular, apto, aptoC, id))
                    flash('Cliente modificado correctamente')
                    mysql.connection.commit()
                            
                    cur = mysql.connection.cursor()
                    cur.execute("""
                                UPDATE animal
                                SET IDclianimal = %s,
                                    nombrecli = %s,
                                    apellidocli = %s,
                                    snombre = %s,
                                    sapellido = %s,
                                    numsocio = %s
                                WHERE numsocio = %s
                            """, (CIpersona, nombre, apellido, snombre, sapellido, numsocio, id))
                    
                    mysql.connection.commit()
                    mensajeciok = 'Cliente modificado correctamente'
                    return editar_mascota(numeromascota, mensajeci, mensajeciok,  mensajeaddmascota, mensajecimascotaok, mensajeaddmascotano )
                
        
#Recibe los datos enviados desde el formulario del HTML Mascotas y los ingresa a la base de datos.
@app.route('/agregar_mascota', methods=['POST'])
def add_mascota():
    if request.method == 'POST':
        fechaR = (datetime.now())
        mensajeci = ""
        mensajeciok = ""
        mensajecimascotaok = ""
        mensajeaddmascotano = ""
        IDclianimal = request.form['CIpersona']
        numsocio = request.form['numsocio']
        nombre = request.form['nombre']
        IDraza = request.form['raza']
        activo = request.form['activo']
        comentario = request.form['comentario']
        chip = request.form['chip']
        if (len(chip) ==0):
            talla = "-"
        fechaNacimiento = request.form['fechaNacimiento']
        talla = request.form['talla']
        if (len(talla) ==0):
            talla = "-"
        sexo = request.form['sexo']
        peso = request.form['peso']
        if (len(peso) ==0):
            peso = "-"
        color = request.form['color']
        if (len(color) ==0):
            color = "-"
        foto2 = request.files['foto']
        cur = mysql.connection.cursor()
        fecha = datetime.now()
        fechadia = str(fecha.day)
        fechames = str(fecha.month)
        fechaano = str(fecha.year)
        fechaAlta = fechadia + "/" + fechames + "/" + fechaano
        cur.execute("SELECT nombre FROM persona_cliente WHERE numsocio = %s", (numsocio,))
        nombrecli = cur.fetchone()
        cur.close()
        cur = mysql.connection.cursor()
        cur.execute("SELECT apellido FROM persona_cliente WHERE numsocio = %s", (numsocio,))
        apellidocli = cur.fetchone()
        cur.close()
        cur = mysql.connection.cursor()
        cur.execute("SELECT snombre FROM persona_cliente WHERE numsocio = %s", (numsocio,))
        snombre = cur.fetchone()
        cur.close()
        cur = mysql.connection.cursor()
        cur.execute("SELECT sapellido FROM persona_cliente WHERE numsocio = %s", (numsocio,))
        sapellido = cur.fetchone()
        cur.close()
        cur = mysql.connection.cursor()
        cur.execute("SELECT descripcion FROM raza WHERE IDraza = %s", (IDraza,))
        descripcionraza = cur.fetchone()
        cur.close()
        cur = mysql.connection.cursor()
        cur.execute("SELECT IDespecie FROM raza WHERE IDraza = %s", (IDraza,))
        IDespecie = cur.fetchone()
        cur.close()
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT descripcion FROM especie WHERE IDespecie = %s", (IDespecie,))
        descripcionespecie = cur.fetchone()
        cur.close()
        #Guarda en una variable el nombre del archivo
        filename = secure_filename(foto2.filename)
        #Si no se adjunta ninguna foto, la variable pasa a tener un nombre genérico y se guarda ese dato (nombre) y todos los demás en el registro en la base de datos.
        if (len(filename) ==0):
            filename = "ninguna.jpg"
            foto = filename
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO animal (IDclianimal, nombre, activo, fechaNacimiento, talla, peso, color, sexo, IDraza, foto, nombrecli, apellidocli, descripcionraza, descripcionespecie, numsocio, snombre, sapellido, fechaAfiliacion, comentario, chip ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (IDclianimal, nombre, activo, fechaNacimiento, talla, peso, color, sexo, IDraza, foto, nombrecli, apellidocli, descripcionraza, descripcionespecie, numsocio, snombre, sapellido, fechaAlta, comentario, chip ))
            mysql.connection.commit()
            cur = mysql.connection.cursor()
            cur.execute("SELECT IDanimal FROM animal ORDER BY IDanimal DESC;")
            numanimal = cur.fetchone()
            cur.close()
            mensajeaddmascota = "Mascota agregada correctamente"

            CIpersonaveterinario = "18767665"
            motivo = "-"
            anamnesia = "-"
            eog = "-"
            eop = "-"
            tratamiento = "-"
            colaterales = "-"
            id = numanimal
            fechaAlta = "-"

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO consulta (CIpersonaveterinario, motivo, anamnesia, eog, pronostico, tratamiento,  colaterales, IDanimal, fechaConsulta )  VALUES  (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (CIpersonaveterinario, motivo, anamnesia, eog, eop, tratamiento, colaterales, id, fechaAlta))
            mysql.connection.commit()

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO vacuna (IDanimal, vacunaAnualR, fecha)  VALUES  (%s,%s,%s)", (id, "", fechaAlta))
            mysql.connection.commit()
            
            cur = mysql.connection.cursor()
            cur.execute("SELECT categoria FROM persona_cliente WHERE numsocio = %s", (numsocio,))
            categoriaCliente = cur.fetchone()
            cur.close()
            
            cur = mysql.connection.cursor()
            cur.execute("SELECT IDanimal FROM animal WHERE numsocio = %s ORDER BY IDanimal DESC;", (numsocio,))
            mascotasCliente = cur.fetchall()
            cur.close()
            print(len(mascotasCliente))
            for c in categoriaCliente:
                categoria = c[0]
                
            if categoria == "P":
                cur = mysql.connection.cursor()
                cur.execute("""
                UPDATE persona_cliente
                SET mascotaTitular = %s
                    WHERE numsocio = %s
                """, (1, numsocio))
                mysql.connection.commit()
                
                return editar_mascota(numanimal, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano)
            
            if categoria == "A" or categoria == "C":
                if(len(mascotasCliente) == 1):
                    cur = mysql.connection.cursor()
                    cur.execute("""
                    UPDATE persona_cliente
                    SET mascotaTitular = %s
                        WHERE numsocio = %s
                    """, (mascotasCliente, numsocio))
                    mysql.connection.commit()
                return editar_mascota(numanimal, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano )
                
        #Si cargaron foto, se guarda una copia en una carpeta local del proyecto y el nombre se ingresa a la base de datos junto a los demás datos.
        
        fecha = str(datetime.now())
        fecha = fecha.replace(" ", "")
        fecha = fecha.replace("-", "")
        fecha = fecha.replace(":", "")
        fecha = fecha.replace(".", "")
        img = Image.open(foto2)
        foto = img.resize((256,256))
        filename = nombre + fecha + ".jpg"
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #shutil.copy('static/fotos/' + filename, 'C:/xampp/htdocs/fotos')
        #shutil.copy('static/fotos/' + filename, 'C:/xampp/fotos')
        
        foto = filename
        cur = mysql.connection.cursor()
        #cur.execute("INSERT INTO animal (IDclianimal, nombre, activo,  fechaNacimiento, talla, peso, color, sexo, IDraza, foto, nombrecli, apellidocli, descripcionraza, descripcionespecie, numsocio, snombre, sapellido, fechaAfiliacion ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (IDclianimal, nombre, activo, fechaNacimiento, talla, peso, color, sexo, IDraza, foto, nombrecli, apellidocli, descripcionraza, descripcionespecie, numsocio, snombre, sapellido, fechaAlta))
        cur.execute("INSERT INTO animal (IDclianimal, nombre, activo, fechaNacimiento, talla, peso, color, sexo, IDraza, foto, nombrecli, apellidocli, descripcionraza, descripcionespecie, numsocio, snombre, sapellido, fechaAfiliacion, comentario, chip ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (IDclianimal, nombre, activo, fechaNacimiento, talla, peso, color, sexo, IDraza, foto, nombrecli, apellidocli, descripcionraza, descripcionespecie, numsocio, snombre, sapellido, fechaAlta, comentario, chip ))
        mysql.connection.commit()
        cur = mysql.connection.cursor()
        cur.execute("SELECT IDanimal FROM animal ORDER BY IDanimal DESC;")
        numanimal = cur.fetchone()
        cur.close()
        

        CIpersonaveterinario = "18767665"
        motivo = "-"
        anamnesia = "-"
        eog = "-"
        eop = "-"
        tratamiento = "-"
        colaterales = "-"
        id = numanimal
        fechaAlta = "-"

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO consulta (CIpersonaveterinario, motivo, anamnesia, eog, pronostico, tratamiento,  colaterales, IDanimal, fechaConsulta )  VALUES  (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (CIpersonaveterinario, motivo, anamnesia, eog, eop, tratamiento, colaterales, id, fechaAlta))
        mysql.connection.commit()

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO vacuna (IDanimal, vacunaAnualR, fecha )  VALUES  (%s,%s,%s)", (id, "Sin registro", fechaAlta ))
        mysql.connection.commit()
        
        mensajeaddmascota = "Mascota agregada correctamente"
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT IDanimal FROM animal WHERE numsocio = %s ORDER BY IDanimal DESC;", (numsocio,))
        mascotasCliente = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT categoria FROM persona_cliente WHERE numsocio = %s", (numsocio,))
        categoriaCliente = cur.fetchone()
        cur.close()
            
        for c in categoriaCliente:
            categoria = c[0]
                
        if categoria == "P":
            cur = mysql.connection.cursor()
            cur.execute("""
            UPDATE persona_cliente
            SET mascotaTitular = %s
            WHERE numsocio = %s
            """, (1, numsocio))
            mysql.connection.commit()
                
            return editar_mascota(numanimal, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano)
            
        if categoria == "A" or categoria == "C":
            if(len(mascotasCliente) == 1):
                cur = mysql.connection.cursor()
                cur.execute("""
                UPDATE persona_cliente
                SET mascotaTitular = %s
                WHERE numsocio = %s
                """, (mascotasCliente, numsocio))
                mysql.connection.commit()
            return editar_mascota(numanimal, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano )
        

@app.route('/androidMascota', methods=['POST'])
def androidMascota():
    if request.method == 'POST':
        #IDclianimal = request.form['CIpersona']
        #numsocio = request.form['numsocio']
        nombre = request.form['nombre']
        raza = request.form['raza']
        print(raza)
        activo = "Si"
        #fechaNacimiento = request.form['fechaNacimiento']
        talla = ""
        if (len(talla) ==0):
            talla = "-"
        sexo = request.form['sexo']
        print(sexo)
        peso = ""
        if (len(peso) ==0):
            peso = "-"
        color = ""
        if (len(color) ==0):
            color = "-"
        foto = request.form['imagen']
        print(foto)
        cur = mysql.connection.cursor()
        cur.execute("SELECT IDraza FROM raza WHERE descripcion = %s", (raza,))
        IDraza = cur.fetchone()
        cur.close()
        #cur = mysql.connection.cursor()
        #fecha = datetime.now()
        #fechadia = str(fecha.day)
        #fechames = str(fecha.month)
        #fechaano = str(fecha.year)
        #fechaAlta = fechadia + "/" + fechames + "/" + fechaano
        
        #Guarda en una variable el nombre del archivo
        filename = secure_filename(foto.filename)
        #Si no se adjunta ninguna foto, la variable pasa a tener un nombre genérico y se guarda ese dato (nombre) y todos los demás en el registro en la base de datos.
        if (len(filename) ==0):
            #filename = "ninguna.jpg"
            #foto = filename
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO animal (IDclianimal, nombre, activo,  talla, peso, color, sexo, foto, numsocio, IDraza ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (CIsocio, nombre, activo, talla, peso, color, sexo, foto, nsocio, IDraza ))
            mysql.connection.commit()
            #mensajeaddmascota = "Mascota agregada correctamente"
            
            return 
        #Si cargaron foto, se guarda una copia en una carpeta local del proyecto y el nombre se ingresa a la base de datos junto a los demás datos.
        fecha = str(datetime.now())
        fecha = fecha.replace(" ", "")
        fecha = fecha.replace("-", "")
        fecha = fecha.replace(":", "")
        fecha = fecha.replace(".", "")
        #print(fecha)
        filename = nombre + fecha + ".jpg"
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        foto = filename
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO animal (IDclianimal, nombre, activo,  talla, peso, color, sexo, foto, numsocio, IDraza ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (CIsocio, nombre, activo, talla, peso, color, sexo, foto, nsocio, IDraza ))
        #cur.execute("INSERT INTO animal (IDclianimal, nombre, activo, fechaNacimiento, talla, peso, color, sexo, IDraza, foto, nombrecli, apellidocli, descripcionraza, descripcionespecie, numsocio, snombre, sapellido, fechaAfiliacion ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (IDclianimal, nombre, activo, fechaNacimiento, talla, peso, color, sexo, IDraza, foto, nombrecli, apellidocli, descripcionraza, descripcionespecie, numsocio, snombre, sapellido, fechaAlta ))
        mysql.connection.commit()
        
        #mensajeaddmascota = "Mascota agregada correctamente"
        
        return 

#Cuando se selecciona el boton editar para una mascota en página Mostrarclientes2.HTML, se envía a esta función la id de la mascota. Con ese dato, se busca toda la información de la mascota y su historial clínico y se envía a la página editarMascota.
@app.route('/editar_mascota/<string:id>', methods = ["POST","GET"])
def editar_mascota(id, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano):
    global nummascota
    nummascota = id
    fechaFinal = "-"
    mascotadetalle = ""
    mascotadetalle2 = ""
    mascotadetallesi = ""
    mascotadetalleno = ""
    mascotaSi = ""
    mascotaNo = ""
    mascotaEstrella2 = ""
    mascotaEstrella1 = ""
    global fechaActual
    fechaActual = date.today()
    if nummascota == 1:
           #print(sociox)
           nummascota = 1
           cur = mysql.connection.cursor()
           cur.execute("SELECT numsocio FROM animal  WHERE IDanimal = %s", (id,))
           numsocio = cur.fetchone()
           cur.close()
           per = mysql.connection.cursor()
           per.execute("SELECT CIpersonacliente, nombre, apellido, correoElectronico, calle, esquina, numero, telefono1, telefono2, fechaAlta, socio, numsocio, snombre, sapellido, categoria, r, motivoBaja, mascotaTitular, calleC, numeroC, apto, aptoC, esquinaC FROM persona_cliente  WHERE numsocio = %s", (sociox,))
           persona = per.fetchall()
           per.close() 
           cur = mysql.connection.cursor()
           cur.execute('SELECT IDanimal, nombre foto FROM animal  WHERE IDanimal = %s', (nummascota,))
           tabmascotaeditar2 = cur.fetchall()
           cur.close()
           
           mascotaedit5 = []
           mascotaedit4 = ("-","-","-","-","-","-","-","-","-","-","-","-","-","-","ninguna.jpg","-","-", "-")
           mascotaedit5.append(mascotaedit4)
           
           per = mysql.connection.cursor()
           per.execute("SELECT IDespecie, descripcion FROM especie")
           especie = per.fetchall()
           per.close()
           global numeromascota
           numeromascota = 1
           mas2 = [1, "Sin Mascotas"]
           return render_template('mascotas.html', mas2 = mas2, tabmascotaeditar5 = mascotaedit5, mensajeaddmascotano = mensajeaddmascotano, mensajecimascotaok = mensajecimascotaok, mensajeaddmascota = mensajeaddmascota, mensajeciok = mensajeciok, mensajeci = mensajeci, tabmascotaeditar2 = tabmascotaeditar2, especie = especie ,  admin1 = admin1,  user = user, tabper = persona, fechaActual = fechaActual)
    numeromascota = id
    #print(numeromascota)
    cur = mysql.connection.cursor()
    cur.execute("SELECT numsocio FROM animal  WHERE IDanimal = %s", (id,))
    numsocio = cur.fetchone()
    cur.close()
    
    per = mysql.connection.cursor()
    per.execute("SELECT m.IDanimal, m.nombre, m.sexo, m.tipoPelo, m.color, m.talla, m.peso, m.activo, m.categoria, m.edadAlAfiliarse, m.fechaNacimiento, r.IDraza, r.descripcion, e.descripcion, m.foto, m.fechaAfiliacion, e.IDespecie, m.comentario, m.chip FROM animal m  RIGHT OUTER JOIN raza r ON r.IDraza = m.IDraza RIGHT JOIN especie e ON r.IDespecie = e.IDespecie  WHERE m.IDanimal = %s", (id,))
    mascotaedit3 = per.fetchall()
    per.close()

    per = mysql.connection.cursor()
    per.execute("SELECT IDanimal FROM animal WHERE numsocio = %s", (numsocio,))
    numAnimales = per.fetchall()
    per.close()
    
    if (len(numAnimales) <= 7):   
        cur = mysql.connection.cursor()
        cur.execute('SELECT a.nombre, a.IDanimal, a.foto, a.activo FROM animal a  RIGHT OUTER JOIN persona_cliente p ON a.numsocio = p.numsocio AND a.activo = %s  WHERE a.numsocio = %s ORDER BY fechaAfiliacion DESC;', ("si",numsocio,))
        mascotadetalle = cur.fetchall()
        cur.close()
        cur = mysql.connection.cursor()
        #cur.execute("SELECT nombre, IDanimal FROM animal  WHERE numsocio = %s", (numsocio,))
        cur.execute('SELECT a.nombre, a.IDanimal, a.foto, a.activo FROM animal a  RIGHT OUTER JOIN persona_cliente p ON a.numsocio = p.numsocio AND a.activo = %s  WHERE a.numsocio = %s ORDER BY fechaAfiliacion DESC;', ("no",numsocio,))
        mascotadetalle2 = cur.fetchall()
        cur.close()

    if (len(numAnimales) > 7):   
        cur = mysql.connection.cursor()
        cur.execute('SELECT a.nombre, a.IDanimal, a.foto, a.activo FROM animal a  RIGHT OUTER JOIN persona_cliente p ON a.numsocio = p.numsocio AND a.activo = %s  WHERE a.numsocio = %s ORDER BY fechaAfiliacion DESC;', ("si",numsocio,))
        mascotadetallesi = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('SELECT a.nombre, a.IDanimal, a.foto, a.activo FROM animal a  RIGHT OUTER JOIN persona_cliente p ON a.numsocio = p.numsocio AND a.activo = %s  WHERE a.numsocio = %s ORDER BY fechaAfiliacion DESC;', ("si",numsocio,))
        mascotaSi = cur.fetchall()
        cur.close()
        cur = mysql.connection.cursor()
        #cur.execute("SELECT nombre, IDanimal FROM animal  WHERE numsocio = %s", (numsocio,))
        cur.execute('SELECT a.nombre, a.IDanimal, a.foto, a.activo FROM animal a  RIGHT OUTER JOIN persona_cliente p ON a.numsocio = p.numsocio AND a.activo = %s  WHERE a.numsocio = %s ORDER BY fechaAfiliacion DESC;', ("no",numsocio,))
        mascotaNo = cur.fetchall()
        cur.close()
        
        if (len(mascotadetallesi) > 7): 
            cur = mysql.connection.cursor()
            cur.execute('SELECT a.nombre, a.IDanimal, a.foto, a.activo FROM animal a  RIGHT OUTER JOIN persona_cliente p ON a.numsocio = p.numsocio AND a.activo = %s  WHERE a.numsocio = %s  ORDER BY fechaAfiliacion DESC LIMIT 7;', ("si",numsocio,))
            mascotadetallesi = cur.fetchall()
            cur.close()
            
        if (len(mascotadetallesi) < 7): 
            num = len(mascotadetallesi)
            num = int (num)
            dif = 7 - num 
            
            cur = mysql.connection.cursor()
            cur.execute('SELECT a.nombre, a.IDanimal, a.foto, a.activo FROM animal a  RIGHT OUTER JOIN persona_cliente p ON a.numsocio = p.numsocio AND a.activo = %s  WHERE a.numsocio = %s  ORDER BY fechaAfiliacion DESC LIMIT 7;', ("si",numsocio,))
            mascotadetallesi = cur.fetchall()
            cur.close()
            
            cur = mysql.connection.cursor()
            cur.execute('SELECT a.nombre, a.IDanimal, a.foto, a.activo FROM animal a  RIGHT OUTER JOIN persona_cliente p ON a.numsocio = p.numsocio AND a.activo = %s  WHERE a.numsocio = %s ORDER BY fechaAfiliacion DESC LIMIT %s;', ("no",numsocio,dif,))
            mascotadetalleno2 = cur.fetchall()
            cur.close()
            mascotadetalleno = []
            i = 1
            for mascota in mascotadetalleno2:    
                mascota3 = mascota
                while i <= dif:
                    i = i + 1
                
                mascota2 = (mascota3[0], mascota3[1], mascota3[2], mascota3[3])
                mascotadetalleno.append(mascota2)
                
            
            if (len(mascotadetalleno) > 7):
                cur = mysql.connection.cursor()
                cur.execute('SELECT a.nombre, a.IDanimal, a.foto, a.activo FROM animal a  RIGHT OUTER JOIN persona_cliente p ON a.numsocio = p.numsocio AND a.activo = %s  WHERE a.numsocio = %s ORDER BY fechaAfiliacion DESC LIMIT 7;', ("no",numsocio,))
                mascotadetalleno = cur.fetchall()
                cur.close()
                
    
    #print(mascotadetallesi)
    #print(mascotadetalleno)
    
    per = mysql.connection.cursor()
    per.execute("SELECT m.IDanimal, m.nombre, m.sexo, m.tipoPelo, m.color, m.talla, m.peso, m.activo, m.categoria, m.edadAlAfiliarse, m.fechaNacimiento, r.IDraza, r.descripcion, e.descripcion, m.foto, m.fechaAfiliacion FROM animal m  RIGHT OUTER JOIN raza r ON r.IDraza = m.IDraza RIGHT JOIN especie e ON r.IDespecie = e.IDespecie AND m.activo = %s WHERE m.IDanimal = %s", ("si", id,))
    mascotaedit = per.fetchall()
    per.close()
    per = mysql.connection.cursor()
    per.execute("SELECT m.IDanimal, m.nombre, m.sexo, m.tipoPelo, m.color, m.talla, m.peso, m.activo, m.categoria, m.edadAlAfiliarse, m.fechaNacimiento, r.IDraza, r.descripcion, e.descripcion, m.foto, m.fechaAfiliacion FROM animal m  RIGHT OUTER JOIN raza r ON r.IDraza = m.IDraza RIGHT JOIN especie e ON r.IDespecie = e.IDespecie AND m.activo = %s WHERE m.IDanimal = %s", ("no", id,))
    mascotaedit2 = per.fetchall()
    per.close()
    
    for comentario in mascotaedit3:
        
        mensajecimascotaavisook = comentario[17]
    per = mysql.connection.cursor()
    per.execute("SELECT IDespecie, descripcion FROM especie")
    especie = per.fetchall()
    per.close()
    per = mysql.connection.cursor()
    per.execute("SELECT IDraza, descripcion FROM raza ORDER BY descripcion")
    raza = per.fetchall()
    per.close()
    
    per = mysql.connection.cursor()
    per.execute("SELECT  m.fechaNacimiento FROM animal m  RIGHT OUTER JOIN raza r ON r.IDraza = m.IDraza RIGHT JOIN especie e ON r.IDespecie = e.IDespecie WHERE IDanimal = %s", (nummascota,))
    fechaNac = per.fetchone()
    per.close()
    
    if  fechaNac:
        anoActual = fechaActual.year
        mesActual = fechaActual.month
        
        for fecha in fechaNac:
            #fechaNac2 = fecha
            
            anoInicial = fecha.year
            mesInicial = fecha.month
        anoFinal = anoActual - anoInicial
        mesFinal = mesActual - mesInicial
        
        if anoFinal == 0:
            anoFinal = 0
        if mesFinal == 0:
            mesFinal = 0 
        if mesInicial <= mesActual and anoFinal == 0:
            mesFinal = mesActual - mesInicial
            mesFinal = str(mesFinal)
            fechaFinal = mesFinal + " meses" 
        
        
        if mesInicial < mesActual and anoFinal != 0:
            mesFinal = mesActual - mesInicial
            anoFinal = str(anoFinal)
            mesFinal = str(mesFinal)
            fechaFinal = anoFinal + "a" + " " + mesFinal + "m" 
        if mesInicial > mesActual and anoFinal != 0:
            mesFinal = 12 - (mesInicial - mesActual)
            anoFinal = anoFinal -1
            anoFinal = str(anoFinal)
            mesFinal = str(mesFinal)
            fechaFinal = anoFinal + "a" + " " + mesFinal + "m" 
        if mesInicial == mesActual and anoFinal != 0:
            anoFinal = anoActual - anoInicial
            anoFinal = str(anoFinal)
            fechaFinal = anoFinal + " años" 
        
    
    per = mysql.connection.cursor()
    per.execute("SELECT motivo, anamnesia, eog, consulta, tratamiento, pronostico, colaterales, CIpersonaVeterinario, fechaConsulta, IDanimal, diagnosticorecortado, IDconsulta, cantidadAdjuntos FROM consulta WHERE IDanimal = %s ORDER BY IDconsulta DESC;", (nummascota,))
    historia = per.fetchall()
    per.close()
    per = mysql.connection.cursor()
    per.execute("SELECT fecha FROM vacuna WHERE IDanimal = %s", (nummascota,))
    vacuna = per.fetchone()
    per.close()
       
    for fechaV in vacuna:   
        if fechaV:
            
            fechaVacuna = fechaV
            anoVacuna = fechaV.year
            
        else:
            anoVacuna = "-"
        
    if anoVacuna != "-":
        proximo = anoVacuna 
        proximoAno = str(proximo)
        mesVacuna = fechaVacuna.month
        proximoMes = str(mesVacuna)
        diaVacuna = fechaVacuna.day
        proximoDia = str(diaVacuna)
        nuevaVacuna = proximoDia + "/" + proximoMes + "/" + proximoAno
    else:
        nuevaVacuna = "-"
    per = mysql.connection.cursor()
    per.execute("SELECT adjunto, fechaAdjunto, tituloAdjunto FROM archivos WHERE IDanimal = %s ORDER BY IDconsulta DESC;", (nummascota,))
    adjuntos = per.fetchall()
    per.close()
    for i in adjuntos:
        if i is None:
            adjuntos = ""
    
    #Si existe al menos un registro de consulta clínica para esta mascota, se crea un archivo en excel que puede ser accedido por el usuário.
    if historia:
        per = mysql.connection.cursor()
        per.execute("SELECT motivo, anamnesia, eog, consulta, tratamiento, colaterales, fechaConsulta FROM consulta WHERE IDanimal = %s ORDER BY  fechaConsulta DESC;", (id,) )
        historia2 = per.fetchall()
        per.close()
        per2 = pd.DataFrame(historia2)
        per2.columns=["Motivo de Consulta", "Anamnnesis","EOG","EOP", "Tratamiento", "Diagnóstico Presuntivo / Colaterales", "Fecha de consulta"]
        per2.reset_index (drop=True).to_excel("static/img/Consultas.xlsx", header=True, index= False)
        
    else:
        shutil.copy('static/excel/Consultas.xlsx', 'static/img')

    per = mysql.connection.cursor()
    per.execute("SELECT CIpersonacliente, nombre, apellido, correoElectronico, calle, esquina, numero, telefono1, telefono2, fechaAlta, socio, numsocio, snombre, sapellido, categoria, r, motivoBaja, mascotaTitular, calleC, numeroC, apto, aptoC, esquinaC FROM persona_cliente  WHERE numsocio = %s", (numsocio,))
    persona2 = per.fetchall()
    per.close()
    per = mysql.connection.cursor()
    persona = []
    for p in persona2:
        per1 = p[14]
        per2 = p[17]

    for me in mascotaedit:
        
        if me[0] == p[17]:
            mascotaEstrella1 = "ok"
            print("hello")
            print(mascotaEstrella1)
    for me2 in mascotaedit2:
        if me2[0] == p[17]:
            mascotaEstrella2 = "ok"
    per = mysql.connection.cursor()
    per.execute("SELECT nombre FROM animal  WHERE IDanimal = %s", (per2,))
    mas = per.fetchone()
    per.close()
    per = mysql.connection.cursor()
    per.execute("SELECT IDanimal, nombre FROM animal  WHERE IDanimal = %s", (per2,))
    mas2 = per.fetchall()
    per.close()
    
    per = mysql.connection.cursor()
    per.execute("SELECT IDanimal, nombre FROM animal  WHERE numsocio = %s", (numsocio,))
    mas3 = per.fetchall()
    per.close()
    persona4 = []
    disabled = ""
    if per1 == "P":
            mas = "-"
            disabled = "-"
            #mas2 = ""
            #mas3 = ""
            #persona4 = (p[0],p[1], p[2],p[3], p[4],p[5], p[6],p[7], p[8],p[9], p[10],p[11], p[12], p[13], p[14],p[15], p[16], "-", p[18],p[19], p[20])
            #persona.append(persona4)
            #print(persona)
            #return render_template('mascotas.html', mas3 = mas3, mas2 = mas2, mas = mas, mensajeaddmascotano = mensajeaddmascotano, mensajeaddmascota = mensajeaddmascota, mensajecimascotaok = mensajecimascotaok, mensajecimascotaavisook = mensajecimascotaavisook, mensajeci = mensajeci, mensajeciok = mensajeciok, raza = raza, especie = especie, tabmascotaeditar= mascotaedit,  tabmascotaeditar2 = mascotaedit2, tabmascotaeditar3 = mascotaedit3, tabhistoria = historia, admin1 = admin1,  user = user, tabper = persona, tabmascota = mascotadetalle, tabadjuntos = adjuntos, fechaFinal = fechaFinal, nuevaVacuna = nuevaVacuna, mascotadetalle2 = mascotadetalle2, mascotadetalleno = mascotadetalleno, mascotadetallesi = mascotadetallesi, mascotaSi = mascotaSi, mascotaNo = mascotaNo, fechaActual = fechaActual ) 
    persona = persona2
    print(persona)
    return render_template('mascotas.html', mascotaEstrella1 = mascotaEstrella1, mascotaEstrella2 = mascotaEstrella2, disabled = disabled, mas3 = mas3, mas2 = mas2, mas = mas, mensajeaddmascotano = mensajeaddmascotano, mensajeaddmascota = mensajeaddmascota, mensajecimascotaok = mensajecimascotaok, mensajecimascotaavisook = mensajecimascotaavisook, mensajeci = mensajeci, mensajeciok = mensajeciok, raza = raza, especie = especie, tabmascotaeditar= mascotaedit,  tabmascotaeditar2 = mascotaedit2, tabmascotaeditar3 = mascotaedit3, tabhistoria = historia, admin1 = admin1,  user = user, tabper = persona, tabmascota = mascotadetalle, tabadjuntos = adjuntos, fechaFinal = fechaFinal, nuevaVacuna = nuevaVacuna, mascotadetalle2 = mascotadetalle2, mascotadetalleno = mascotadetalleno, mascotadetallesi = mascotadetallesi, mascotaSi = mascotaSi, mascotaNo = mascotaNo, fechaActual = fechaActual )
 #Recibe los datos de una mascota en particular que deben ser actualizados en la base de datos.
@app.route('/actualizar_mascota/<id>', methods=['POST',"GET"])
def actualizar_mascota(id):
    if request.method == 'POST':
        numsocio = id
        mensajeci = ""
        mensajeciok = ""
        mensajeaddmascota = ""
        mensajeaddmascotano = ""
        nombre = request.form['nombre']
        activo = request.form['activo']
        fechaNacimiento = request.form['fechaNacimiento']
        talla = request.form['talla']
        sexo = request.form['sexo']
        peso = request.form['peso']
        IDraza = request.form['raza']
        color = request.form['color']
        comentario = request.form['comentario']
        chip = request.form['chip']
        vacunaAnual = request.form['fechaVacuna']
        #IDraza = request.form['idraza']
        foto2 = request.files['foto']
        cur = mysql.connection.cursor()
        cur.execute("SELECT descripcion FROM raza WHERE IDraza = %s", (IDraza,))
        descripcionraza = cur.fetchone()
        cur.close()
        cur = mysql.connection.cursor()
        cur.execute("SELECT IDespecie FROM raza WHERE IDraza = %s", (IDraza,))
        IDespecie = cur.fetchone()
        cur.close()
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT descripcion FROM especie WHERE IDespecie = %s", (IDespecie,))
        descripcionespecie = cur.fetchone()
        cur.close()
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT IDvacuna FROM vacuna WHERE IDanimal = %s", (id,))
        vacuna = cur.fetchone()
        cur.close()

        for v in vacuna:
            IDvacuna = v
        cur = mysql.connection.cursor()
        cur.execute("""
                UPDATE animal
                SET nombre = %s,
                categoria = %s,
                talla = %s,
                sexo = %s,
                peso = %s,
                color = %s,
                fechaNacimiento = %s,
                activo = %s,
                IDraza = %s,
                descripcionraza = %s,
                descripcionespecie = %s,
                comentario = %s,
                chip = %s
                WHERE IDanimal = %s
                """, (nombre, activo, talla, sexo, peso, color, fechaNacimiento, activo, IDraza, descripcionraza, descripcionespecie, comentario, chip, id))
        mysql.connection.commit()
        
        fechaActual = date.today()
        
        fechadia = str(fechaActual.day)
        fechames = str(fechaActual.month)
        fechaanio = fechaActual.year + 1
        fechaano = str(fechaanio)
        fechaAlta = fechadia + "/" + fechames + "/" + fechaano
        fechaAltaR = fechadia + "/" + fechames + "/" + fechaano 
        siguienteVacuna = fechadia + "." + fechames + "." + fechaano 
        
        if vacunaAnual:    
            anioProximo = vacunaAnual[0:4]
            print(anioProximo)
            anioProximo2 = int(anioProximo)
            anioProximo3 = str(anioProximo2 + 1)
            mesProximo = vacunaAnual[5:7]
            diaProximo = vacunaAnual[8:10]
            vacunaProxima = diaProximo + "." + mesProximo + "." + anioProximo3
            print(vacunaProxima)
        

        if (len(vacunaAnual) != 0):
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE vacuna
                SET IDanimal = %s,
                    vacunaAnualR = %s,
                    fecha = %s,
                    IDvacuna = %s,
                    vacunaProxima = %s
                    WHERE IDanimal = %s
            """, (id, fechaAltaR, vacunaAnual, IDvacuna, vacunaProxima, id))
            mysql.connection.commit()
        
        filename = secure_filename(foto2.filename)  
         #Si cargaron foto, se guarda una copia en una carpeta local del proyecto y el nombre se actualiza en la base de datos junto a los demás datos.
        if (len(filename) !=0):
            fecha = str(datetime.now())
            fecha = fecha.replace(" ", "")
            fecha = fecha.replace("-", "")
            fecha = fecha.replace(":", "")
            fecha = fecha.replace(".", "")
            
            img = Image.open(foto2)
            foto = img.resize((256,256))
            filename = nombre + fecha + ".jpg"
            filename = nombre + fecha + ".jpg"
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            foto = filename
            cur = mysql.connection.cursor()
            cur.execute("UPDATE animal SET foto = %s WHERE IDanimal = %s", (foto,id))
            mysql.connection.commit()
        mensajecimascotaok = "Datos de mascota modificados correctamente"
        return editar_mascota(id, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano)


#Permite agregar especies y/o razas
@app.route('/add_especie_raza', methods = ['POST','GET'])
def add_especie_raza():
    msg = ''
    msg2 = ''
    if request.method == 'POST':
       especie = request.form['descripcion']
       raza = request.form['nuevaRaza'] 

       #print(id)
       per = mysql.connection.cursor()
       per.execute("SELECT r.descripcion FROM raza r WHERE r.descripcion = %s", (raza,))
       nRaza = per.fetchall()
       per.close() 
       if nRaza: 
          msg2 = 'La raza ingresada ya existe!' 
          flash('Cliente modificado correctamente')
          return redirect(url_for ("agregarEspecieRaza", msg2 = msg2))   
       else:                           
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO raza (descripcion,IDespecie) VALUES  (%s,%s)", (raza,especie))
            mysql.connection.commit()
            #cur.close()
            msg = 'La raza fue ingresada correctamente!' 
            flash('Cliente ')
            #return redirect(url_for ("agregarEspecieRaza"), msg = msg)
            return redirect(url_for('agregarEspecieRaza', msg = msg ))
            


#Toma los datos del formulario enviado desde productos.html para ingreso de nuevo producto e inserta los datos correspondientes, dando de alta un nuevo registro.
@app.route('/add_producto', methods=['POST', "GET"])
def add_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion'] 
        precio = request.form['precio']
        impuestos = request.form['iva']
        foto = request.files['foto']
        cat =  request.form['categoria']
        marca =  request.form['marca']
        precio2 = float(precio)
        impuestos2 = float(impuestos)
        iva = precio2*impuestos2/100
        precioFinal2 = precio2 + iva
        precioFinal3 = round(precioFinal2)

        filename = secure_filename(foto.filename)
        #Si no se adjunta ninguna foto, la variable pasa a tener un nombre genérico y se guarda ese dato (nombre) y todos los demás en el registro en la base de datos.
        if (len(filename) ==0):
            filename = "ninguna.jpg"
            foto = filename
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO producto (nombre, descripcion, precio, impuestos, precioFinal, iva, foto, categoria, marca) VALUES  (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (nombre, descripcion, precio, iva, precioFinal3, impuestos, foto, cat, marca))
            mysql.connection.commit()
            return redirect(url_for ("productos"))
        
        fecha = str(datetime.now())
        fecha = fecha.replace(" ", "")
        fecha = fecha.replace("-", "")
        fecha = fecha.replace(":", "")
        fecha = fecha.replace(".", "")
        print(fecha)
        filename = nombre + fecha + ".jpg"
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        foto = filename
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO producto (nombre, descripcion, precio, impuestos, precioFinal, iva, foto, categoria, marca) VALUES  (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (nombre, descripcion, precio, iva, precioFinal3, impuestos, foto, cat, marca))
        mysql.connection.commit()
        return redirect(url_for ("productos"))

#Selecciona todos los registros en la tabla producto y envia los datos a productos.html desde la variable tabproducto.
@app.route('/productos')
def productos():
    per = mysql.connection.cursor()
    per.execute("SELECT nombre, descripcion, precioFinal, IDproducto, iva, precio FROM producto WHERE IDproducto = %s", (12,))
    datossocioC = per.fetchall()
    per.close()
    per = mysql.connection.cursor()
    per.execute("SELECT nombre, descripcion, precioFinal, IDproducto, iva, precio FROM producto WHERE IDproducto = %s", (11,))
    datossocioA = per.fetchall()
    per.close()
    per = mysql.connection.cursor()
    per.execute("SELECT * FROM producto")
    productos2 = per.fetchall()
    per.close()
    return render_template('productos.html', tabproducto = productos , datossocioA = datossocioA, datossocioC = datossocioC,  admin1 = admin1,  user = user)

#Toma el ID 0 en el boton de editar en la pagina productos.html. Ese id corresponde al numero del producto en la base de datos. Trae todos los datos de los campos vinculados a ese productos y envia el resultado a productos.html por tabproductoeditar.
@app.route('/editar_producto/<id>', methods = ['POST', 'GET'])
def editar_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM producto WHERE IDproducto = %s', (id,))
    productoedit = cur.fetchall()
    cur.close()
    print (productoedit)
    return render_template('productos.html',  tabproductoeditar= productoedit,  admin1 = admin1,  user = user )

#Toma el ID 0 en el boton de editar en la pagina productos.html. Ese id corresponde al numero del producto en la base de datos,  y realiza los cambios solicitados 
@app.route('/actualizarproducto/<id>', methods=['POST'])
def actualizarproducto(id):
    if request.method == 'POST':
        #IDproducto = request.form["IDproducto"]
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        iva = request.form['iva']
        cur = mysql.connection.cursor()
        precio2 = float(precio)
        impuestos2 = float(iva)
        impuestos = precio2*impuestos2/100
        precioFinal2 = precio2 + impuestos
        precioFinal3 = round(precioFinal2)
        cur.execute("""
            UPDATE producto
            SET nombre = %s,
                descripcion = %s,
                precio = %s,
                iva = %s,
                impuestos = %s,
                precioFinal = %s
            WHERE IDproducto = %s
        """, (nombre, descripcion, precio, iva, impuestos, precioFinal3, id))
        mysql.connection.commit()
        flash('Producto modificado correctamente! Cerrar X')
        return redirect(url_for('productos'))

#Toma el ID correspondiente de la tabla producto en productos.html, lo formatea para que sea enviado a la base de datos y que elimine el campo completo.
@app.route('/eliminar_producto/<string:id>', methods = ['POST','GET'])
def eliminar_producto(id):
    print(id)
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM producto WHERE IDproducto = {0}".format(id))
    mysql.connection.commit()
    return redirect(url_for('productos'))
    
#Desde una mascota en particular se extraen algunos datos de la misma y su cliente para mostrar en consultaMedica.html, mas los datos de consultas prexistentes.
@app.route('/consulta/<id>', methods = ["POST", "GET"])
def consulta(id):
   cur = mysql.connection.cursor()
   cur.execute('SELECT m.IDclianimal, m.nombre, m.categoria, p.CIpersona, p.nombre, p.apellido, m.IDanimal, r.descripcion, e.descripcion, p.numsocio   FROM animal m RIGHT OUTER JOIN persona_cliente p ON p.CIpersonaCliente = m.IDclianimal RIGHT JOIN raza r ON r.IDraza = m.IDraza RIGHT JOIN especie e ON e.IDespecie = r.IDespecie WHERE IDanimal = %s', (id,))
   permas = cur.fetchall()
   cur.close()
   per = mysql.connection.cursor()
   per.execute("SELECT motivo, anamnesia, eog, consulta, diagnostico, pronostico, colaterales, CIpersonaVeterinario, fechaConsulta, IDanimal, diagnosticorecortado, IDconsulta FROM consulta WHERE IDanimal = %s ORDER BY  fechaConsulta DESC;", (id,) )
   historia = per.fetchall()
   per.close()
   
 #Si tiene ya registros de historia, arma un excel y almacena en una carpeta para que se pueda descargar. Si no, solo abre un excel vacio.
   if historia:
        per = mysql.connection.cursor()
        per.execute("SELECT motivo, anamnesia, eog, consulta, diagnostico, pronostico, colaterales, fechaConsulta FROM consulta WHERE IDanimal = %s ORDER BY  fechaConsulta DESC;", (id,) )
        historia2 = per.fetchall()
        per2 = pd.DataFrame(historia2)
        per2.columns=["Motivo", "Anamnnesia","EOG","Consulta","Diagnóstico", "Pronóstico", "Colaterales", "Fecha de consulta"]
        per2.reset_index (drop=True).to_excel("static/img/Consultas.xlsx", header=True, index= False)
        
   else:
        shutil.copy('static/excel/Consultas.xlsx', 'static/img')
   print(historia)
   return render_template("consultaMedica.html", tabpermas=permas, tabhistoria = historia)

@app.route('/nuevaConsulta', methods = ["POST"])
def nuevaConsulta():
   IDanimal = request.form['IDanimal']
   cur = mysql.connection.cursor()
   cur.execute('SELECT m.IDclianimal, m.nombre, m.categoria, p.CIpersona, p.nombre, p.apellido, m.IDanimal, r.descripcion, e.descripcion, p.numsocio   FROM animal m RIGHT OUTER JOIN persona_cliente p ON p.CIpersonaCliente = m.IDclianimal RIGHT JOIN raza r ON r.IDraza = m.IDraza RIGHT JOIN especie e ON e.IDespecie = r.IDespecie WHERE IDanimal = %s', (IDanimal,))
   permas = cur.fetchall()
   cur.close()
   return render_template("nuevaConsulta.html", tabpermas=permas)

#Ingresa datos en la base de datos de una nueva consulta de una mascota.
@app.route('/agregar_consulta', methods=["POST", "GET"])
def agregar_consulta():
    if request.method == 'POST':
        fechaActual = (datetime.now())
        mensajeciok = ""
        mensajeci = ""
        mensajeaddmascota = ""
        mensajecimascotaok = ""
        mensajeaddmascotano = ""
        CIpersonaveterinario = "18767665"
        motivo = request.form['motivo']
        anamnesia = request.form['anamnesia']
        eog = request.form['eog']
        eop = request.form['eop']
        tratamiento = request.form['tratamiento']
        colaterales = request.form['colaterales']
        id = request.form['id']
        vacunaAnual = request.form['vacuna']
        cur = mysql.connection.cursor()
        cur.execute('SELECT IDvacuna FROM vacuna WHERE IDanimal = %s', (id,))
        IDvac = cur.fetchone()
        for v in IDvac:
            IDvacuna = v
        global numeroMas
        numeroMas = id
        if (len(id) ==0):
            return editar_mascota(numeroMas, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano)
        
        fechadia = str(fechaActual.day)
        fechames = str(fechaActual.month)
        fechaanio = fechaActual.year + 1
        fechaano = str(fechaanio)
        fechaAlta = fechadia + "/" + fechames + "/" + fechaano
        fechaAltaR = fechadia + "/" + fechames + "/" + fechaano 
        fechaProxima = fechadia + "." + fechames + "." + fechaano 

        
        
        print(vacunaAnual)
        if vacunaAnual == "si":
            vacunaAnual = fechaActual
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE vacuna
                SET IDanimal = %s,
                    vacunaAnualR = %s,
                    fecha = %s,
                    IDvacuna = %s,
                    vacunaProxima = %s
                    WHERE IDanimal = %s
            """, (id, fechaAltaR, fechaActual, IDvacuna, fechaProxima, id))
            mysql.connection.commit()
            
        else:
            vacunaAnual = date(1111,11,11)
            fechaAltaR ="Sin registro"
            
            
            
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO consulta (CIpersonaveterinario, motivo, anamnesia, eog, pronostico, tratamiento,  colaterales, IDanimal, fechaConsulta, vacunaAnual, vacunaAnualR )  VALUES  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (CIpersonaveterinario, motivo, anamnesia, eog, eop, tratamiento, colaterales, id, fechaAlta, vacunaAnual, fechaAltaR))
        mysql.connection.commit()

        
            
        
        return editar_mascota(id, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano)
        

#selecciona desde la base los datos extraidos de una consulta médica de una mascota en particular y envia los datos a la página editarConsul.html para que se pueda editar.
@app.route('/editar_consulta', methods = ['POST'])
def editar_consulta():
    if request.method == 'POST':
        id = request.form['IDconsulta']
        cur = mysql.connection.cursor()
        cur.execute('SELECT fechaAdjunto, tituloAdjunto, adjunto, IDarchivo FROM archivos WHERE IDconsulta = %s', (id,))
        consultadj = cur.fetchall()
        cur.close()
        return render_template('editarConsul.html', tabconsultadj = consultadj)

@app.route('/editar_consulta2/<id>', methods = ['POST', 'GET'])
def editar_consulta2(id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT motivo, anamnesia, eog, consulta, diagnostico, pronostico, colaterales, CIpersonaVeterinario, fechaConsulta, IDanimal, diagnosticorecortado, IDconsulta FROM consulta  WHERE IDconsulta = %s ORDER BY fechaConsulta DESC;", (id,))
        consultaedit = cur.fetchall()
        cur.close()
        cur = mysql.connection.cursor()
        cur.execute('SELECT fechaAdjunto, tituloAdjunto, adjunto, IDarchivo FROM archivos WHERE IDconsulta = %s', (id,))
        consultadj = cur.fetchall()
        cur.close()
        print(consultaedit)
        return render_template('editarConsul.html',  tabconsultaedit = consultaedit, tabconsultaagadj = consultaedit, tabconsultadj = consultadj)

#Actualiza en la base de datos los cambios sobre una consulta medica en particular.
@app.route('/actualizar_consulta/<id>', methods=["POST", "GET"])
def actualizar_consulta(id):
    if request.method == 'POST':
        diagnostico = request.form['diagnostico']
        observaciones = request.form['observaciones']
        cur = mysql.connection.cursor()
        cur.execute("""
                UPDATE consulta
                SET diagnostico = %s,
                    observaciones = %s
                    WHERE IDconsulta = %s
            """, (diagnostico, observaciones, id))
        mysql.connection.commit()
    return editar_consulta()

#Agrega un adjunto a una consulta médica en particular.
@app.route('/agregar_adjunto', methods=["POST"])
def agregar_adjunto():
  if request.method == 'POST':
    mensajeciok = ""
    mensajeci = ""
    mensajeaddmascota = ""
    mensajecimascotaok = ""
    mensajeaddmascotano = ""
    consultanum = request.form['consultanum']
    cur = mysql.connection.cursor()
    cur.execute('SELECT IDanimal FROM consulta WHERE IDconsulta = %s', (consultanum,))
    animaladj = cur.fetchone() 
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute('SELECT cantidadAdjuntos FROM consulta WHERE IDconsulta = %s', (consultanum,))
    cantidad = cur.fetchone() 
    cur.close()
    print (cantidad)
    for i in cantidad:
        if i == 0:
            suma = 1
        else:
            suma = i + 1
    tituloadjunto = request.form["tituloadjunto"]
    archivo = request.files["archivo"]
 #Extrae el nombre del archivo y lo guarda en la base de datos. El archivo se guarda en una carpeta almacenada en el proyecto.   
    filename = secure_filename(archivo.filename)
    fecha = str(datetime.now())
    fecha = fecha.replace(" ", "")
    fecha = fecha.replace("-", "")
    fecha = fecha.replace(":", "")
    fecha = fecha.replace(".", "")
    fecha = fecha + "."
    filename = filename.replace(".", fecha)
    archivo.save(os.path.join(app.config["UPLOAD_FOLDER2"], filename))
    archivo = filename
    
    fechadia = str(fechaActual.day)
    fechames = str(fechaActual.month)
    fechaano = str(fechaActual.year)
    fechaAlta = fechadia + "/" + fechames + "/" + fechaano
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO archivos (adjunto, IDconsulta, tituloadjunto, cantidadAdjuntos, fechaAdjunto, IDanimal)  VALUES  (%s,%s,%s,%s,%s,%s)", (archivo,consultanum, tituloadjunto, suma, fechaAlta, animaladj))
    mysql.connection.commit()
    cur = mysql.connection.cursor()
    cur.execute('SELECT IDarchivo FROM archivos ORDER BY IDarchivo DESC;')
    numeroarchivo = cur.fetchone()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute("""
                UPDATE consulta
                SET cantidadAdjuntos = %s
                    WHERE IDconsulta = %s
            """, (suma, consultanum))
    #cur.execute("""UPDATE consulta SET cantidadAdjuntos = %s WHERE IDconsulta = %s""" (cantidad,id))
    mysql.connection.commit()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO consulta (IDarchivo)  VALUES  (%s)", (numeroarchivo,))
    mysql.connection.commit()
    cur = mysql.connection.cursor()
    cur.execute('SELECT IDanimal FROM consulta WHERE IDconsulta = %s', (consultanum,))
    animal = cur.fetchone()
    cur.close()
    return editar_mascota(animal, mensajeci, mensajeciok, mensajecimascotaok, mensajeaddmascota, mensajeaddmascotano)

#Elimina  un adjunto de una consulta médica.
@app.route('/eliminar_adjunto/<string:id>', methods = ['POST','GET'])
def eliminar_adjunto(id):
    print(id)
    cur = mysql.connection.cursor()
    cur.execute('SELECT IDconsulta FROM archivos WHERE IDarchivo = %s', (id,))
    idconsulta = cur.fetchone()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM archivos WHERE IDarchivo = {0}".format(id))
    mysql.connection.commit()
    return editar_consulta2(idconsulta)

#Muestra la história clínica de una mascota en particular.
@app.route('/ver_historia/<id>', methods = ["POST", "GET"])
def ver_historia(id):
    per = mysql.connection.cursor()
    per.execute("SELECT motivo, anamnesia, eog, consulta, diagnostico, pronostico, colaterales, CIpersonaVeterinario, fechaConsulta, IDanimal, diagnosticorecortado, IDconsulta FROM consulta  WHERE IDanimal = %s ORDER BY fechaConsulta DESC;", (id,))
    historia = per.fetchall()
    per.close()
    per = mysql.connection.cursor()
    per.execute("SELECT m.IDanimal, m.nombre, m.sexo, m.tipoPelo, m.color, m.talla, m.peso, m.activo, m.categoria, m.edadAlAfiliarse, m.fechaNacimiento, r.IDraza, r.descripcion, e.descripcion, m.foto FROM animal m  RIGHT OUTER JOIN raza r ON r.IDraza = m.IDraza RIGHT JOIN especie e ON r.IDespecie = e.IDespecie WHERE IDanimal = %s", (id,))
    mascota = per.fetchone()
    per.close()
#Si hay al menos un registro crea un archivo excel y lo almacena en una carpeta del proyecto permitiendo su descarga desde la página. Si no abre en su lugar un excel vacío.  
    if historia:
        per = mysql.connection.cursor()
        per.execute("SELECT motivo, anamnesia, eog, consulta, diagnostico, pronostico, colaterales, fechaConsulta FROM consulta WHERE IDanimal = %s ORDER BY  fechaConsulta DESC;", (id,) )
        historia2 = per.fetchall()
        per2 = pd.DataFrame(historia2)
        per2.columns=["Motivo", "Anamnnesia","EOG","Consulta","Diagnóstico", "Pronóstico", "Colaterales", "Fecha de consulta"]
        per2.reset_index (drop=True).to_excel("static/img/Consultas.xlsx", header=True, index= False)
        
        
    else:
        shutil.copy('static/excel/Consultas.xlsx', 'static/img')
    return render_template('consultaMedica.html', tabhistoria = historia, tabmascota = mascota,  tabper = persona)

@app.route('/ver_consulta/<id>', methods = ["POST", "GET"])
def ver_consulta(id):
    
    per = mysql.connection.cursor()
    per.execute("SELECT motivo, anamnesia, eog, consulta, tratamiento, pronostico, colaterales, CIpersonaVeterinario, fechaConsulta, IDanimal, diagnosticorecortado, IDconsulta, cantidadAdjuntos FROM consulta WHERE IDconsulta = %s ORDER BY IDconsulta DESC;", (id,))
    historiaConsulta = per.fetchall()
    per.close()
    
    per = mysql.connection.cursor()
    per.execute("SELECT adjunto, fechaAdjunto, tituloAdjunto FROM archivos WHERE IDconsulta = %s ORDER BY IDconsulta DESC;", (id,))
    adjuntosConsulta = per.fetchall()
    per.close()
    return render_template("consultaMedica.html", historiaConsulta = historiaConsulta, adjuntosConsulta = adjuntosConsulta)

#Busca un adjunto por su nombre en la carpeta que los almacena para poder abrirlo.
@app.route('/buscar_adjunto/<id>', methods=["POST", "GET"])
def buscar_adjunto(id):
    ruta_archivo = 'static/Adjuntos/' + id
    print(ruta_archivo)
    if os.path.isfile(ruta_archivo):
     print(ruta_archivo)
     return send_file(ruta_archivo, attachment_filename= id)

#Vacia el cache de las páginas del programa para que refresque continuamente los cambios
@app.route('/profile/details', methods=['GET', 'POST'])
def profile_details():
    response = make_response(render_template('mascotas.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    return response

if __name__ == "__main__":
    app.run( port=3000, debug=True )
    

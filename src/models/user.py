
from sqlite3 import Cursor
from src.config.db import db
from email import message
from http import server
from smtplib import SMTP
from email.message import EmailMessage
from src.config import settings


class UsuarioModel():
   
    """ def crearUser(serlf,usuario,correo,claveEncritada,validate_mail,vali_url):
        cursor =db.cursor()
        cursor.execute('insert into usuario(nombre,correo,password,validate_mail,vali_url) values(%s,%s,%s,%s,%s)', (
            usuario,
            correo,
            claveEncritada,
            validate_mail,
            vali_url,

            ))       
        cursor.close()   """
    def validarUser(self,usuario):
        cursor =db.cursor()
        cursor.execute('select correo, password from usuario where validate_mail= "true" and usuario.correo = %s',(usuario,))      
        usuario = cursor.fetchall()
        cursor.close()
        return usuario

def createUser(name,email,claveEncritada,validate_mail,vali_url):
    cursor = db.cursor()
    cursor.execute("insert into usuario (nombre,correo,password,validate_mail,vali_url) values(%s,%s,%s,%s,%s)", (
        name,
        email,
        claveEncritada,
        validate_mail,
        vali_url,

    ))
    cursor.close()



def valiCorreo(valimail,content):

    message = EmailMessage()

    message['subject'] = 'Correo de validacion'
    message['from'] = 'kiragod@gmail.com'
    message['To'] = valimail
    message.set_content(content)

    username = settings.SMPT_USERNAME
    password = settings.SMPT_PASSWORD

    server = SMTP(settings.SMPT_HOSTNAME)
    server.starttls()
    server.login(username, password)
    server.send_message(message)

    server.quit()
    
def UsuarioValidado(validate_mail, vali_url):
    cursor = db.cursor()
    
    cursor.execute('UPDATE usuario SET validate_mail = "true", vali_url = "" WHERE validate_mail="'+validate_mail+'" AND vali_url="'+vali_url+'"')

    cursor.close()
def UserVal(validate_mail,vali_url):
    cursor = db.cursor(dictionary= True)
    cursor.execute('select * from usuario where validate_mail="'+validate_mail+'" AND vali_url = "'+vali_url+'"')

    userv = cursor.fetchall()
    cursor.close()
    return userv



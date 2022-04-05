from pickle import FALSE
from flask import render_template, request, redirect, url_for, jsonify, flash, session
from src import app
from src.models.user import UsuarioModel
from src.models import user

import random ,string
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import re

@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['comment']:
        return redirect(url_for("login"))
    


@app.route("/usuario/create", methods =['POST','GET'])
def createUser():
     if request.method ==  'POST':
                usuarioModel = UsuarioModel()
                name=request.form.get('usuario')
                email=request.form.get('email')
                password=request.form.get('password')
                encriptar= generate_password_hash(password)                 
                isValid=True

                lenpass =  len(password)
                minuscula = False
                mayuscula= False
                numeros = False
                special = False
                valimail = False

                if  usuarioModel.validarUser(usuario=email):
                        isValid = False
                        flash("El correo ya existe")
                else:
                        isValid=True
                        print("Correo valido")
                  
                if name == "":
                        flash("Nombre Obligatorio")
                        isValid=False        
                if email == "":
                        flash("Correo Obligatorio")   
                        isValid=False    
                if re.search('[@]',email):
                        valimail= True
                if valimail == False:
                        flash("Correo no valido (@)")                                  
               
                if password == "":
                        flash("Contraseña Obligatoria")  
                        isValid=False  
                if lenpass < 8 :                       
                        flash("La contraseña debe tener minimo 8 caracteres")                       
                        isValid=False 
               
                
                for caracter in password:
                        if caracter.islower() == True:  
                               minuscula = True
                        if caracter.isupper()== True:
                                mayuscula= True
                        if caracter.isdigit()==True:
                                numeros= True                   
                                                             
                if mayuscula == False:
                        isValid=False
                        flash("Ingrese al menos una Mayusculas a la contraseña")
                        
                if minuscula == False:
                        isValid=False
                        flash("Ingrese al menos una minuscula a la contraseña")
                
                if numeros == False:
                        isValid=False
                        flash("Ingrese al menos un Número a la contraseña")
                
                if re.search('[@_!#$%^&*()<>?/\|}{~:]',password):                        
                        special= True
                       
                if special == False:
                        isValid=False
                        flash("Ingrese al menos un caracter a la contraseña")

                if isValid==False:
                        return render_template("user/crearUser.html",name=name,email=email,password=password)
        
                user.createUser(name=name,email=email,claveEncritada=encriptar)                 
                return redirect(url_for("login"))
     else:
                return render_template ("user/crearUser.html")
    

@app.route("/" ,methods =['POST','GET'])
def login():
    usuarioModel = UsuarioModel()
    if request.method == "GET":
        return render_template("auth/login.html")
    else:
        usuario = request.form['email']
        password = request.form['password']
        user = usuarioModel.validarUser(usuario)
        result = validardateuser(user,password)
        
        if user is not None and result==True:
            print("Welcome")
            
            session['username'] = usuario
            return redirect(url_for("home"))
        else:
            flash("Correo / Password incorrect")
            return redirect(url_for("login"))
            
def validardateuser(users,password):
    for user in users:
        return check_password_hash(user[1],password)

@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username')
        print("salir")
    return redirect(url_for("login"))



@app.route("/home")
def home():
    return render_template ("home/home.html")

@app.route("/validarcorreo")
def valco():
        return ("Validando correo")
    

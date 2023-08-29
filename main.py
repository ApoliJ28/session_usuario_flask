from flask import Flask, redirect, request, url_for, render_template, flash, session
from werkzeug.security import check_password_hash as checkph
from werkzeug.security import generate_password_hash as generateph

import bbdd
app = Flask(__name__)
app.secret_key = 'miclavesecreta'

@app.before_request
def antes_de_todo():
    ruta = request.path
    if not 'usuario' in session and ruta != "/entrar" and ruta != "/login" and ruta != "/registro" and ruta != "/registrar":
        flash("Inicia session para continuar")
        return redirect(url_for('entrar'))

@app.route("/dentro")
def dentro():
    return render_template('index.html')

@app.route("/")
@app.route("/entrar")
def entrar():
    return render_template("entrar.html")

@app.route("/login", methods= ["POST"])
def login():
    email = request.form['email']
    clave = request.form['clave']
    try:
        usuario = bbdd.get_usuario(email)
    except Exception as e:
        flash("Error al obtener el usuario")
    if usuario:
        if(checkph(usuario[2], clave)):
            session['usuario'] = email
            return redirect('/dentro')
    else:
        flash("Acceso denegado")
        return redirect("/entrar")
    
    return redirect("/entrar")

@app.route("/salir")
def salir():
    session.pop("usuario", None)
    flash("Session cerrada")
    return redirect("/entrar")

@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route("/registrar", methods = ['POST'])
def registrar():
    email = request.form['email']
    clave = request.form['clave']
    clave = generateph(clave)
    try:
        bbdd.alta_usuario(email, clave)
        flash("Usuario registrado")
    except Exception as e:
        flash(f"error al registrar el usuario, error: {e}")
    finally:
        return redirect("/entrar")

if __name__ == '__main__':
    app.run(debug= True, port=3031)

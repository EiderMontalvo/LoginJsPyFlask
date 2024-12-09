from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from datetime import datetime
from functools import wraps
import time
import hashlib

class Usuario:
    def __init__(self, NombreCompleto, CorreoElectronico, Contrasena):
        self.NombreCompleto = NombreCompleto
        self.CorreoElectronico = CorreoElectronico
        self.Contrasena = self._HashContrasena(Contrasena)
        self.FechaRegistro = datetime.now()

    def _HashContrasena(self, Contrasena):
        return hashlib.sha256(Contrasena.encode()).hexdigest()

    def ValidarContrasena(self, Contrasena):
        return self.Contrasena == self._HashContrasena(Contrasena)

class GestorUsuarios:
    def __init__(self):
        self.Usuarios = []

    def AgregarUsuario(self, NombreCompleto, CorreoElectronico, Contrasena):
        if not self.BuscarPorCorreo(CorreoElectronico):
            NuevoUsuario = Usuario(NombreCompleto, CorreoElectronico, Contrasena)
            self.Usuarios.append(NuevoUsuario)
            return True
        return False

    def BuscarPorCorreo(self, CorreoElectronico):
        return next((usuario for usuario in self.Usuarios 
                    if usuario.CorreoElectronico.lower() == CorreoElectronico.lower()), None)

    def ValidarCredenciales(self, CorreoElectronico, Contrasena):
        Usuario = self.BuscarPorCorreo(CorreoElectronico)
        return Usuario if Usuario and Usuario.ValidarContrasena(Contrasena) else None

app = Flask(__name__)
app.secret_key = 'ClaveSecretaParaLaSesion2024'
GestorDeUsuarios = GestorUsuarios()

def RequiereAutenticacion(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'CorreoElectronico' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def inicio():
    if 'CorreoElectronico' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'CorreoElectronico' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        if not request.is_json:
            return jsonify({
                'Exitoso': False,
                'Mensaje': 'Se requiere JSON'
            }), 400

        DatosRecibidos = request.get_json()
        CorreoElectronico = DatosRecibidos.get('CorreoElectronico', '').strip()
        Contrasena = DatosRecibidos.get('Contrasena', '').strip()

        if not CorreoElectronico or not Contrasena:
            return jsonify({
                'Exitoso': False,
                'Mensaje': 'Por favor, complete todos los campos'
            }), 400

        if not GestorDeUsuarios.Usuarios:
            return jsonify({
                'Exitoso': False,
                'Mensaje': 'Debe registrarse primero'
            }), 401

        UsuarioEncontrado = GestorDeUsuarios.ValidarCredenciales(CorreoElectronico, Contrasena)
        
        if UsuarioEncontrado:
            session['CorreoElectronico'] = CorreoElectronico
            session.permanent = True
            return jsonify({
                'Exitoso': True,
                'Mensaje': f'¡Bienvenido {UsuarioEncontrado.NombreCompleto}!',
                'Redireccion': url_for('dashboard')
            })

        return jsonify({
            'Exitoso': False,
            'Mensaje': 'Correo electrónico o contraseña incorrectos'
        }), 401

    return render_template('login.html')

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if 'CorreoElectronico' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        if not request.is_json:
            return jsonify({
                'Exitoso': False,
                'Mensaje': 'Se requiere JSON'
            }), 400

        DatosRecibidos = request.get_json()
        NombreCompleto = DatosRecibidos.get('NombreCompleto', '').strip()
        CorreoElectronico = DatosRecibidos.get('CorreoElectronico', '').strip()
        Contrasena = DatosRecibidos.get('Contrasena', '').strip()

        if not all([NombreCompleto, CorreoElectronico, Contrasena]):
            return jsonify({
                'Exitoso': False,
                'Mensaje': 'Todos los campos son requeridos'
            }), 400

        if len(Contrasena) < 6:
            return jsonify({
                'Exitoso': False,
                'Mensaje': 'La contraseña debe tener al menos 6 caracteres'
            }), 400

        if GestorDeUsuarios.BuscarPorCorreo(CorreoElectronico):
            return jsonify({
                'Exitoso': False,
                'Mensaje': 'El correo electrónico ya está registrado'
            }), 400

        if GestorDeUsuarios.AgregarUsuario(NombreCompleto, CorreoElectronico, Contrasena):
            return jsonify({
                'Exitoso': True,
                'Mensaje': '¡Registro exitoso!',
                'Redireccion': url_for('login')
            })
        
        return jsonify({
            'Exitoso': False,
            'Mensaje': 'Error al registrar el usuario'
        }), 500

    return render_template('registrar.html')

@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if 'CorreoElectronico' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        if not request.is_json:
            return jsonify({
                'Exitoso': False,
                'Mensaje': 'Se requiere JSON'
            }), 400

        DatosRecibidos = request.get_json()
        CorreoElectronico = DatosRecibidos.get('CorreoElectronico', '').strip()

        if not CorreoElectronico:
            return jsonify({
                'Exitoso': False,
                'Mensaje': 'El correo electrónico es requerido'
            }), 400

        time.sleep(1)
        
        return jsonify({
            'Exitoso': True,
            'Mensaje': 'Si el correo existe, recibirás instrucciones para recuperar tu contraseña',
            'Redireccion': url_for('login')
        })

    return render_template('recuperar.html')

@app.route('/dashboard')
@RequiereAutenticacion
def dashboard():
    Usuario = GestorDeUsuarios.BuscarPorCorreo(session['CorreoElectronico'])
    if not Usuario:
        session.clear()
        return redirect(url_for('login'))
        
    return render_template('dashboard.html', Usuario=Usuario)

@app.route('/cerrar-sesion')
def cerrar_sesion():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
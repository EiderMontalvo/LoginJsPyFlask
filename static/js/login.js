document.addEventListener('DOMContentLoaded', function() {
    const FormularioLogin = document.getElementById('FormularioLogin');
    const BotonLogin = document.getElementById('BotonLogin');
    const MostrarContrasena = document.getElementById('MostrarContrasena');
    const CampoContrasena = document.getElementById('Contrasena');

    MostrarContrasena.addEventListener('change', function() {
        CampoContrasena.type = this.checked ? 'text' : 'password';
    });

    FormularioLogin.addEventListener('submit', async function(e) {
        e.preventDefault();
        BotonLogin.disabled = true;

        try {
            const DatosFormulario = {
                CorreoElectronico: FormularioLogin.CorreoElectronico.value.trim(),
                Contrasena: FormularioLogin.Contrasena.value.trim()
            };

            if (!DatosFormulario.CorreoElectronico || !DatosFormulario.Contrasena) {
                throw new Error('Por favor, complete todos los campos');
            }

            const Respuesta = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(DatosFormulario)
            });

            const Datos = await Respuesta.json();

            if (!Respuesta.ok) throw new Error(Datos.Mensaje || 'Error en el inicio de sesión');

            await Swal.fire({
                icon: 'success',
                title: '¡Éxito!',
                text: Datos.Mensaje,
                timer: 2000,
                showConfirmButton: false
            });

            window.location.href = Datos.Redireccion;

        } catch (error) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: error.message
            });
        } finally {
            BotonLogin.disabled = false;
        }
    });
});
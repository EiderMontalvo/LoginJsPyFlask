document.addEventListener('DOMContentLoaded', function() {
    const FormularioRegistro = document.getElementById('FormularioRegistro');
    const BotonRegistro = document.getElementById('BotonRegistro');
    const MostrarContrasena = document.getElementById('MostrarContrasena');
    const CampoContrasena = document.getElementById('Contrasena');

    MostrarContrasena.addEventListener('change', function() {
        CampoContrasena.type = this.checked ? 'text' : 'password';
    });

    FormularioRegistro.addEventListener('submit', async function(e) {
        e.preventDefault();
        BotonRegistro.disabled = true;

        try {
            const DatosFormulario = {
                NombreCompleto: FormularioRegistro.NombreCompleto.value.trim(),
                CorreoElectronico: FormularioRegistro.CorreoElectronico.value.trim(),
                Contrasena: FormularioRegistro.Contrasena.value.trim()
            };
            if (!DatosFormulario.NombreCompleto) {
                throw new Error('El nombre completo es requerido');
            }

            if (!DatosFormulario.CorreoElectronico) {
                throw new Error('El correo electrónico es requerido');
            }

            if (!DatosFormulario.CorreoElectronico.includes('@')) {
                throw new Error('Ingrese un correo electrónico válido');
            }

            if (DatosFormulario.Contrasena.length < 6) {
                throw new Error('La contraseña debe tener al menos 6 caracteres');
            }

            const Respuesta = await fetch('/registrar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(DatosFormulario)
            });

            const Datos = await Respuesta.json();

            if (!Respuesta.ok) throw new Error(Datos.Mensaje || 'Error en el registro');

            await Swal.fire({
                icon: 'success',
                title: '¡Registro Exitoso!',
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
            BotonRegistro.disabled = false;
        }
    });
});
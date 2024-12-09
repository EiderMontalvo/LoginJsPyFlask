document.addEventListener('DOMContentLoaded', function() {
    const FormularioRecuperar = document.getElementById('FormularioRecuperar');
    const BotonRecuperar = document.getElementById('BotonRecuperar');

    FormularioRecuperar.addEventListener('submit', async function(e) {
        e.preventDefault();
        BotonRecuperar.disabled = true;

        try {
            const CorreoElectronico = FormularioRecuperar.CorreoElectronico.value.trim();

            if (!CorreoElectronico) {
                throw new Error('El correo electrónico es requerido');
            }

            if (!CorreoElectronico.includes('@')) {
                throw new Error('Ingrese un correo electrónico válido');
            }

            const Respuesta = await fetch('/recuperar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ CorreoElectronico })
            });

            const Datos = await Respuesta.json();

            if (!Respuesta.ok) throw new Error(Datos.Mensaje);
            const UsuarioSimulado = {
                correo: CorreoElectronico,
                contrasena: '******'
            };

            await Swal.fire({
                icon: 'info',
                title: 'Información de Cuenta',
                html: `
                    <div style="text-align: left; margin: 20px;">
                        <p><strong>Correo:</strong> ${UsuarioSimulado.correo}</p>
                        <p><strong>Contraseña:</strong> ${UsuarioSimulado.contrasena}</p>
                    </div>
                `,
                confirmButtonText: 'Entendido'
            });

            window.location.href = Datos.Redireccion;

        } catch (error) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: error.message
            });
        } finally {
            BotonRecuperar.disabled = false;
        }
    });
});
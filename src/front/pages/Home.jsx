
export const Home = () => {
	return (
		<div className="container home-container">
			<div className="row">
				<div className="col-12 text-center vh-100 d-flex flex-column justify-content-center align-items-center">
					<h1>Este es mi página de inicio</h1>
					<p>
						Lorem ipsum, dolor sit amet consectetur adipisicing elit. Deleniti vel illum dignissimos accusantium! Accusamus minus aspernatur illum dolores aliquam, sed repellendus atque eveniet quam maiores possimus, cum numquam velit qui!
					</p>
				</div>
			</div>
		</div>
	);
};




/*

	1.- Protejer las rutas, Todos <--- este componente
	2.- Método para eviar correos 
	3.- recuperar contraseña
	4.- Integrar el avatar (Integrar con cloudinary)
	5.- Eliminar el input del avatar (al guaradar user)
	6.- Crear la sesión de perfil tal como lo pide el diseño
	7.- Al registrar usuario enviar correo de activación
	8.- Usar dos contraseñas para validar que sean iguales
	9.- Cerrar sesión
	10.- Eliminar los token de sesión cerrada

*/
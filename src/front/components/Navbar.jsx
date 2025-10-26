import { Link, NavLink } from "react-router-dom";
import useGlobalReducer from "../hooks/useGlobalReducer";

export const Navbar = () => {
	const { store, dispatch } = useGlobalReducer();

	return (
		<nav className="navbar navbar-expand-sm navbar-dark bg-dark navbar-custom">
			<div className="container-fluid">
				<Link className="navbar-brand" to="/">Todo's</Link>
				<button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
					<span className="navbar-toggler-icon"></span>
				</button>
				<div className="collapse navbar-collapse" id="navbarNav">
					<ul className="navbar-nav ms-auto navbar-ul">
						<li className="nav-item">
							<NavLink className={({ isActive }) => isActive ? "bordered" : ""} aria-current="page" to="/">Inicio</NavLink>
						</li>
						<li className="nav-item">
							<NavLink className={({ isActive }) => isActive ? "bordered" : ""} to="/tasks">Lista de tareas</NavLink>
						</li>
					</ul>
					{
						store.token ? (
							<div className="mb-3 mb-sm-0">
								{/* <NavLink className={({ isActive }) => isActive ? "bordered" : ""} to="/logout">Cerrar sesión</NavLink> */}
								<button className="btn btn-outline-light me-3">Cerrar sesión</button>
							</div>
						) :
							(<div className="mb-3 mb-sm-0">
								{/* <NavLink className={({ isActive }) => isActive ? "bordered" : ""} to="/login">Iniciar sesión</NavLink> */}
								<NavLink
									to={`/login`}

									className={({ isActive }) => isActive ? "btn btn-outline-light me-3 bordered d-none" : "btn btn-outline-light me-3"}
								>
									Iniciar sesión
								</NavLink>
							</div>)
					}
					{
						store.token ? (
							<div className="profile-pic-navbar">
								<img src="https://i.pravatar.cc/300" alt="Profile" className="profile-pic-img-navbar" />
							</div>) : null
					}

				</div>
			</div>
		</nav>
	);
};
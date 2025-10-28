import { useState, useRef } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Toaster, toast } from 'sonner';

const initialUserState = {
    lastname: "",
    email: "",
    avatar: null,
    password: ""
}

const Register = () => {
    const [user, setUser] = useState(initialUserState);
    const fileInputRef = useRef(null);
    const navigate = useNavigate();

    const handleChange = (event) => {
        const { name, value } = event.target;
        setUser({ ...user, [name]: value });
    };

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        setUser({ ...user, avatar: file });
    }

    const handleSubmit = async (event) => {
        event.preventDefault();
        // Aquí puedes manejar el envío del formulario, por ejemplo, enviando los datos a un servidor
        const url = import.meta.env.VITE_BACKEND_URL;

        const response = await fetch(`${url}/register`, {
            method: 'POST',
            body: JSON.stringify(user),
            headers: {
                'Content-Type': 'application/json'
            }
        });


        const data = await response.json();
        if (response.ok) {
            setUser(initialUserState);
            fileInputRef.current.value = null;

            toast.success('Usuario registrado con éxito')
            setTimeout(() => {
                navigate('/login');
            }, 1500);

        } else {
            toast.error(`${data.message}`);
            // Aquí puedes manejar errores, mostrar mensajes, etc.
        }
    }


    return (
        <div className="container">
            <div className="vh-100 d-flex flex-column justify-content-center home-container">
                <div className="row justify-content-center my-5 p-4">
                    <h2 className="text-center my-3">Registrarse en nuestra plataforma :)</h2>
                    <div className="col-12 col-md-6 border py-4">
                        <form
                            onSubmit={handleSubmit}
                        >
                            <div className="form-group mb-3">
                                <label htmlFor="txtLastname">Nombre completo:</label>
                                <input
                                    type="text"
                                    placeholder="Jhon Doe"
                                    className="form-control"
                                    id="txtLastname"
                                    name="lastname"
                                    value={user.lastname}
                                    onChange={handleChange}
                                />
                            </div>

                            <div className="form-group mb-3">
                                <label htmlFor="txtEmail">Correo:</label>
                                <input
                                    type="text"
                                    placeholder="elmero@gmail.com"
                                    className="form-control"
                                    id="txtEmail"
                                    name="email"
                                    value={user.email}
                                    onChange={handleChange}
                                />
                            </div>


                            <div className="form-group mb-3">
                                <label htmlFor="txtAvatar">Avatar:</label>
                                <input
                                    type="file"
                                    placeholder="elmero@gmail.com"
                                    className="form-control"
                                    id="txtAvatar"
                                    name="avatar"
                                    ref={fileInputRef}
                                    onChange={handleFileChange}
                                />
                            </div>


                            <div className="form-group mb-3">
                                <label htmlFor="btnPassword">Contraseña:</label>
                                <input
                                    type="password"
                                    placeholder="elmero@gmail.com"
                                    className="form-control"
                                    id="btnPassword"
                                    name="password"
                                    value={user.password}
                                    onChange={handleChange}
                                />
                            </div>
                            <button className="btn btn-outline-primary w-100">Inicia sesión</button>
                        </form>
                    </div>

                    <div className="w-100"></div>
                    <Toaster position="top-right" />

                    {/* <br/> */}

                    <div className="col-12 col-md-6 d-flex justify-content-between my-1">
                        <Link to={"/login"}>Ya tengo una cuenta</Link>
                    </div>
                </div>
            </div>
        </div>
    );
}
export default Register;

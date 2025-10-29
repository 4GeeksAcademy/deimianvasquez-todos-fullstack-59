import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom"
import { Toaster, toast } from 'sonner';
import useGlobalReducer from "../hooks/useGlobalReducer";

const BASE_URL = import.meta.env.VITE_BACKEND_URL

const initialUserState = {
    email: "",
    password: ""
}

const Login = () => {

    const [user, setUser] = useState(initialUserState);
    const { dispatch } = useGlobalReducer();

    const navigate = useNavigate();


    const handleChange = ({ target }) => {
        const { name, value } = target;
        setUser({
            ...user,
            [name]: value
        });
    }

    const handleSubmit = async (event) => {
        event.preventDefault();

        const response = await fetch(`${BASE_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(user)


        });
        const data = await response.json();
        console.log(data);

        if (response.ok) {
            toast.success('Usuario registrado con éxito')
            dispatch({
                type: "SET_TOKEN",
                payload: data.token,
            });
            const responseUser = await fetch(`${BASE_URL}/me`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${data.token}`
                }
            });
            const dataUser = await responseUser.json();
            console.log(dataUser);

            dispatch({
                type: "SET_USER",
                payload: dataUser,
            });

            localStorage.setItem("token", data.token);
            localStorage.setItem("user", JSON.stringify(dataUser));

            setTimeout(() => {
                navigate('/');
            }, 1500);
        }
    }

    return (
        <div className="container vh-100 d-flex flex-column justify-content-center home-container">
            <div className="row justify-content-center">
                <h2 className="text-center my-3">Ingresa en nuestra plataforma :)</h2>
                <Toaster position="top-right" />
                <div className="col-12 col-md-6 border py-4">
                    <form
                        onSubmit={handleSubmit}
                    >
                        <div className="form-group mb-3">
                            <label htmlFor="btnEmail">Correo:</label>
                            <input
                                type="text"
                                placeholder="elmero@gmail.com"
                                className="form-control"
                                id="btnEmail"
                                name="email"
                                value={user.email}
                                onChange={handleChange}
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

                {/* <br/> */}

                <div className="col-12 col-md-6 d-flex justify-content-between my-1">
                    <Link to={"/register"}>Registrarme</Link>
                    <Link to={"/recovery-password"}>Olvido su contraseña</Link>
                </div>
            </div>
        </div>

    );

};

export default Login;
import React from "react";
import { Navigate } from "react-router-dom";
import useGlobalReducer from "../hooks/useGlobalReducer";

// Protege rutas comprobando store.token.
// Uso: <ProtectedRoute><MiComponente/></ProtectedRoute>
const ProtectedRoute = ({ children }) => {
    const { store } = useGlobalReducer();

    // Si no hay token, redirige a /login
    if (!store || !store.token) {
        return <Navigate to="/login" replace />;
    }

    return children;
};

export default ProtectedRoute;
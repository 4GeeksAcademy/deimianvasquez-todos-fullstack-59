import React from "react";

const Tasks = () => {
    return (
        <div className="container mt-4">
            <h1>Lista de tareas</h1>
            <p>Esta es la página protegida de tareas. Aquí podrás ver y gestionar tus tareas.</p>
            {/* Aquí montarás el componente que consuma /api/todos */}
        </div>
    );
};

export default Tasks;
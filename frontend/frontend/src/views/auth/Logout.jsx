import { logout } from "../../utils/auth"; 
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

function Logout() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('token');
        logout();
        setIsAuthenticated(false);
        // navigate('/login');
    }, []);

    return (
        !isAuthenticated && (
        <div className="alert alert-success w-50 text-center ">
            Logout successful!
            <div className="mt-3 ">
                <button className="btn btn-primary me-2" onClick={() => navigate('/')}>Home</button>
                <button className="btn btn-secondary" onClick={() => navigate('/login')}>Login</button>
            </div>
        </div>
        )
    );
}

export default Logout;
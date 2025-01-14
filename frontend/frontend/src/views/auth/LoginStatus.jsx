import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Cookies from 'js-cookie'; 

const LoginStatus = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const navigate = useNavigate();

    const checkAuthentication = () => {
        const access_token = Cookies.get('access_token');
        const refresh_token = Cookies.get('refresh_token');

        if (access_token || refresh_token) {
            setIsAuthenticated(true);
        } else {
            setIsAuthenticated(false);
        }
    };

    useEffect(() => {
        checkAuthentication();
        const interval = setInterval(checkAuthentication, 500); // Check every 500ms
        return () => clearInterval(interval);
    }, []);

    const handleClick = () => {
      if (isAuthenticated) {
        console.log('Logging out');
        setIsAuthenticated(false);
        navigate('/logout');
      } else {
        console.log('Navigating to login');
        navigate('/login');
      }
    };

    return (
      <button 
        onClick={handleClick} 
        className={`btn ${isAuthenticated ? "btn-danger" : "btn-primary"}`}>
        {isAuthenticated ? "Logout" : "Login"}
      </button>
    );
};

export default LoginStatus;

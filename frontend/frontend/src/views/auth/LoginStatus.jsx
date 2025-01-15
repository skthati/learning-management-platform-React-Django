import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Cookies from 'js-cookie'; 
import isAuthenticated from "./IsAuthenticated";

const LoginStatus = ({ user }) => {
    const [authenticationStatus, setAuthenticationStatus] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const interval = setInterval(setAuthenticationStatus(isAuthenticated()), 500); // Check every 500ms
        return () => clearInterval(interval); // Cleanup
    }, []);
    
    const handleClick = () => {
      if (authenticationStatus) {
        console.log('Logging out');
        setAuthenticationStatus(false);
        navigate('/logout');
      } else {
        console.log('Navigating to login');
        navigate('/login');
      }
    };

    return (
      <button 
        onClick={handleClick} 
        className={`btn ${authenticationStatus ? "btn-danger" : "btn-primary"}`}>
        {authenticationStatus ? "Logout" : "Login"}
      </button>
    );
};

export default LoginStatus;

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const getCookieValue = (cookieName) => {
  const cookies = document.cookie.split('; ');
  const cookie = cookies.find((c) => c.startsWith(`${cookieName}=`));
  return cookie ? cookie.split('=')[1] : null;
};

const LoginStatus = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = getCookieValue('access_token');
    console.log('Token from cookies:', token);
    setIsAuthenticated(Boolean(token));
  }, []);

  const handleClick = () => {
    if (isAuthenticated) {
      console.log('Logging out');
      document.cookie = 'access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'; // Delete the cookie
      setIsAuthenticated(false);
      navigate('/login');
    } else {
      console.log('Navigating to login');
      navigate('/login');
    }
  };

  return (
    <button onClick={handleClick} className="btn btn-primary">
      {isAuthenticated ? "Logout" : "Login"}
    </button>
  );
};

export default LoginStatus;

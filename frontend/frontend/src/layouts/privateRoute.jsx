import { Navigate } from 'react-router-dom';
import { useAuthStore } from '../store/auth';

const PrivateRoute = ({ element }) => {
    const isLoggedIn = useAuthStore((state) => state.isLoggedIn());

    return isLoggedIn ? element : <Navigate to="/" replace />;
};

export default PrivateRoute;



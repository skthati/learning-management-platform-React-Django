import { navigate } from 'react-router-dom';
import { useAuthStore } from '../store/auth';

const PrivateRoute = ({ children }) => {
    const isLoggedIn = useAuthStore((state) => state.isLoggedIn)();

    return isLoggedIn ? <> children </> : <> <navigate to = "/login/"></navigate></>;
}

export default PrivateRoute;


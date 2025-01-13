import { useState, useEffect } from 'react';
import { setUser } from '../utils/auth';

const MainWrapper = ({ children }) => {
    const [loading, setLoading] = useState(true); // Track loading state
    const [error, setError] = useState(null); // Track errors

    useEffect(() => {
        const handler = async () => {
            try {
                await setUser(); // Execute the user setup
                setLoading(false); // Mark loading as complete
            } catch (err) {
                setError(err.message); // Capture any errors
                setLoading(false); // Ensure loading state is cleared even on error
            }
        };
        handler();
    }, []);

    if (loading) {
        return <div>Loading...</div>; // Placeholder during loading
    }

    if (error) {
        return <div>Error: {error}</div>; // Display error if something goes wrong
    }

    return <>{children}</>; // Render children once ready
};

export default MainWrapper;


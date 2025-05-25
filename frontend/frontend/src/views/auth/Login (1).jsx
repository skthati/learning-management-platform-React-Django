import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import apiInstance from "../../utils/axios";
import { login } from "../../utils/auth";
import IsAuthenticated from "./IsAuthenticated";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [authenticationStatus, setAuthenticationStatus] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Reset error state when the component mounts
    setAuthenticationStatus(IsAuthenticated());
    setError("");
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await login(email, password);
      console.log(response);
      setLoading(false);
      setSuccess(true);
      navigate("/"); // Redirect to dashboard or any other page after successful login
    } catch (err) {
      setLoading(false);
      setError(err.response.data?.detail || "Invalid email or password");
      
    } 
  };

  return (
    <div className="container mt-5">
      <h1 className="text-center mb-4">Login</h1>
      {error && <div className="alert alert-danger">{error}</div>}
      {success && <div className="alert alert-success">Login successful</div>}
      {authenticationStatus ? <div className="alert alert-info">You are already logged in</div> : <div className="alert alert-info">You are not logged in</div>} 
      <form onSubmit={handleSubmit} className="mx-auto" style={{ maxWidth: '600px' }}>
        <div className="mb-3">
          <label htmlFor="email" className="form-label">Email:</label>
          <input
            type="email"
            className="form-control"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">Password:</label>
          <input
            type="password"
            className="form-control"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary w-100" disabled={loading}>
          {loading ? <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> : "Login"}
        </button>
      </form>
      <div className="text-center mt-3">
        <Link to="/register">Don't have an account? Register</Link>
      </div>
    </div>
  );
}

export default Login;
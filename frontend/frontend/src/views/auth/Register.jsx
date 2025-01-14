import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import apiInstance from "../../utils/axios";
import { register } from "../../utils/auth";

function Register() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirmation, setPasswordConfirmation] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  console.log(fullName)

  useEffect(() => {
    // Reset error state when the component mounts
    setError("");
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    setSuccess(false);

    if (password !== passwordConfirmation) {
      setError("Passwords do not match");
      setLoading(false);
      return;
    }

    try {
      // const response = await apiInstance.post("/user/register/", {
      //   full_name: fullName,
      //   email,
      //   password1: password,
      //   password2: passwordConfirmation,
      // });
      const response = await register(fullName, email, password, passwordConfirmation);
      setSuccess("true");
    } catch (err) {
      setError(err.response.data?.detail || "Something went wrong");
      
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5 ">
      <h1 className="text-center mb-4">Register</h1>
      {error && <div className="alert alert-danger">{error}</div>}
      {success && (
        <div className="alert alert-success">
          Registration successful!
          <div className="mt-3">
            <button className="btn btn-primary me-2" onClick={() => navigate('/')}>Home</button>
            <button className="btn btn-secondary" onClick={() => navigate('/login')}>Login</button>
          </div>
        </div>
      )}
      {!success && (
        <form onSubmit={handleSubmit} className="mx-auto" style={{ maxWidth: '600px' }}>
        <div className="mb-3">
          <label htmlFor="fullName" className="form-label">Full Name:</label>
          <input
            type="text"
            className="form-control"
            id="fullName"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            required
          />
        </div>
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
        <div className="mb-3">
          <label htmlFor="passwordConfirmation" className="form-label">Confirm Password:</label>
          <input
            type="password"
            className="form-control"
            id="passwordConfirmation"
            value={passwordConfirmation}
            onChange={(e) => setPasswordConfirmation(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary w-100" disabled={loading}>
          {loading ? "Registering..." : "Register"}
        </button>
      </form>
      )}
      <div className="text-center mt-3">
        <Link to="/login">Already have an account? Login</Link>
      </div>
    </div>
  );
}

export default Register;
import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import apiInstance from "../../utils/axios";

function PasswordResetEmail() {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Reset error state when the component mounts
    setError("");
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    setSuccess(false);

    try {
      const response = await apiInstance.get(`/user/verify-email/${email}/`);
      console.log("Email sent successfully");
      console.log(response);
      setSuccess(true);
    } catch (err) {
        setError(err.response?.data?.message || "Something went wrong")
    } finally {
        setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <h1 className="text-center mb-4">Reset Password</h1>
      {error && <div className="alert alert-danger">{error}</div>}
      {success && (
        <div className="alert alert-success">
          Password reset email sent successfully!
          <div className="mt-3">
            <button className="btn btn-primary me-2" onClick={() => navigate('/')}>Home</button>
            <button className="btn btn-secondary" onClick={() => navigate('/login')}>Login</button>
          </div>
        </div>
      )}
      {!success && (
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
          <button type="submit" className="btn btn-primary w-100" disabled={loading}>
            {loading ? "Sending..." : "Send Password Reset Email"}
          </button>
        </form>
      )}
      <div className="text-center mt-3">
        <Link to="/login">Remembered your password? Login</Link>
      </div>
    </div>
  );
}

export default PasswordResetEmail;
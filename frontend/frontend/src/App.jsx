import { Route, Routes, BrowserRouter, useLocation, useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import MainWrapper from './layouts/mainWrapper'
import PrivateRoute from './layouts/privateRoute'
import Register from './views/auth/Register'
import Login from './views/auth/Login'
import Logout from './views/auth/Logout'
import 'bootstrap/dist/css/bootstrap.min.css';
import { logout } from './utils/auth'
import LoginStatus from './views/auth/LoginStatus'
import PasswordResetEmail from './views/auth/PasswordResetVerifyEmail'
import ResetPassword from './views/auth/ResetPassword'

function App() {
  return  (
    <BrowserRouter>
      <div className="container mt-5 ">
        <MainWrapper>
          <LoginStatus />
          <MyLandingPage />
          <Routes>
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route path="/logout" element={<Logout />} />
            <Route path="/verify-email" element={<PasswordResetEmail />} />
            <Route path="/reset-password" element={<ResetPassword />} />
            <Route path="/*" element={<PrivateRoute element={<MainWrapper />} />} />
          </Routes>
        </MainWrapper>
      </div>
    </BrowserRouter>

  )  
}

const MyLandingPage = () => {
  const location = useLocation();
  return location.pathname === '/' ? <h1>Hello World !</h1> : null
}

export default App

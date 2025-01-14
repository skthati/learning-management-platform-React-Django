import { Route, Routes, BrowserRouter, useLocation } from 'react-router-dom'
// import './App.css'
import MainWrapper from './layouts/mainWrapper'
import PrivateRoute from './layouts/privateRoute'
import Register from './views/auth/Register'
import Login from './views/auth/Login'
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return  (
    <BrowserRouter>
      <div className="container mt-5 ">
        <MainWrapper>
          <MyLandingPage />
          <Routes>
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
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

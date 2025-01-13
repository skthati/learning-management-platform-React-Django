import { Route, Routes, BrowserRouter } from 'react-router-dom'
import './App.css'
import MainWrapper from './layouts/mainWrapper'
import PrivateRoute from './layouts/privateRoute'
import Register from './views/auth/Register'

function App() {
  return  (
    <BrowserRouter>
      <MainWrapper>
        <Routes>
          <Route path="/register" element={<Register />} />
          <Route path="/*" element={<PrivateRoute element={<MainWrapper />} />} />
        </Routes>
      </MainWrapper>
    </BrowserRouter>

  )  
}

export default App

import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { DataProvider } from './context/DataContext'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import Hands from './pages/Hands'
import './styles/main.scss'

function App() {
  return (
    <BrowserRouter>
      <DataProvider>
        <div id="app">
          <Sidebar />
          <main>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/hands" element={<Hands />} />
            </Routes>
          </main>
        </div>
      </DataProvider>
    </BrowserRouter>
  )
}

export default App
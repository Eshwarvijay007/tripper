import { Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import LaylaPage from './pages/LaylaPage'
import ChatPage from './pages/ChatPage'

function App() {
  return (
    <div className="min-h-screen bg-white">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/layla" element={<LaylaPage />} />
        <Route path="/chat" element={<ChatPage />} />
      </Routes>
    </div>
  )
}

export default App
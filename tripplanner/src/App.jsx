import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import LaylaPage from './pages/LaylaPage';
import ChatPage from './pages/ChatPage';
import FinalTripPlannerPage from './pages/FinalTripPlannerPage';
import { ChatProvider } from './context/ChatContext';

function App() {
  return (
    <div className="min-h-screen bg-white">
      <ChatProvider>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/layla" element={<LaylaPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/trip" element={<FinalTripPlannerPage />} />
        </Routes>
      </ChatProvider>
    </div>
  );
}

export default App;
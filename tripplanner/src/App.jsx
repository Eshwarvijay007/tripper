import { Routes, Route, Navigate } from 'react-router-dom';
import NaomiPage from "./pages/NaomiPage";
import ChatPage from "./pages/ChatPage";
import FinalTripPlannerPage from "./pages/FinalTripPlannerPage";
import { ChatProvider } from "./context/ChatContext";

function App() {
  return (
    <div className="min-h-screen bg-white">
      <ChatProvider>
        <Routes>
          <Route path="/" element={<Navigate to="/naomi" replace />} />
          <Route path="/naomi" element={<NaomiPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/trip" element={<FinalTripPlannerPage />} />
        </Routes>
      </ChatProvider>
    </div>
  );
}

export default App;
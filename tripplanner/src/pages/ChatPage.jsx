import { Link } from 'react-router-dom'

const ChatPage = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Chat Interface</h1>
        <p className="text-gray-600 mb-8">This would be the dedicated chat interface for trip planning.</p>
        <Link 
          to="/layla" 
          className="inline-flex items-center gap-2 rounded-full bg-accent-green px-8 py-4 text-lg text-white ring-2 ring-accent-green ring-offset-2 transition-colors hover:bg-accent-green-2"
        >
          Go to Layla AI Chat
        </Link>
      </div>
    </div>
  )
}

export default ChatPage
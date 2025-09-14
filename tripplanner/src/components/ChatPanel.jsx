import React, { useContext, useEffect, useState } from 'react';
import { ChatContext } from '../context/ChatContext';

const ChatPanel = ({ onQuickAction, onUserMessage }) => {
  const { messages, addMessage } = useContext(ChatContext);
  const [inputValue, setInputValue] = useState('');

  // Seed assistant message similar to snapshot
  useEffect(() => {
    if (messages.length === 0) {
      addMessage({
        sender: 'assistant',
        text: 'Hi! Tell me about your trip. Where are you headed and when? I can plan your days and suggest stays.'
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleSendMessage = () => {
    if (inputValue.trim() === '') return;
    const text = inputValue;
    addMessage({ text, sender: 'user' });
    setInputValue('');
    if (onUserMessage) onUserMessage(text);
  };

  // Simple gradient avatar with three variants
  const GradientAvatar = ({ variant = 0 }) => {
    const variants = [
      'bg-gradient-to-br from-pink-500 via-orange-400 to-amber-300',
      'bg-gradient-to-br from-indigo-500 via-purple-500 to-fuchsia-500',
      'bg-gradient-to-br from-teal-400 via-emerald-500 to-lime-400',
    ];
    const cls = variants[variant % variants.length];
    return <div className={`w-8 h-8 rounded-full ${cls}`} />;
  };

  return (
    <section className="relative h-full bg-white">
      {/* Scrollable region (messages + quick replies) with reserved bottom space for input */}
      <div className="absolute inset-x-0 top-0 bottom-20 overflow-y-auto px-4 pt-4 pb-2">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex items-start gap-3 my-4 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {msg.sender === 'assistant' && <GradientAvatar variant={index} />}
            <div
              className={`rounded-lg px-4 py-2 max-w-lg ${
                msg.sender === 'user' ? 'bg-primary-green text-white' : 'bg-gray-100 text-gray-900'
              }`}
            >
              {msg.text}
            </div>
            {msg.sender === 'user' && <GradientAvatar variant={index + 1} />}
          </div>
        ))}
      </div>
      {/* Fixed bottom bar with credit counter and input */}
      <div className="absolute bottom-0 left-0 right-0 bg-white border-t">
        <div className="p-3">
          <div className="flex items-end gap-2 max-w-full">
            <textarea
              placeholder="Ask anything..."
              className="flex-1 min-h-10 border rounded-md px-3 py-2 focus:outline-none"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSendMessage();
                }
              }}
            />
            <button
              className="px-4 py-2 rounded-md bg-primary-green text-white disabled:opacity-50"
              onClick={handleSendMessage}
              disabled={!inputValue.trim()}
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ChatPanel;

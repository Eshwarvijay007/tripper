import React, { useContext, useEffect, useState } from 'react';
import { ChatContext } from '../context/ChatContext';

const ChatPanel = ({ onQuickAction, onUserMessage }) => {
  const { messages, addMessage } = useContext(ChatContext);
  const [inputValue, setInputValue] = useState('');

  // Seed assistant message similar to snapshot
  useEffect(() => {
    if (messages.length === 0) {
      addMessage({
        //sender: 'assistant',
        // text:
        //   "Now that we have your trip, how about we modify and reserve it. I can help you tailor your trip, update your preferences and add or remove things. Remember, the whole trip will be booked for you hassle free! You don't have to do anything.",
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

  return (
    <section className="relative h-full bg-white">
      {/* Scrollable region (messages + quick replies) with reserved bottom space for input */}
      <div className="absolute inset-x-0 top-0 bottom-20 overflow-y-auto px-4 pt-4 pb-2">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex items-start gap-3 my-4 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {msg.sender === 'assistant' && (
              <img
                src="https://layla.ai/theme/layla/new-character-small.webp"
                alt="Layla"
                className="w-8 h-8 rounded-full"
              />
            )}
            <div
              className={`rounded-lg px-4 py-2 max-w-lg ${
                msg.sender === 'user' ? 'bg-primary-green text-white' : 'bg-gray-100 text-gray-900'
              }`}
            >
              {msg.text}
            </div>
            {msg.sender === 'user' && <div className="w-8 h-8 rounded-full bg-gray-300"></div>}
          </div>
        ))}
        <div className="absolute bottom-2 left-0 right-0 bg-white border-t">
          {['Modify trip', 'Make it cheaper', 'Show hotels'].map((label) => (
            <button
              key={label}
              className="inline-flex items-center gap-2 rounded-full border px-3 py-1 text-sm hover:bg-gray-50 bg-white"
              onClick={() => {
                addMessage({ text: label, sender: 'user' });
                if (onQuickAction) onQuickAction(label);
              }}
            >
              {label}
            </button>
          ))}
        </div>
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

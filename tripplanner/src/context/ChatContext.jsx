import React, { createContext, useState } from 'react';

export const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState(() => [
    {
      sender: 'assistant',
      text: 'Hi! Tell me about your trip. Where are you headed and when? I can plan your days and suggest stays.'
    }
  ]);

  const addMessage = (message) => {
    setMessages((prevMessages) => {
      const last = prevMessages[prevMessages.length - 1];
      if (last && last.text === message.text && last.sender === message.sender) {
        return prevMessages; // prevent accidental duplicates
      }
      return [...prevMessages, message];
    });
  };

  const updateLastMessage = (text) => {
    setMessages((prevMessages) => {
      const newMessages = [...prevMessages];
      newMessages[newMessages.length - 1].text += text;
      return newMessages;
    });
  };

  return (
    <ChatContext.Provider value={{ messages, addMessage, updateLastMessage }}>
      {children}
    </ChatContext.Provider>
  );
};

import React, { createContext, useState } from 'react';

export const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState([]);

  const addMessage = (message) => {
    setMessages((prevMessages) => [...prevMessages, message]);
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

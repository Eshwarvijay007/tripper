import React, { createContext, useState } from 'react';

const STORAGE_KEY = 'tripper.conversationId';

const INITIAL_MESSAGES = [
  {
    sender: 'assistant',
    text: 'Hi! Tell me about your trip. Where are you headed and when? I can plan your days and suggest stays.'
  }
];

const cloneInitialMessages = () => INITIAL_MESSAGES.map((msg) => ({ ...msg }));

export const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState(() => cloneInitialMessages());
  const [conversationId, setConversationIdState] = useState(() => {
    if (typeof window === 'undefined') return null;
    return window.localStorage.getItem(STORAGE_KEY);
  });

  const persistConversationId = (value) => {
    setConversationIdState(value);
    if (typeof window === 'undefined') return;
    if (value) {
      window.localStorage.setItem(STORAGE_KEY, value);
    } else {
      window.localStorage.removeItem(STORAGE_KEY);
    }
  };

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

  const resetConversation = () => {
    setMessages(cloneInitialMessages());
    persistConversationId(null);
  };

  return (
    <ChatContext.Provider
      value={{
        messages,
        addMessage,
        updateLastMessage,
        conversationId,
        setConversationId: persistConversationId,
        resetConversation,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

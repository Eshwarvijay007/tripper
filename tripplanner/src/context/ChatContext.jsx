import React, { createContext, useState } from 'react';
import {
  clearConversationIdCookie,
  getConversationIdFromCookie,
  setConversationIdCookie,
} from '../lib/conversation';

export const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState(() => [
    {
      sender: 'assistant',
      text: 'Hi! Tell me about your trip. Where are you headed and when? I can plan your days and suggest stays.'
    }
  ]);
  const [conversationId, setConversationIdState] = useState(() => getConversationIdFromCookie());
  const [itineraryData, setItineraryData] = useState(null);
  const [isItineraryDone, setIsItineraryDone] = useState(false);
  const [typingSessions, setTypingSessions] = useState(0);

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

  const setConversationId = (id) => {
    setConversationIdState(id);
    if (id) {
      setConversationIdCookie(id);
    } else {
      clearConversationIdCookie();
    }
  };

  const updateItineraryData = (data, isDone = false) => {
    setItineraryData(data);
    setIsItineraryDone(isDone);
  };

  const startAssistantTyping = () => {
    setTypingSessions((count) => count + 1);
  };

  const stopAssistantTyping = () => {
    setTypingSessions((count) => Math.max(0, count - 1));
  };

  return (
    <ChatContext.Provider value={{ 
      messages, 
      addMessage, 
      updateLastMessage, 
      conversationId, 
      setConversationId,
      itineraryData,
      isItineraryDone,
      updateItineraryData,
      isAssistantTyping: typingSessions > 0,
      startAssistantTyping,
      stopAssistantTyping
    }}>
      {children}
    </ChatContext.Provider>
  );
};

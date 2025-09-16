import React, { useState, useContext } from 'react';
import { motion } from 'framer-motion';
import { Globe2, Briefcase, Users, FileText, Send } from 'lucide-react';
import { postChatMessage, streamChat } from '../lib/api';
import { ChatContext } from '../context/ChatContext';

const LaylaPromptSection = () => {
  const [inputValue, setInputValue] = useState('');
  const { addMessage, updateLastMessage, conversationId, setConversationId } = useContext(ChatContext);
  const [isTyping, setIsTyping] = useState(false);
  const [chatDisabled, setChatDisabled] = useState(false);

  const handleSendMessage = async (message) => {
    const text = message || inputValue;
    if (text.trim() === '' || chatDisabled) return;
    addMessage({ text, sender: 'user' });
    setInputValue('');
    setChatDisabled(true);
    setIsTyping(true);
    try {
      const { conversationId: newConversationId, streamUrl } = await postChatMessage({
        content: text,
        conversationId,
      });
      setConversationId(newConversationId);
      addMessage({ sender: 'assistant', text: '' });
      await streamChat({
        streamUrl,
        onEvent: (evt) => {
          if (!evt || typeof evt !== 'object') return;
          if (evt.event === 'message') {
            updateLastMessage(evt.content || '');
          } else if (evt.event === 'error') {
            const msg = evt.message || 'Something went wrong while generating a reply.';
            updateLastMessage(msg);
          }
        },
      });
    } catch (error) {
      const fallback = error instanceof Error ? error.message : 'Unexpected error sending message.';
      addMessage({ sender: 'assistant', text: fallback });
    } finally {
      setIsTyping(false);
      setChatDisabled(false);
    }
  };

  const quickActions = [
    { text: 'Create a new trip', icon: <Globe2 /> },
    { text: 'Inspire me where to go', icon: <Briefcase /> },
    { text: 'Build a road trip', icon: <Users /> },
    { text: 'Plan a last minute getaway', icon: <FileText /> },
  ];

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.6 }}
      className="bg-transparent gap-6 flex flex-col items-center w-full px-4 md:px-6 pb-30"
    >
      <div className="container mx-auto flex h-full w-full flex-col items-center justify-center gap-6">
        <div className="flex h-full w-full max-w-3xl flex-col justify-center gap-6">
          <div className="relative w-full min-w-3xs max-w-3xl rounded-2xl inline-flex flex-col justify-start items-start overflow-hidden bg-white/80 backdrop-blur-sm">
            <div className="prompt-text-area min-h-36 self-stretch rounded-2xl outline outline-1 outline-offset-[-1px] outline-input inline-flex flex-col justify-between items-start overflow-hidden">
              <div className="self-stretch flex flex-col justify-start items-start gap-2">
                <div className="self-stretch rounded-lg inline-flex justify-start items-start gap-1">
                  <textarea
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        handleSendMessage();
                      }
                    }}
                    placeholder="Plan a trip to..."
                    className="border-input placeholder:text-layla-muted-foreground focus-visible:border-ring focus-visible:ring-ring/50 flex field-sizing-content min-h-16 w-full rounded-md bg-transparent px-3 py-2 transition-[color,box-shadow] outline-none disabled:cursor-not-allowed disabled:opacity-50 md:text-sm dark:bg-transparent border-0 shadow-none focus-visible:ring-0 text-base resize-none overflow-y-auto"
                    disabled={chatDisabled}
                  ></textarea>
                </div>
              </div>
              <div className="self-stretch px-3 pb-3 gap-2 relative inline-flex justify-between items-end">
                <div className="flex-1 min-w-0 relative">
                  <div className="overflow-x-auto scrollbar-none">
                    <div className="flex justify-start items-center gap-1 w-max"></div>
                  </div>
                </div>
                <div className="flex justify-end items-center flex-shrink-0">
                  <button
                    onClick={() => handleSendMessage()}
                    disabled={!inputValue.trim() || chatDisabled}
                    className="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-all cursor-pointer disabled:pointer-events-none disabled:opacity-50 bg-primary-green text-white shadow-xs hover:bg-primary-green/90 size-9"
                  >
                    <Send />
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div className="flex flex-wrap items-center justify-center gap-2">
            {quickActions.map((action, index) => (
              <button
                key={index}
                onClick={() => handleSendMessage(action.text)}
                className="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-full text-sm font-medium transition-all cursor-pointer border bg-layla-background shadow-xs hover:bg-accent hover:text-accent-foreground h-9 px-4 py-2"
              >
                {action.icon}
                {action.text}
              </button>
            ))}
          </div>
          {/* Conversation renders only on /trip; Layla page is input-only */}
        </div>
      </div>
    </motion.section>
  );
};

export default LaylaPromptSection;

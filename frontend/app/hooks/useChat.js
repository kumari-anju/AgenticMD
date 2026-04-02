'use client';

import { useState, useCallback, useRef, useEffect } from 'react';
import * as api from '../lib/api';

const INITIAL_FORM_STATE = {
  hcp_name: '',
  date: '',
  interaction_type: 'Meeting',
  sentiment: '',
  shared_materials: [],
  topic_discussed: '',
};

const SYSTEM_MESSAGE = {
  role: 'system',
  content:
    'Log interaction details here (e.g., "Met Dr. Smith, discussed Prodo-X efficacy, positive sentiment, shared brochure") or ask for help.',
};

export function useChat() {
  const [messages, setMessages] = useState([SYSTEM_MESSAGE]);
  const [formState, setFormState] = useState(INITIAL_FORM_STATE);
  const [threadId, setThreadId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [conversations, setConversations] = useState([]);

  const [changedFields, setChangedFields] = useState([]);
  const prevFormRef = useRef(INITIAL_FORM_STATE);

  // Fetch all conversations for the user
  const fetchConversations = useCallback(async () => {
    try {
      const data = await api.getConversations();
      if (data.conversations) {
        setConversations(data.conversations);
      }
    } catch (err) {
      console.error('Failed to fetch conversations:', err);
    }
  }, []);

  // Load a specific thread (history and state)
  const loadThread = useCallback(async (id) => {
    if (!id) return;
    setIsLoading(true);
    setError(null);
    setThreadId(id);
    
    try {
      // Parallel fetch for speed
      const [historyData, stateData] = await Promise.all([
        api.getChatHistory(id),
        api.getThreadState(id),
      ]);

      if (historyData.messages) {
        // Map backend roles to frontend roles if necessary
        const mappedHistory = historyData.messages.map(m => ({
          role: m.role === 'human' ? 'user' : 'assistant',
          content: m.content
        }));
        setMessages([SYSTEM_MESSAGE, ...mappedHistory]);
      }

      if (stateData.state) {
        setFormState(stateData.state);
        prevFormRef.current = stateData.state;
      }
    } catch (err) {
      setError('Failed to load conversation history.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Reset to new conversation
  const startNewConversation = useCallback(() => {
    setThreadId(null);
    setMessages([SYSTEM_MESSAGE]);
    setFormState(INITIAL_FORM_STATE);
    prevFormRef.current = INITIAL_FORM_STATE;
    setError(null);
  }, []);

  const sendMessage = useCallback(
    async (prompt) => {
      if (!prompt.trim() || isLoading) return;

      setError(null);
      const userMessage = { role: 'user', content: prompt };
      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);

      try {
        const data = await api.sendChatMessage(prompt, threadId);

        const aiMessage = { role: 'assistant', content: data.response };
        setMessages((prev) => [...prev, aiMessage]);

        if (data.thread_id && data.thread_id !== threadId) {
          setThreadId(data.thread_id);
          fetchConversations(); // Refresh list if a new thread was created
        }

        if (data.state) {
          const prev = prevFormRef.current;
          const changed = [];
          for (const key of Object.keys(data.state)) {
            if (JSON.stringify(prev[key]) !== JSON.stringify(data.state[key]) && data.state[key] != null) {
              changed.push(key);
            }
          }
          setChangedFields(changed);
          setFormState(data.state);
          prevFormRef.current = data.state;
          if (changed.length > 0) {
            setTimeout(() => setChangedFields([]), 1600);
          }
        }
      } catch (err) {
        setError(err.message || 'Failed to get response from AI.');
        setMessages((prev) => [
          ...prev,
          { role: 'assistant', content: '⚠️ Sorry, I encountered an error. Please try again.' },
        ]);
      } finally {
        setIsLoading(false);
      }
    },
    [isLoading, threadId, fetchConversations]
  );

  const clearError = useCallback(() => setError(null), []);

  return {
    messages,
    formState,
    threadId,
    conversations,
    isLoading,
    error,
    changedFields,
    sendMessage,
    loadThread,
    fetchConversations,
    startNewConversation,
    clearError,
  };
}

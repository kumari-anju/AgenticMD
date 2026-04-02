'use client';

import { useState, useRef, useEffect } from 'react';

/**
 * ChatPanel — Right panel
 * AI assistant chat interface with message bubbles,
 * typing indicator, and input bar.
 */
export default function ChatPanel({ messages, isLoading, error, onSend, onClearError }) {
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  // Auto-resize textarea logic
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      const newHeight = Math.min(textarea.scrollHeight, 160); // approx 6 lines
      textarea.style.height = `${newHeight}px`;
    }
  }, [inputValue]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSubmit = (e) => {
    if (e) e.preventDefault();
    if (!inputValue.trim() || isLoading) return;
    onSend(inputValue.trim());
    setInputValue('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      if (e.shiftKey) {
        // Allow Shift+Enter for new line
        return;
      }
      // Enter to send
      e.preventDefault();
      handleSubmit();
    }
  };

  // Render message content – support bold (**text**) and line breaks
  const renderContent = (content) => {
    // Simple bold markdown: **text** → <strong>text</strong>
    const parts = content.split(/(\*\*[^*]+\*\*)/g);
    return parts.map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={i}>{part.slice(2, -2)}</strong>;
      }
      // Handle line breaks
      return part.split('\n').map((line, j) => (
        <span key={`${i}-${j}`}>
          {j > 0 && <br />}
          {line}
        </span>
      ));
    });
  };

  return (
    <div className="chat-panel" id="chat-panel">
      {/* ── Header ── */}
      <div className="chat-header">
        <div className="chat-header-title">
          <span className="robot-emoji">🤖</span>
          AI Assistant
        </div>
        <div className="chat-header-subtitle">
          Log Interaction details here via chat
        </div>
      </div>

      {/* ── Messages ── */}
      <div className="messages-area" id="messages-area">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <div className="message-bubble">
              {renderContent(msg.content)}
            </div>
          </div>
        ))}

        {/* Typing indicator */}
        {isLoading && (
          <div className="typing-indicator">
            <div className="typing-dot" />
            <div className="typing-dot" />
            <div className="typing-dot" />
          </div>
        )}

        {/* Error toast */}
        {error && (
          <div className="error-toast" onClick={onClearError}>
            {error}
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* ── Input ── */}
      <div className="chat-input-container">
        <textarea
          ref={textareaRef}
          className="chat-input"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Describe Interaction..."
          disabled={isLoading}
          id="chat-input"
          rows="1"
        />
        <button
          onClick={handleSubmit}
          className="send-button"
          disabled={isLoading || !inputValue.trim()}
          id="send-button"
          aria-label="Send message"
        >
          <span className="send-icon">
            {/* "A" icon matching the reference — styled as the Log button */}
            A
          </span>
        </button>
      </div>
    </div>
  );
}

'use client';

import { useEffect, useState } from 'react';
import InteractionForm from './components/InteractionForm';
import ChatPanel from './components/ChatPanel';
import Sidebar from './components/Sidebar';
import { useChat } from './hooks/useChat';
import { useAuth } from './hooks/useAuth';

export default function Home() {
  const { user, logout, loading: authLoading } = useAuth();
  const {
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
  } = useChat();
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);

  // Initial load
  useEffect(() => {
    if (user) {
      fetchConversations();
    }
  }, [user, fetchConversations]);

  if (authLoading || !user) {
    return (
      <div className="auth-container">
        <div style={{ color: 'var(--accent-blue)', fontWeight: 600 }}>Loading AgenticMD...</div>
      </div>
    );
  }

  return (
    <div className={`app-container ${isSidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
      <header className="dashboard-header">
        <div className="auth-logo" style={{ fontSize: '20px', marginBottom: 0 }}>
          <span className="logo-icon">🩺</span>
          <span>AgenticMD</span>
        </div>
        
        <div className="user-info">
          <div className="user-text">
            <span className="user-name">{user.full_name}</span>
            <span className="user-role" style={{ fontSize: '12px', color: 'var(--text-secondary)', marginLeft: '8px' }}>
              ({user.role})
            </span>
          </div>
          <button className="logout-btn" onClick={logout}>Sign Out</button>
        </div>
      </header>

      <main className="main-content">
        {/* Left Panel — Conversation History */}
        <Sidebar 
          conversations={conversations}
          activeThreadId={threadId}
          onThreadSelect={loadThread}
          onNewChat={startNewConversation}
          isCollapsed={isSidebarCollapsed}
          onToggle={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
        />

        {/* Center Panel — Interaction Details Form */}
        <InteractionForm
          formState={formState}
          changedFields={changedFields}
        />

        {/* Right Panel — AI Chat Assistant */}
        <ChatPanel
          messages={messages}
          isLoading={isLoading}
          error={error}
          onSend={sendMessage}
          onClearError={clearError}
        />
      </main>
    </div>
  );
}

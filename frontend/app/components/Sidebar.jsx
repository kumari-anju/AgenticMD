'use client';

import React from 'react';

/**
 * Sidebar component showing past conversation threads for the user.
 */
export default function Sidebar({ 
  conversations, 
  activeThreadId, 
  onThreadSelect, 
  onNewChat,
  isCollapsed,
  onToggle
}) {
  
  // Format date for better readability (IST)
  const formatDate = (dateStr) => {
    if (!dateStr) return 'Unknown Date';
    try {
      // Ensure the date is treated as UTC if it doesn't have a timezone indicator
      let normalizedDate = dateStr;
      if (!dateStr.endsWith('Z') && !dateStr.includes('+')) {
        normalizedDate += 'Z';
      }
      const date = new Date(normalizedDate);
      return date.toLocaleString('en-IN', { 
        day: 'numeric',
        month: 'short', 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: false,
        timeZone: 'Asia/Kolkata'
      });
    } catch (e) {
      return dateStr;
    }
  };

  return (
    <>
      <aside className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
        <div className="sidebar-header">
          <button className="new-chat-btn" onClick={onNewChat} title="New Session">
            <span>+</span> 
            {!isCollapsed && "New Session"}
          </button>
        </div>

        <div className="sidebar-content">
          {conversations.length === 0 ? (
            <div style={{ padding: '20px', textAlign: 'center', color: '#999', fontSize: '13px' }}>
              No recent sessions found.
            </div>
          ) : (
            conversations.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)).map((conv) => (
              <div 
                key={conv.thread_id} 
                className={`sidebar-item ${activeThreadId === conv.thread_id ? 'active' : ''}`}
                onClick={() => onThreadSelect(conv.thread_id)}
              >
                <div className="sidebar-item-title">
                  Session {conv.thread_id.substring(0, 8)}
                </div>
                <div className="sidebar-item-date">
                  {formatDate(conv.created_at)}
                </div>
              </div>
            ))
          )}
        </div>
      </aside>

      {/* Floating Toggle Button */}
      <button 
        className="sidebar-toggle-btn" 
        onClick={onToggle}
        title={isCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
      >
        <span className="toggle-icon">◀</span>
      </button>
    </>
  );
}

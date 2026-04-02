const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Common fetch wrapper to handle authentication headers.
 */
async function fetchWithAuth(endpoint, options = {}) {
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
    ...options.headers,
  };

  const url = `${API_BASE_URL}${endpoint}`;
  const res = await fetch(url, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Backend error: ${res.status}`);
  }

  return res.json();
}

/**
 * Send a chat message to the LangGraph backend.
 */
export async function sendChatMessage(prompt, threadId = null) {
  const body = { prompt };
  if (threadId) {
    body.thread_id = threadId;
  }

  return fetchWithAuth('/api/v1/chat/process', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

/**
 * User Signup API
 */
export async function signup(userData) {
  return fetchWithAuth('/api/v1/auth/signup', {
    method: 'POST',
    body: JSON.stringify(userData),
  });
}

/**
 * User Login API
 */
export async function login(email, password) {
  return fetchWithAuth('/api/v1/auth/login', {
    method: 'POST',
    body: JSON.stringify({
      email,
      password,
      full_name: 'Login User',
      confirm_pass: password,
    }),
  });
}

/**
 * Get Current User Profile
 */
export async function getMe() {
  return fetchWithAuth('/api/v1/auth/me', {
    method: 'GET',
  });
}

/**
 * Fetch all conversation thread IDs for the user
 */
export async function getConversations() {
  return fetchWithAuth('/api/v1/chat/conversations', {
    method: 'GET',
  });
}

/**
 * Fetch message history for a specific thread
 */
export async function getChatHistory(threadId) {
  return fetchWithAuth(`/api/v1/chat/history?thread_id=${threadId}`, {
    method: 'GET',
  });
}

/**
 * Fetch form state for a specific thread
 */
export async function getThreadState(threadId) {
  return fetchWithAuth(`/api/v1/chat/state?thread_id=${threadId}`, {
    method: 'GET',
  });
}

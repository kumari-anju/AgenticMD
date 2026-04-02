'use client';

import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import * as api from '../lib/api';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  const loadUser = useCallback(async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setLoading(false);
      return;
    }

    try {
      const userData = await api.getMe();
      setUser(userData);
    } catch (err) {
      console.error('Failed to load user:', err);
      localStorage.removeItem('access_token');
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadUser();
  }, [loadUser]);

  const login = async (email, password) => {
    setLoading(true);
    try {
      const { access_token } = await api.login(email, password);
      localStorage.setItem('access_token', access_token);
      await loadUser();
      router.push('/');
    } catch (err) {
      setLoading(false);
      throw err;
    }
  };

  const signup = async (userData) => {
    setLoading(true);
    try {
      await api.signup(userData);
      // Automatically login after signup
      const { access_token } = await api.login(userData.email, userData.password);
      localStorage.setItem('access_token', access_token);
      await loadUser();
      router.push('/');
    } catch (err) {
      setLoading(false);
      throw err;
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
    router.push('/auth/login');
  };

  // Redirect to login if user is not authenticated and trying to access protected routes
  useEffect(() => {
    if (!loading && !user && !pathname.startsWith('/auth')) {
      router.push('/auth/login');
    }
  }, [user, loading, pathname, router]);

  return (
    <AuthContext.Provider value={{ user, loading, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

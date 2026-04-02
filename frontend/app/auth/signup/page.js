'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '../../hooks/useAuth';

export default function SignupPage() {
  const [formData, setFormData] = useState({
    email: '',
    full_name: '',
    password: '',
    confirm_pass: '',
    role: 'Physician',
    organization: '',
  });
  const [error, setError] = useState('');
  const { signup, loading } = useAuth();

  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData((prev) => ({ ...prev, [id]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirm_pass) {
      setError('Passwords do not match');
      return;
    }

    try {
      await signup(formData);
    } catch (err) {
      setError(err.message || 'Failed to create account');
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card" style={{ maxWidth: '500px' }}>
        <div className="auth-header">
          <div className="auth-logo">
            <span className="logo-icon">🩺</span>
            <span>AgenticMD</span>
          </div>
          <h1 className="auth-title">Create Account</h1>
          <p className="auth-subtitle">Join AgenticMD to start managing interaction logs</p>
        </div>

        {error && <div className="auth-error">{error}</div>}

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label" htmlFor="full_name">Full Name</label>
              <input
                id="full_name"
                className="auth-input"
                placeholder="John Doe"
                value={formData.full_name}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label" htmlFor="email">Email Address</label>
              <input
                id="email"
                type="email"
                className="auth-input"
                placeholder="john@example.com"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label" htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                className="auth-input"
                placeholder="••••••••"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label" htmlFor="confirm_pass">Confirm Password</label>
              <input
                id="confirm_pass"
                type="password"
                className="auth-input"
                placeholder="••••••••"
                value={formData.confirm_pass}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label" htmlFor="role">Role</label>
              <select
                id="role"
                className="auth-input"
                value={formData.role}
                onChange={handleChange}
                style={{ appearance: 'auto', paddingRight: '12px' }}
              >
                <option value="Physician">Physician</option>
                <option value="Medical Representative">Medical Rep</option>
                <option value="Administrator">Administrator</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label" htmlFor="organization">Organization</label>
              <input
                id="organization"
                className="auth-input"
                placeholder="St. Mary's Hospital"
                value={formData.organization}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <button 
            type="submit" 
            className="auth-button"
            disabled={loading}
          >
            {loading ? 'Creating account...' : 'Sign Up'}
          </button>
        </form>

        <div className="auth-footer">
          Already have an account? 
          <Link href="/auth/login" className="auth-link">Sign In</Link>
        </div>
      </div>
    </div>
  );
}

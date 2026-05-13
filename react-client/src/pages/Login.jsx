import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('/auth/login', { username, password });
      localStorage.setItem('token', res.data.access_token);
      navigate('/profile');
      window.location.reload();
    } catch (err) {
      setError(err.response?.data?.detail || 'Помилка входу');
    }
  };

  return (
    <div className="auth-container">
      <h2>Вхід</h2>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleLogin} className="auth-form">
        <input
          type="text"
          placeholder="Ім'я користувача"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit" className="btn primary">Увійти</button>
      </form>
    </div>
  );
}

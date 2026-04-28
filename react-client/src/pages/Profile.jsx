import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';

export default function Profile() {
  const [user, setUser] = useState(null);
  const [favorites, setFavorites] = useState([]);
  const [friends, setFriends] = useState([]);
  const [searchUser, setSearchUser] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  useEffect(() => {
    fetchProfile();
    fetchFavorites();
    fetchFriends();
  }, []);

  const fetchProfile = async () => {
    try {
      const res = await api.get('/users/me');
      setUser(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchFavorites = async () => {
    try {
      const res = await api.get('/actions/favorites');
      setFavorites(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchFriends = async () => {
    try {
      const res = await api.get('/users/friends');
      setFriends(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSearchUsers = async () => {
    try {
      const res = await api.get(`/users/search?query=${searchUser}`);
      setSearchResults(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const addFriend = async (userId) => {
    try {
      await api.post(`/users/friends/${userId}`);
      alert('Запит надіслано');
      fetchFriends();
    } catch (err) {
      alert(err.response?.data?.detail || 'Помилка');
    }
  };

  const acceptFriend = async (userId) => {
    try {
      await api.post(`/users/friends/${userId}/accept`);
      fetchFriends();
    } catch (err) {
      console.error(err);
    }
  };

  const rejectFriend = async (userId) => {
    try {
      await api.post(`/users/friends/${userId}/reject`);
      fetchFriends();
    } catch (err) {
      console.error(err);
    }
  };

  const removeFriend = async (userId) => {
    try {
      await api.delete(`/users/friends/${userId}`);
      fetchFriends();
    } catch (err) {
      console.error(err);
    }
  };

  const removeFavorite = async (gameId) => {
    try {
      await api.delete(`/actions/favorites/${gameId}`);
      fetchFavorites();
    } catch (err) {
      alert(err.response?.data?.detail || 'Помилка видалення');
    }
  };

  if (!user) return <div>Завантаження...</div>;

  return (
    <div className="profile-container">
      <div className="profile-header">
        <h2>Привіт, {user.username}!</h2>
        <p>Email: {user.email}</p>
      </div>

      <div className="profile-sections">
        <section className="favorites-section">
          <h3>Улюблені ігри</h3>
          <div className="games-list">
            {favorites.length === 0 ? <p>Немає улюблених ігор</p> : favorites.map(game => (
              <div key={game.id} className="game-card small">
                {game.image_url && <img src={game.image_url} alt={game.title} />}
                <div className="game-info">
                  <h4>{game.title}</h4>
                  <button onClick={() => removeFavorite(game.id)} className="btn danger">Видалити</button>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="friends-section">
          <h3>Друзі</h3>
          
          <div className="friends-list">
            <h4>Мої друзі</h4>
            {friends.filter(f => f.status === 'accepted').map(friend => (
              <div key={friend.id} className="friend-item">
                <span>{friend.username}</span>
                <div className="actions">
                  <Link to={`/chat/${friend.id}`} className="btn primary small">Чат</Link>
                  <button onClick={() => removeFriend(friend.id)} className="btn danger small">Видалити</button>
                </div>
              </div>
            ))}
            {friends.filter(f => f.status === 'accepted').length === 0 && <p>Немає друзів</p>}

            <h4>Вхідні запити</h4>
            {friends.filter(f => f.status === 'pending' && f.direction === 'received').map(req => (
              <div key={req.id} className="friend-item">
                <span>{req.username}</span>
                <div className="actions">
                  <button onClick={() => acceptFriend(req.id)} className="btn success small">Прийняти</button>
                  <button onClick={() => rejectFriend(req.id)} className="btn danger small">Відхилити</button>
                </div>
              </div>
            ))}
            {friends.filter(f => f.status === 'pending' && f.direction === 'received').length === 0 && <p>Немає запитів</p>}

            <h4>Надіслані запити</h4>
            {friends.filter(f => f.status === 'pending' && f.direction === 'sent').map(req => (
              <div key={req.id} className="friend-item">
                <span>{req.username}</span>
                <span className="badge">В очікуванні</span>
              </div>
            ))}
          </div>

          <div className="search-users">
            <h4>Знайти друзів</h4>
            <input 
              type="text" 
              value={searchUser}
              onChange={(e) => setSearchUser(e.target.value)}
              placeholder="Ім'я користувача..."
            />
            <button onClick={handleSearchUsers} className="btn primary small">Пошук</button>
            <div className="search-results">
              {searchResults.map(u => (
                <div key={u.id} className="search-result-item">
                  <span>{u.username}</span>
                  <button onClick={() => addFriend(u.id)} className="btn secondary small">Додати</button>
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

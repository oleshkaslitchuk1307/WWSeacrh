import { useState, useEffect } from 'react';
import api from '../api';

export default function Home() {
  const [games, setGames] = useState([]);
  const [genres, setGenres] = useState([]);
  const [search, setSearch] = useState('');
  const [genre, setGenre] = useState('');
  
  useEffect(() => {
    fetchGenres();
    fetchGames();
  }, []);

  const fetchGenres = async () => {
    try {
      const res = await api.get('/games/genres');
      setGenres(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchGames = async () => {
    try {
      const params = new URLSearchParams();
      if (search) params.append('title', search);
      if (genre) params.append('genre', genre);
      
      const res = await api.get(`/search?${params.toString()}`);
      setGames(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const addFavorite = async (gameId) => {
    try {
      await api.post(`/actions/favorites/${gameId}`);
      alert('Гру додано в улюблені!');
    } catch (err) {
      alert(err.response?.data?.detail || 'Помилка');
    }
  };

  return (
    <div className="home-container">
      <div className="search-bar">
        <input 
          type="text" 
          placeholder="Пошук ігор..." 
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select value={genre} onChange={(e) => setGenre(e.target.value)}>
          <option value="">Всі жанри</option>
          {genres.map(g => <option key={g} value={g}>{g}</option>)}
        </select>
        <button onClick={fetchGames} className="btn primary">Пошук</button>
      </div>

      <div className="games-grid">
        {games.map(game => (
          <div key={game.id} className="game-card">
            {game.image_url && <img src={game.image_url} alt={game.title} className="game-img" />}
            <div className="game-info">
              <h3>{game.title}</h3>
              <p>{game.genre}</p>
              <p>⭐️ {game.rating}</p>
              {localStorage.getItem('token') && (
                <button onClick={() => addFavorite(game.id)} className="btn secondary">
                  Додати в улюблені
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

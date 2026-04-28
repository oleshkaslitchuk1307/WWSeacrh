import { useState, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api';

export default function Chat() {
  const { userId } = useParams();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [otherUser, setOtherUser] = useState(null);
  const [currentUser, setCurrentUser] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    fetchMessages();
    fetchOtherUser();
    fetchCurrentUser();
    const interval = setInterval(fetchMessages, 3000);
    return () => clearInterval(interval);
  }, [userId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const fetchMessages = async () => {
    try {
      const res = await api.get(`/chat/${userId}`);
      setMessages(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchOtherUser = async () => {
    try {
      const res = await api.get(`/users/${userId}`);
      setOtherUser(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchCurrentUser = async () => {
    try {
      const res = await api.get('/users/me');
      setCurrentUser(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    try {
      await api.post('/chat', {
        receiver_id: parseInt(userId),
        message: newMessage
      });
      setNewMessage('');
      fetchMessages();
    } catch (err) {
      alert('Помилка відправки');
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <Link to="/profile" className="btn secondary small">← Назад</Link>
        {otherUser && <h3>Чат з {otherUser.username}</h3>}
      </div>

      <div className="messages-window">
        {messages.map((msg) => {
          const isMe = msg.sender_id === currentUser?.id;
          const senderName = isMe ? 'Ви' : (otherUser?.username || 'Друг');
          
          return (
            <div 
              key={msg.id} 
              className={`message-wrapper ${isMe ? 'sent' : 'received'}`}
            >
              <div className="message-bubble">
                <span className="sender-name">{senderName}</span>
                <p>{msg.message}</p>
                <span className="timestamp">{new Date(msg.timestamp).toLocaleTimeString()}</span>
              </div>
            </div>
          );
        })}
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-form" onSubmit={sendMessage}>
        <input 
          type="text" 
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Напишіть повідомлення..."
        />
        <button type="submit" className="btn primary">Відправити</button>
      </form>
    </div>
  );
}

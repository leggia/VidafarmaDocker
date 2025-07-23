import React, { useState } from 'react';
import './App.css';

function App() {
  const [consulta, setConsulta] = useState('');
  const [respuesta, setRespuesta] = useState('');
  const [isListening, setIsListening] = useState(false);

  // Función para manejar consultas por texto
  const handleConsulta = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/consulta-ia', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ texto: consulta, tipo: 'general' }),
      });
      const data = await response.json();
      setRespuesta(data.respuesta);
    } catch (error) {
      setRespuesta('Error al conectar con la API');
    }
  };

  // Función para reconocimiento de voz (Web Speech API)
  const startListening = () => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      
      recognition.lang = 'es-ES';
      recognition.continuous = false;
      recognition.interimResults = false;
      
      recognition.onstart = () => {
        setIsListening(true);
      };
      
      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setConsulta(transcript);
        setIsListening(false);
      };
      
      recognition.onerror = (event) => {
        console.error('Error en reconocimiento de voz:', event.error);
        setIsListening(false);
      };
      
      recognition.start();
    } else {
      alert('Tu navegador no soporta reconocimiento de voz');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Vidafarma_IA</h1>
        <p>Plataforma inteligente para gestión de farmacias</p>
      </header>
      
      <main>
        <div className="consulta-section">
          <h2>Consulta por voz o texto</h2>
          
          <div className="input-group">
            <input
              type="text"
              value={consulta}
              onChange={(e) => setConsulta(e.target.value)}
              placeholder="Escribe tu consulta o usa el micrófono..."
              className="consulta-input"
            />
            <button
              onClick={startListening}
              disabled={isListening}
              className="mic-button"
            >
              {isListening ? '🎤 Escuchando...' : '🎤'}
            </button>
          </div>
          
          <button onClick={handleConsulta} className="send-button">
            Enviar consulta
          </button>
          
          {respuesta && (
            <div className="respuesta">
              <h3>Respuesta:</h3>
              <p>{respuesta}</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App; 
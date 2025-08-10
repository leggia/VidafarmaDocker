import React, { useState, useEffect } from 'react';
import './App.css';
import { BarcodeScanner } from './components/BarcodeScanner';
import { auth, googleProvider } from './firebase'; // Importar desde firebase.js
import { signInWithPopup, onAuthStateChanged, signOut } from "firebase/auth";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

// --- Función para obtener el token de forma segura ---
async function getAuthToken() {
  console.log("getAuthToken: auth.currentUser", auth.currentUser); // Added for debugging
  if (!auth.currentUser) {
    throw new Error("Usuario no autenticado.");
  }
  return await auth.currentUser.getIdToken(true);
}

function App() {
  const [user, setUser] = useState(null); // Estado para el usuario
  const [consulta, setConsulta] = useState('');
  const [respuesta, setRespuesta] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [isScanning, setIsScanning] = useState(false);

  // --- Efecto para observar cambios en la autenticación ---
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
    });
    // Limpiar el observador al desmontar el componente
    return () => unsubscribe();
  }, []);

  // --- Funciones de Autenticación ---
  const handleLogin = async () => {
    try {
      await signInWithPopup(auth, googleProvider);
    } catch (error) {
      console.error("Error durante el inicio de sesión:", error);
      setRespuesta("Error al iniciar sesión. Por favor, inténtalo de nuevo.");
    }
  };

  const handleLogout = async () => {
    try {
      await signOut(auth);
    } catch (error) {
      console.error("Error durante el cierre de sesión:", error);
    }
  };

  // --- Funciones de API (Modificadas) ---
  const handleConsulta = async () => {
    if (!consulta.trim()) return;

    try {
      const token = await getAuthToken();
      console.log("Firebase ID Token obtenido:", token ? token.substring(0, 30) + '...' : 'No token'); // Log del token (truncado)
      const response = await fetch(`${API_BASE_URL}/api/consulta-ia`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`, // Enviar token
        },
        body: JSON.stringify({ texto: consulta, tipo: 'general' }),
      });

      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }

      const data = await response.json();
      setRespuesta(data.respuesta_ia.respuesta);
    } catch (error) {
      console.error("Error al conectar con la API:", error);
      setRespuesta('Error al conectar con la API. Revisa la consola para más detalles.');
    }
  };

  const handleBarcodeScan = async (barcode) => {
    setIsScanning(false);
    try {
      const token = await getAuthToken();
      const response = await fetch(`${API_BASE_URL}/api/odoo/product/barcode/${barcode}`, {
        headers: {
          'Authorization': `Bearer ${token}`, // Enviar token
        },
      });
      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }
      const data = await response.json();
      setRespuesta(`Producto encontrado: ${data.name} - Precio: S/ ${data.list_price.toFixed(2)} - Stock: ${data.qty_available}`);
    } catch (error) {
      console.error("Error al buscar producto por código de barras:", error);
      setRespuesta('Producto no encontrado con ese código de barras.');
    }
  };

  // --- Lógica de Renderizado ---
  if (!user) {
    return (
      <div className="App">
        <header className="App-header">
          <h1>Bienvenido a Vidafarma IA</h1>
          <p>Por favor, inicia sesión para continuar</p>
          <button onClick={handleLogin} className="login-button">Iniciar Sesión con Google</button>
        </header>
      </div>
    );
  }

  // --- Interfaz Principal (si el usuario está autenticado) ---
  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <h1>Vidafarma IA</h1>
          <p>Tu asistente inteligente para la gestión de farmacia</p>
        </div>
        <div className="user-info">
          <span>Hola, {user.displayName}</span>
          <button onClick={handleLogout} className="logout-button">Cerrar Sesión</button>
        </div>
      </header>
      
      <main>
        {isScanning ? (
          <div className="scanner-container">
            <BarcodeScanner 
              onResult={handleBarcodeScan} 
              onError={(e) => setRespuesta("Error de escáner: " + e.message)} 
            />
            <button onClick={() => setIsScanning(false)}>Cancelar</button>
          </div>
        ) : (
          <div className="consulta-container">
            <h2>¿Cómo puedo ayudarte?</h2>
            
            <div className="input-group">
              <input
                type="text"
                value={consulta}
                onChange={(e) => setConsulta(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleConsulta()}
                placeholder="Escribe o pulsa el micrófono..."
                className="consulta-input"
              />
              <button
                onClick={() => { /* Lógica de reconocimiento de voz */ }}
                disabled={isListening}
                className={`mic-button ${isListening ? 'listening' : ''}`}
                aria-label="Iniciar reconocimiento de voz"
              >
                {isListening ? '... 🎤' : '🎤'}
              </button>
              <button onClick={() => setIsScanning(true)} className="scan-button">📷</button>
            </div>
            
            <button onClick={handleConsulta} className="send-button" disabled={!consulta.trim()}>
              Enviar
            </button>
            
            {respuesta && (
              <div className="respuesta-container">
                <h3>Respuesta:</h3>
                <p>{respuesta}</p>
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="App-footer">
        <p>Desarrollado con IA</p>
      </footer>
    </div>
  );
}

export default App;

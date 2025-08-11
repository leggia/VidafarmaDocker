import { useState, useEffect, useRef } from 'react';

// Comprobación de compatibilidad del navegador
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition;

if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = false; // Solo captura una frase a la vez
    recognition.lang = 'es-ES';     // Configurado para español
    recognition.interimResults = false;
}

export const useSpeechRecognition = () => {
    const [isListening, setIsListening] = useState(false);
    const [transcript, setTranscript] = useState('');
    const [error, setError] = useState(null);

    const startListening = () => {
        if (!recognition) {
            setError("El reconocimiento de voz no es compatible con este navegador.");
            return;
        }
        if (isListening) return;

        setTranscript(''); // Limpia la transcripción anterior
        setIsListening(true);
        setError(null);
        recognition.start();
    };

    useEffect(() => {
        if (!recognition) return;

        recognition.onresult = (event) => {
            const currentTranscript = event.results[0][0].transcript;
            setTranscript(currentTranscript);
            setIsListening(false); // Deja de escuchar después de obtener un resultado
        };

        recognition.onerror = (event) => {
            setError(`Error de reconocimiento: ${event.error}`);
            setIsListening(false);
        };

        recognition.onend = () => {
            // Se asegura de que el estado de "escuchando" esté desactivado
            setIsListening(false);
        };
    }, []);

    return { isListening, transcript, error, startListening, hasRecognitionSupport: !!recognition };
};
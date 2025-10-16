import { useState, useRef, useEffect } from 'react';
import PropTypes from 'prop-types';
import './AudioRecorder.css';

function AudioRecorder({ onTranscription, onCommand, isActive }) {
  const [isRecording, setIsRecording] = useState(false);
  const [useWebSpeech, setUseWebSpeech] = useState(false);
  const mediaRecorderRef = useRef(null);
  const recognitionRef = useRef(null);
  const streamRef = useRef(null);

  useEffect(() => {
    if (isActive) {
      startRecording();
    } else {
      stopRecording();
    }

    return () => {
      stopRecording();
    };
  }, [isActive]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      // Intentar usar Web Speech API primero
      const started = startWebSpeechRecognition();
      
      if (started) {
        setUseWebSpeech(true);
        setIsRecording(true);
      } else {
        // Fallback a MediaRecorder
        setUseWebSpeech(false);
        startMediaRecorder(stream);
      }
    } catch (error) {
      console.error('Error al iniciar grabación:', error);
      alert('No se pudo acceder al micrófono. Verifica los permisos.');
    }
  };

  const startWebSpeechRecognition = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
      console.log('Web Speech API no disponible');
      return false;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.lang = 'es-ES';
      recognition.interimResults = false;
      recognition.continuous = true;

      recognition.onresult = (event) => {
        const last = event.results[event.results.length - 1];
        if (last.isFinal) {
          const text = last[0].transcript.trim();
          console.log('Reconocido:', text);
          
          if (onTranscription) {
            onTranscription(text);
          }

          // Parsear comando si tiene palabra clave
          const parsed = parseCommand(text);
          if (parsed && onCommand) {
            onCommand(parsed);
          }
        }
      };

      recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
      };

      recognition.start();
      recognitionRef.current = recognition;
      setIsRecording(true);
      return true;
    } catch (error) {
      console.error('Error iniciando Web Speech:', error);
      return false;
    }
  };

  const startMediaRecorder = (stream) => {
    const mediaRecorder = new MediaRecorder(stream);
    const audioChunks = [];

    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
      
      if (onTranscription) {
        onTranscription(audioBlob);
      }

      // Reiniciar grabación si sigue activo
      if (isActive) {
        audioChunks.length = 0;
        mediaRecorder.start();
        setTimeout(() => {
          if (mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
          }
        }, 5000);
      }
    };

    mediaRecorder.start();
    mediaRecorderRef.current = mediaRecorder;
    setIsRecording(true);

    // Grabar en intervalos de 5 segundos
    setTimeout(() => {
      if (mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
      }
    }, 5000);
  };

  const stopRecording = () => {
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
        recognitionRef.current = null;
      } catch (error) {
        console.warn('Error deteniendo reconocimiento:', error);
      }
    }

    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current = null;
    }

    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }

    setIsRecording(false);
  };

  const parseCommand = (text) => {
    const t = text.toLowerCase();
    
    // Más flexible - no requiere exactamente "travistec"
    if (!t.includes('travis') && t.length < 3) {
      return null;
    }

    // Limpiar texto
    let payloadText = t.replace('travis tec', '').replace('travistec', '').replace('travis', '').trim();

    // Extraer números y palabras clave
    const numbers = payloadText.match(/\d+(\.\d+)?/g) || [];
    const params = {};
    let task = 'unknown';

    // 1) Bitcoin - buscar en cualquier parte del texto (predicción a CORTO PLAZO)
    if (payloadText.match(/\b(bitcoin|btc|bit coin)\b/i)) {
      task = 'bitcoin';
      if (numbers.length > 0) {
        params.days = parseInt(numbers[0]); // Cambiado a días
      }
    }

    // 2) Película - más flexible (acepta plural y singular)
    else if (payloadText.match(/\b(pel[ií]culas?|movies?|recomienda|recomendaci[óo]n|film|films)\b/i)) {
      task = 'movie';
      // Extraer título después de "pelicula"
      const match = payloadText.match(/pel[íi]culas?\s+(.+)/);
      if (match) {
        params.title = match[1].trim();
      }
    }

    // 3) Automóvil - más variaciones (acepta plurales y "teccar")
    else if (payloadText.match(/\b(autom[óo]viles?|autos?|coches?|carros?|cars?|veh[íi]culos?|teccar|tec\s*car)\b/i)) {
      task = 'car';
      if (numbers.length >= 2) {
        params.year = parseInt(numbers[0], 10);
        params.km = parseInt(numbers[1], 10);
      }
    }

    // 4) SP500 - muy flexible (acepta 500, 507, 50, etc.) - predicción a CORTO PLAZO
    else if (payloadText.match(/\b(sp\s*[45]\d{2}|sp\s*50\d?|s\s*[&y]?\s*p\s*[45]\d{2}|s\s*[&y]?\s*p\s*50\d?|standard|sandp|s\s*and\s*p)\b/i)) {
      task = 'sp500';
      if (numbers.length > 0) {
        params.days = parseInt(numbers[0]); // Cambiado a días
      }
    }

    // 5) Masa corporal - más variaciones
    else if (payloadText.match(/\b(masa\s*corporal|imc|bmi|grasa|peso|altura)\b/i)) {
      task = 'bmi';
      if (numbers.length >= 2) {
        params.height = parseFloat(numbers[0]);
        params.weight = parseFloat(numbers[1]);
      }
      if (numbers.length >= 3) {
        params.age = parseInt(numbers[2], 10);
      }
    }

    // 6) Aguacate - más flexible (acepta plurales) - predicción a CORTO PLAZO
    else if (payloadText.match(/\b(aguacates?|avocados?|paltas?)\b/i)) {
      task = 'avocado';
      if (numbers.length > 0) {
        params.days = parseInt(numbers[0]); // Cambiado a días
      }
    }

    // 7) Londres - más flexible
    else if (payloadText.match(/\b(londres|london)\b/i)) {
      task = 'london';
      const days = ['lunes', 'martes', 'miercoles', 'miércoles', 'jueves', 'viernes', 'sabado', 'sábado', 'domingo'];
      const foundDay = days.find(d => payloadText.includes(d));
      if (foundDay) {
        params.day = foundDay;
      }
    }

    // 8) Chicago - más flexible
    else if (payloadText.match(/\b(chicago)\b/i)) {
      task = 'chicago';
      const days = ['lunes', 'martes', 'miercoles', 'miércoles', 'jueves', 'viernes', 'sabado', 'sábado', 'domingo'];
      const foundDay = days.find(d => payloadText.includes(d));
      if (foundDay) {
        params.day = foundDay;
      }
    }

    // 9) Cirrosis - más flexible (acepta plurales)
    else if (payloadText.match(/\b(cirrosis|cirrhosis|h[íi]gados?)\b/i)) {
      task = 'cirrhosis';
      // Extraer edad y bilirrubina si se dan parámetros numéricos
      if (numbers.length >= 1) {
        params.age = parseFloat(numbers[0]) * 365; // Convertir años a días
      }
      if (numbers.length >= 2) {
        params.bilirubin = parseFloat(numbers[1]);
      }
    }

    // 10) Avión - más flexible (acepta plurales)
    else if (payloadText.match(/\b(aviones?|vuelos?|flights?|aerol[íi]neas?)\b/i)) {
      task = 'airline';
      // Extraer mes, día y distancia
      if (numbers.length >= 1) {
        params.month = parseInt(numbers[0], 10);  // Primer número = mes
      }
      if (numbers.length >= 2) {
        params.day = parseInt(numbers[1], 10);  // Segundo número = día
      }
      if (numbers.length >= 3) {
        params.distance = parseInt(numbers[2], 10);  // Tercer número = distancia en millas
      }
      
      // Extraer mes por nombre
      const months = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
        'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
      };
      const foundMonth = Object.keys(months).find(m => payloadText.includes(m));
      if (foundMonth) {
        params.month = months[foundMonth];
      }
    }

    return {
      text: payloadText,
      task: task,
      params: params
    };
  };

  return (
    <div className="audio-recorder">
      <div className={`recording-indicator ${isRecording ? 'active' : ''}`}>
        <div className="pulse"></div>
        <span>
          {isRecording 
            ? `🎤 Grabando ${useWebSpeech ? '(Web Speech)' : '(MediaRecorder)'}`
            : '🎤 Micrófono inactivo'
          }
        </span>
      </div>
    </div>
  );
}

AudioRecorder.propTypes = {
  onTranscription: PropTypes.func,
  onCommand: PropTypes.func,
  isActive: PropTypes.bool.isRequired
};

export default AudioRecorder;

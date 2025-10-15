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
    
    if (!t.includes('travistec') && !t.includes('travis tec')) {
      return null;
    }

    let payloadText = t.replace('travis tec', '').replace('travistec', '').trim();

    // Extraer números y palabras clave
    const numbers = payloadText.match(/\d+(\.\d+)?/g) || [];
    const params = {};
    let task = 'unknown';

    // 1) travisTEC predice el precio del bitcoin
    if (payloadText.includes('bitcoin')) {
      task = 'bitcoin';
      // Sin parámetros - usa datos recientes
    }

    // 2) travisTEC recomienda una pelicula
    else if (payloadText.includes('pelicula') || payloadText.includes('película') || payloadText.includes('recomienda')) {
      task = 'movie';
      // Extraer título después de "pelicula"
      const match = payloadText.match(/pel[íi]cula\s+(.+)/);
      if (match) {
        params.title = match[1].trim();
      }
    }

    // 3) travisTEC Predice el precio de un automovil (año y kilometraje)
    else if (payloadText.includes('automovil') || payloadText.includes('automóvil') || payloadText.includes('coche') || payloadText.includes('carro')) {
      task = 'car';
      if (numbers.length >= 2) {
        params.year = parseInt(numbers[0], 10);
        params.km = parseInt(numbers[1], 10);
      }
    }

    // 4) travisTEC Predice el precio del SP500 (tiempo en años)
    else if (payloadText.includes('sp500') || payloadText.includes('sp 500') || payloadText.includes('sp50')) {
      task = 'sp500';
      if (numbers.length > 0) {
        params.years = parseFloat(numbers[0]);
      }
    }

    // 5) travisTEC Predice la masa corporal (altura, peso, edad)
    else if (payloadText.includes('masa corporal') || payloadText.includes('imc') || payloadText.includes('grasa')) {
      task = 'bmi';
      if (numbers.length >= 2) {
        params.height = parseFloat(numbers[0]);
        params.weight = parseFloat(numbers[1]);
      }
      if (numbers.length >= 3) {
        params.age = parseInt(numbers[2], 10);
      }
    }

    // 6) travisTEC predice el precio del aguacate (tiempo en años)
    else if (payloadText.includes('aguacate') || payloadText.includes('avocado')) {
      task = 'avocado';
      if (numbers.length > 0) {
        params.years = parseFloat(numbers[0]);
      }
    }

    // 7) Predecir la cantidad de crimenes por dia en Londres (día de la semana)
    else if (payloadText.includes('londres') || payloadText.includes('london')) {
      task = 'london';
      const days = ['lunes', 'martes', 'miercoles', 'miércoles', 'jueves', 'viernes', 'sabado', 'sábado', 'domingo'];
      const foundDay = days.find(d => payloadText.includes(d));
      if (foundDay) {
        params.day = foundDay;
      }
    }

    // 8) travisTEC predecir la cantidad de crimenes por dia en chicago (día de la semana)
    else if (payloadText.includes('chicago')) {
      task = 'chicago';
      const days = ['lunes', 'martes', 'miercoles', 'miércoles', 'jueves', 'viernes', 'sabado', 'sábado', 'domingo'];
      const foundDay = days.find(d => payloadText.includes(d));
      if (foundDay) {
        params.day = foundDay;
      }
    }

    // 9) travisTEC clasifica el tipo de cirrosis de un paciente
    else if (payloadText.includes('cirrosis')) {
      task = 'cirrhosis';
      // Extraer valores si se dan parámetros numéricos
      if (numbers.length > 0) {
        params.features = numbers.map(n => parseFloat(n));
      }
    }

    // 10) travisTEC Predecir el precio de los viajes de un avion (lugar y mes)
    else if (payloadText.includes('avion') || payloadText.includes('avión') || payloadText.includes('vuelo')) {
      task = 'airline';
      // Extraer mes
      const months = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
        'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
      };
      const foundMonth = Object.keys(months).find(m => payloadText.includes(m));
      if (foundMonth) {
        params.month = months[foundMonth];
      } else if (numbers.length > 0) {
        params.month = parseInt(numbers[0], 10);
      }
      
      // Extraer lugar
      const placeMatch = payloadText.match(/(?:desde|a|hacia|para)\s+([a-záéíóúñ]+)/i);
      if (placeMatch) {
        params.location = placeMatch[1];
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

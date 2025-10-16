import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CameraCapture from '../components/CameraCapture';
import AudioRecorder from '../components/AudioRecorder';
import EmotionDisplay from '../components/EmotionDisplay';
import { apiClient } from '../services/api-client';
import './Capture.css';

function Capture() {
  // Estados separados para cada sistema
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [isAudioActive, setIsAudioActive] = useState(false);
  const [currentEmotions, setCurrentEmotions] = useState(null);
  
  // REGISTROS SEPARADOS PARA CADA SISTEMA
  const [faceRecognitionLogs, setFaceRecognitionLogs] = useState([]); // 📸 Logs de reconocimiento facial
  const [voiceCommandLogs, setVoiceCommandLogs] = useState([]); // 🎤 Logs de comandos de voz
  
  const [snapshotPreview, setSnapshotPreview] = useState(null);
  const navigate = useNavigate();

  // Función para agregar log al sistema de RECONOCIMIENTO FACIAL
  const addFaceLog = (message, type = 'info') => {
    const newLog = {
      id: Date.now(),
      message,
      type,
      timestamp: new Date().toLocaleTimeString(),
      system: 'face'
    };
    setFaceRecognitionLogs(prev => [newLog, ...prev].slice(0, 20));
  };

  // Función para agregar log al sistema de COMANDOS DE VOZ
  const addVoiceLog = (message, type = 'info') => {
    const newLog = {
      id: Date.now() + 1, // +1 para evitar IDs duplicados
      message,
      type,
      timestamp: new Date().toLocaleTimeString(),
      system: 'voice'
    };
    setVoiceCommandLogs(prev => [newLog, ...prev].slice(0, 20));
  };

  // Controles para el sistema de CÁMARA (emociones)
  const handleStartCamera = () => {
    setIsCameraActive(true);
    addFaceLog('📸 Sistema de reconocimiento facial INICIADO', 'success');
  };

  const handleStopCamera = () => {
    setIsCameraActive(false);
    setCurrentEmotions(null);
    addFaceLog('📸 Sistema de reconocimiento facial DETENIDO', 'info');
  };

  // Controles para el sistema de AUDIO (comandos de voz)
  const handleStartAudio = () => {
    setIsAudioActive(true);
    addVoiceLog('🎤 Sistema de comandos de voz INICIADO', 'success');
  };

  const handleStopAudio = () => {
    setIsAudioActive(false);
    addVoiceLog('🎤 Sistema de comandos de voz DETENIDO', 'info');
  };

  const handleSnapshot = (imageBlob) => {
    const url = URL.createObjectURL(imageBlob);
    setSnapshotPreview(url);
    addFaceLog('📷 Foto capturada correctamente', 'success');
    
    // Limpiar URL después de 30 segundos
    setTimeout(() => URL.revokeObjectURL(url), 30000);
  };

  const handleEmotionDetected = async (imageBlob) => {
    try {
      const faceData = await apiClient.recognizeFace(imageBlob);
      
      if (faceData.attributes && faceData.attributes.emotion) {
        setCurrentEmotions(faceData.attributes.emotion);
        addFaceLog(`😊 Emoción detectada: ${faceData.dominant_emotion || 'N/A'}`, 'success');
      } else if (faceData.dominant_emotion) {
        // Formato simple del mock
        const emotions = faceData.details || { [faceData.dominant_emotion]: 0.8 };
        setCurrentEmotions(emotions);
        addFaceLog(`😊 Emoción detectada: ${faceData.dominant_emotion}`, 'success');
      } else {
        addFaceLog(faceData.message || 'No se detectó rostro', 'warning');
      }
    } catch (error) {
      console.error('Error procesando rostro:', error);
      addFaceLog(`❌ Error: ${error.message}`, 'error');
    }
  };

  const handleTranscription = async (audioOrText) => {
    try {
      console.log('📝 handleTranscription llamado con:', audioOrText);
      if (typeof audioOrText === 'string') {
        // Ya es texto del Web Speech API
        addVoiceLog(`🎤 Transcripción: "${audioOrText}"`, 'info');
      } else {
        // Es un Blob, enviarlo al backend
        const transcription = await apiClient.transcribeAudio(audioOrText);
        addVoiceLog(`🎤 Transcripción: "${transcription}"`, 'info');
      }
    } catch (error) {
      console.error('❌ Error transcribiendo:', error);
      addVoiceLog(`❌ Error transcribiendo: ${error.message}`, 'error');
    }
  };

  const handleCommand = async (command) => {
    try {
      console.log('🎯 handleCommand llamado con:', command);
      addVoiceLog(`🎯 Comando parseado: ${command.task || 'desconocido'}`, 'info');
      
      const response = await apiClient.processCommand(command);
      console.log('✅ Respuesta del servidor:', response);
      
      addVoiceLog(`✅ ${response}`, 'success');
    } catch (error) {
      console.error('❌ Error procesando comando:', error);
      addVoiceLog(`❌ Error: ${error.message}`, 'error');
    }
  };

  const goToResults = () => {
    navigate('/results', { 
      state: { 
        faceRecognitionLogs, 
        voiceCommandLogs,
        emotions: currentEmotions 
      } 
    });
  };

  // 🔧 FUNCIÓN DE PRUEBA - Llama directamente al API sin voz
  const testCommand = async (commandName) => {
    const testCommands = {
      bitcoin: { task: 'bitcoin', text: 'bitcoin 7', params: { days: 7 } },
      movie: { task: 'movie', text: 'película', params: {} },
      car: { task: 'car', text: 'coche 2020 50000', params: { year: 2020, km: 50000 } },
      bmi: { task: 'bmi', text: 'imc 1.75 75 30', params: { height: 1.75, weight: 75, age: 30 } },
      london: { task: 'london', text: 'londres viernes', params: { day: 'viernes' } }
    };

    const command = testCommands[commandName];
    addVoiceLog(`🧪 Enviando comando de prueba: ${commandName}`, 'info');
    
    try {
      console.log('🧪 TEST - Enviando:', command);
      const response = await apiClient.processCommand(command);
      console.log('🧪 TEST - Respuesta:', response);
      addVoiceLog(`✅ ${response}`, 'success');
    } catch (error) {
      console.error('🧪 TEST - Error:', error);
      addVoiceLog(`❌ Error en prueba: ${error.message}`, 'error');
    }
  };

  return (
    <div className="capture-page">
      <div className="capture-header">
        <h1>JarvisTEC - Sistemas Inteligentes</h1>
        <p>Controla cada sistema de forma independiente</p>
      </div>

      {/* SECCIÓN 1: RECONOCIMIENTO FACIAL Y EMOCIONES */}
      <div className="system-section camera-section">
        <div className="section-header">
          <h2>📸 Sistema de Reconocimiento Facial</h2>
          <p>Detecta emociones en tiempo real usando la cámara</p>
        </div>

        <div className="controls">
          {!isCameraActive ? (
            <button onClick={handleStartCamera} className="btn btn-start">
              ▶️ Activar Cámara
            </button>
          ) : (
            <button onClick={handleStopCamera} className="btn btn-stop">
              ⏹️ Detener Cámara
            </button>
          )}
        </div>

        <div className="system-content">
          <div className="camera-container">
            <CameraCapture 
              isActive={isCameraActive}
              onSnapshot={handleSnapshot}
              onEmotionDetected={handleEmotionDetected}
            />
            
            {snapshotPreview && (
              <div className="snapshot-preview">
                <h3>Última captura</h3>
                <img src={snapshotPreview} alt="Snapshot preview" />
              </div>
            )}
          </div>

          <div className="emotions-container">
            <h3>Emociones Detectadas</h3>
            <EmotionDisplay emotions={currentEmotions} />
          </div>
        </div>

        {/* LOG DE RECONOCIMIENTO FACIAL - DEBAJO DE LA CÁMARA */}
        <div className="logs-section-inline facial-logs-inline">
          <h3>📋 Registro de Actividad</h3>
          <div className="logs-container">
            {faceRecognitionLogs.length === 0 ? (
              <p className="no-logs">No hay actividad de reconocimiento facial. Activa la cámara para comenzar.</p>
            ) : (
              faceRecognitionLogs.map(log => (
                <div key={log.id} className={`log-entry ${log.type}`}>
                  <span className="timestamp">[{log.timestamp}]</span>
                  <span className="log-icon">📸</span>
                  <span className="message">{log.message}</span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* SEPARADOR */}
      <div className="system-separator"></div>

      {/* SECCIÓN 2: COMANDOS DE VOZ */}
      <div className="system-section audio-section">
        <div className="section-header">
          <h2>🎤 Sistema de Comandos de Voz</h2>
          <p>Habla comandos para obtener predicciones y recomendaciones</p>
        </div>

        <div className="controls">
          {!isAudioActive ? (
            <button onClick={handleStartAudio} className="btn btn-start">
              ▶️ Activar Micrófono
            </button>
          ) : (
            <button onClick={handleStopAudio} className="btn btn-stop">
              ⏹️ Detener Micrófono
            </button>
          )}
        </div>

        <div className="system-content">
          <div className="audio-container">
            <AudioRecorder 
              isActive={isAudioActive}
              onTranscription={handleTranscription}
              onCommand={handleCommand}
            />
          </div>

          {/* LOG DE COMANDOS DE VOZ - AL LADO DEL MICRÓFONO */}
          <div className="logs-section-inline voice-logs-inline">
            <h3>📋 Registro de Actividad</h3>
            <div className="logs-container">
              {voiceCommandLogs.length === 0 ? (
                <p className="no-logs">No hay actividad de comandos de voz. Activa el micrófono para comenzar.</p>
              ) : (
                voiceCommandLogs.map(log => (
                  <div key={log.id} className={`log-entry ${log.type}`}>
                    <span className="timestamp">[{log.timestamp}]</span>
                    <span className="log-icon">🎤</span>
                    <span className="message">{log.message}</span>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>

      {/* BOTÓN DE RESULTADOS */}
      <div className="results-button-container">
        <button onClick={goToResults} className="btn btn-secondary btn-large">
          📊 Ver Estadísticas y Resultados
        </button>
      </div>
    </div>
  );
}

export default Capture;

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
  const [logs, setLogs] = useState([]);
  const [snapshotPreview, setSnapshotPreview] = useState(null);
  const navigate = useNavigate();

  const addLog = (message, type = 'info') => {
    const newLog = {
      id: Date.now(),
      message,
      type,
      timestamp: new Date().toLocaleTimeString()
    };
    setLogs(prev => [newLog, ...prev].slice(0, 20));
  };

  // Controles para el sistema de CÁMARA (emociones)
  const handleStartCamera = () => {
    setIsCameraActive(true);
    addLog('📸 Sistema de reconocimiento facial INICIADO', 'success');
  };

  const handleStopCamera = () => {
    setIsCameraActive(false);
    setCurrentEmotions(null);
    addLog('📸 Sistema de reconocimiento facial DETENIDO', 'info');
  };

  // Controles para el sistema de AUDIO (comandos de voz)
  const handleStartAudio = () => {
    setIsAudioActive(true);
    addLog('🎤 Sistema de comandos de voz INICIADO', 'success');
  };

  const handleStopAudio = () => {
    setIsAudioActive(false);
    addLog('🎤 Sistema de comandos de voz DETENIDO', 'info');
  };

  const handleSnapshot = (imageBlob) => {
    const url = URL.createObjectURL(imageBlob);
    setSnapshotPreview(url);
    addLog('Foto capturada', 'success');
    
    // Limpiar URL después de 30 segundos
    setTimeout(() => URL.revokeObjectURL(url), 30000);
  };

  const handleEmotionDetected = async (imageBlob) => {
    try {
      const faceData = await apiClient.recognizeFace(imageBlob);
      
      if (faceData.attributes && faceData.attributes.emotion) {
        setCurrentEmotions(faceData.attributes.emotion);
        addLog(`Emoción detectada: ${faceData.dominant_emotion || 'N/A'}`, 'success');
      } else if (faceData.dominant_emotion) {
        // Formato simple del mock
        const emotions = faceData.details || { [faceData.dominant_emotion]: 0.8 };
        setCurrentEmotions(emotions);
        addLog(`Emoción detectada: ${faceData.dominant_emotion}`, 'success');
      } else {
        addLog(faceData.message || 'No se detectó rostro', 'warning');
      }
    } catch (error) {
      console.error('Error procesando rostro:', error);
      addLog(`Error: ${error.message}`, 'error');
    }
  };

  const handleTranscription = async (audioOrText) => {
    try {
      console.log('📝 handleTranscription llamado con:', audioOrText);
      if (typeof audioOrText === 'string') {
        // Ya es texto del Web Speech API
        addLog(`🎤 Transcripción: ${audioOrText}`, 'info');
      } else {
        // Es un Blob, enviarlo al backend
        const transcription = await apiClient.transcribeAudio(audioOrText);
        addLog(`🎤 Transcripción: ${transcription}`, 'info');
      }
    } catch (error) {
      console.error('❌ Error transcribiendo:', error);
      addLog(`❌ Error transcribiendo: ${error.message}`, 'error');
    }
  };

  const handleCommand = async (command) => {
    try {
      console.log('🎯 handleCommand llamado con:', command);
      addLog(`🎯 Comando parseado: ${JSON.stringify(command)}`, 'info');
      
      const response = await apiClient.processCommand(command);
      console.log('✅ Respuesta del servidor:', response);
      
      addLog(`✅ Respuesta: ${response}`, 'success');
    } catch (error) {
      console.error('❌ Error procesando comando:', error);
      addLog(`❌ Error procesando comando: ${error.message}`, 'error');
    }
  };

  const goToResults = () => {
    navigate('/results', { 
      state: { 
        logs, 
        emotions: currentEmotions 
      } 
    });
  };

  // 🔧 FUNCIÓN DE PRUEBA - Llama directamente al API sin voz
  const testCommand = async (commandName) => {
    const testCommands = {
      bitcoin: { task: 'bitcoin', text: 'bitcoin', params: {} },
      movie: { task: 'movie', text: 'película matrix', params: { title: 'matrix' } },
      car: { task: 'car', text: 'coche 2020 50000', params: { year: 2020, km: 50000 } },
      bmi: { task: 'bmi', text: 'imc 180 75 30', params: { height: 180, weight: 75, age: 30 } },
      london: { task: 'london', text: 'londres viernes', params: { day: 'viernes' } }
    };

    const command = testCommands[commandName];
    addLog(`🧪 TEST: Enviando comando ${commandName}`, 'info');
    
    try {
      console.log('🧪 TEST - Enviando:', command);
      const response = await apiClient.processCommand(command);
      console.log('🧪 TEST - Respuesta:', response);
      addLog(`✅ TEST OK: ${response}`, 'success');
    } catch (error) {
      console.error('🧪 TEST - Error:', error);
      addLog(`❌ TEST ERROR: ${error.message}`, 'error');
    }
  };

  return (
    <div className="capture-page">
      <div className="capture-header">
        <h1>🤖 TravisTEC - Sistemas Inteligentes</h1>
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
            
            <div className="commands-help">
              <h3>Comandos Disponibles:</h3>
              <ul>
                <li>"TravisTEC bitcoin" - Precio de Bitcoin</li>
                <li>"TravisTEC película matrix" - Recomendaciones</li>
                <li>"TravisTEC imc 180 75 30" - Cálculo IMC</li>
                <li>"TravisTEC Londres viernes" - Crímenes</li>
                <li>+ 6 comandos más...</li>
              </ul>
            </div>

            {/* 🔧 PANEL DE PRUEBAS */}
            <div className="test-panel">
              <h3>🧪 Pruebas sin Micrófono</h3>
              <p>Haz clic para probar la conexión directamente:</p>
              <div className="test-buttons">
                <button onClick={() => testCommand('bitcoin')} className="btn-test">
                  💰 Bitcoin
                </button>
                <button onClick={() => testCommand('movie')} className="btn-test">
                  🎬 Película
                </button>
                <button onClick={() => testCommand('car')} className="btn-test">
                  🚗 Auto
                </button>
                <button onClick={() => testCommand('bmi')} className="btn-test">
                  💪 IMC
                </button>
                <button onClick={() => testCommand('london')} className="btn-test">
                  🇬🇧 Londres
                </button>
              </div>
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

      {/* LOGS COMPARTIDOS */}
      <div className="logs-section">
        <h2>📋 Registro de Actividad (Ambos Sistemas)</h2>
        <div className="logs-container">
          {logs.length === 0 ? (
            <p className="no-logs">No hay actividad aún. Activa algún sistema para comenzar.</p>
          ) : (
            logs.map(log => (
              <div key={log.id} className={`log-entry ${log.type}`}>
                <span className="timestamp">[{log.timestamp}]</span>
                <span className="message">{log.message}</span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

export default Capture;

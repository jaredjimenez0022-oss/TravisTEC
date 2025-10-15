import { Link } from 'react-router-dom';
import './Home.css';

function Home() {
  return (
    <div className="home-container">
      <div className="hero">
        <h1>🤖 Jarvis TEC</h1>
        <p className="subtitle">Asistente inteligente con reconocimiento facial y procesamiento de voz</p>
      </div>

      <div className="features">
        <div className="feature-card">
          <h2>📸 Reconocimiento Facial</h2>
          <p>Detecta emociones en tiempo real usando Azure Face API</p>
        </div>
        
        <div className="feature-card">
          <h2>🎤 Procesamiento de Voz</h2>
          <p>Transcripción de audio y procesamiento de comandos con IA</p>
        </div>
        
        <div className="feature-card">
          <h2>🧠 Modelos ML</h2>
          <p>Predicciones basadas en múltiples modelos de machine learning</p>
        </div>
      </div>

      <div className="cta-section">
        <h2>Comienza ahora</h2>
        <div className="button-group">
          <Link to="/capture" className="btn btn-primary">
            Iniciar Captura
          </Link>
          <Link to="/results" className="btn btn-secondary">
            Ver Resultados
          </Link>
        </div>
      </div>

      <div className="info-section">
        <h3>¿Cómo funciona?</h3>
        <ol>
          <li>Inicia la captura de cámara y audio</li>
          <li>El sistema analiza las emociones faciales en tiempo real</li>
          <li>Da comandos de voz para interactuar con el asistente</li>
          <li>Visualiza los resultados y predicciones</li>
        </ol>
      </div>
    </div>
  );
}

export default Home;

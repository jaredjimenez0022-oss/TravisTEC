import { useLocation, Link } from 'react-router-dom';
import EmotionDisplay from '../components/EmotionDisplay';
import './Results.css';

function Results() {
  const location = useLocation();
  const { logs = [], emotions = null } = location.state || {};

  const getLogStats = () => {
    const stats = {
      total: logs.length,
      success: logs.filter(l => l.type === 'success').length,
      error: logs.filter(l => l.type === 'error').length,
      info: logs.filter(l => l.type === 'info').length,
      warning: logs.filter(l => l.type === 'warning').length
    };
    return stats;
  };

  const stats = getLogStats();

  return (
    <div className="results-page">
      <div className="results-header">
        <h1>📊 Resultados de la Sesión</h1>
        <p>Análisis detallado de la captura realizada</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card total">
          <div className="stat-icon">📝</div>
          <div className="stat-content">
            <h3>Total de Eventos</h3>
            <p className="stat-value">{stats.total}</p>
          </div>
        </div>

        <div className="stat-card success">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <h3>Exitosos</h3>
            <p className="stat-value">{stats.success}</p>
          </div>
        </div>

        <div className="stat-card error">
          <div className="stat-icon">❌</div>
          <div className="stat-content">
            <h3>Errores</h3>
            <p className="stat-value">{stats.error}</p>
          </div>
        </div>

        <div className="stat-card info">
          <div className="stat-icon">ℹ️</div>
          <div className="stat-content">
            <h3>Informativos</h3>
            <p className="stat-value">{stats.info}</p>
          </div>
        </div>
      </div>

      <div className="results-content">
        <div className="emotions-result">
          <h2>Última Emoción Detectada</h2>
          <EmotionDisplay emotions={emotions} />
        </div>

        <div className="logs-result">
          <h2>Registro Completo</h2>
          <div className="logs-list">
            {logs.length === 0 ? (
              <div className="empty-state">
                <p>No hay registros de actividad</p>
                <Link to="/capture" className="btn btn-primary">
                  Iniciar Captura
                </Link>
              </div>
            ) : (
              logs.map(log => (
                <div key={log.id} className={`log-item ${log.type}`}>
                  <span className="log-timestamp">{log.timestamp}</span>
                  <span className="log-type">{log.type.toUpperCase()}</span>
                  <span className="log-message">{log.message}</span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      <div className="actions">
        <Link to="/capture" className="btn btn-primary">
          🔄 Nueva Captura
        </Link>
        <Link to="/" className="btn btn-secondary">
          🏠 Volver al Inicio
        </Link>
      </div>
    </div>
  );
}

export default Results;

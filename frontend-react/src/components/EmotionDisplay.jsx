import PropTypes from 'prop-types';
import './EmotionDisplay.css';

function EmotionDisplay({ emotions }) {
  if (!emotions || Object.keys(emotions).length === 0) {
    return (
      <div className="emotion-display empty">
        <p>No se detectaron emociones</p>
      </div>
    );
  }

  // Obtener la emoción dominante
  const dominant = Object.entries(emotions).reduce((a, b) => 
    a[1] > b[1] ? a : b
  );

  // Mapeo de emociones a emojis
  const emotionEmojis = {
    happiness: '😊',
    joy: '😊',
    sadness: '😢',
    anger: '😠',
    fear: '😨',
    surprise: '😲',
    neutral: '😐',
    disgust: '🤢',
    contempt: '😒'
  };

  // Ordenar emociones por valor
  const sortedEmotions = Object.entries(emotions)
    .sort((a, b) => b[1] - a[1]);

  return (
    <div className="emotion-display">
      <div className="dominant-emotion">
        <div className="emoji">
          {emotionEmojis[dominant[0]] || '🙂'}
        </div>
        <h3>{dominant[0]}</h3>
        <p className="confidence">{(dominant[1] * 100).toFixed(1)}%</p>
      </div>

      <div className="emotion-bars">
        {sortedEmotions.map(([emotion, value]) => (
          <div key={emotion} className="emotion-bar">
            <div className="emotion-label">
              <span>{emotionEmojis[emotion] || '🙂'}</span>
              <span className="emotion-name">{emotion}</span>
            </div>
            <div className="bar-container">
              <div 
                className="bar-fill" 
                style={{ width: `${value * 100}%` }}
              />
            </div>
            <span className="value">{(value * 100).toFixed(1)}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}

EmotionDisplay.propTypes = {
  emotions: PropTypes.object
};

export default EmotionDisplay;

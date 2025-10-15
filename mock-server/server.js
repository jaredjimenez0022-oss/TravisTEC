const express = require('express');
const cors = require('cors');
const multer = require('multer');

const app = express();
const port = 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Configurar multer para archivos
const upload = multer({ storage: multer.memoryStorage() });

// Mock data
const mockEmotions = [
  { happiness: 0.85, sadness: 0.05, anger: 0.03, surprise: 0.04, neutral: 0.03 },
  { neutral: 0.70, happiness: 0.20, sadness: 0.05, surprise: 0.03, anger: 0.02 },
  { surprise: 0.80, happiness: 0.10, neutral: 0.05, fear: 0.03, sadness: 0.02 },
  { sadness: 0.75, neutral: 0.15, anger: 0.05, happiness: 0.03, fear: 0.02 },
  { anger: 0.70, disgust: 0.15, sadness: 0.08, neutral: 0.05, contempt: 0.02 }
];

const mockResponses = [
  "El precio de Bitcoin en los próximos 5 años se estima en $85,000 con tendencia alcista.",
  "Basado en el análisis, el aguacate tendrá un precio promedio de $2.50 por unidad.",
  "La película recomendada para ti es 'Inception' con una puntuación de 8.8/10.",
  "El índice S&P 500 muestra una tendencia positiva del 12% anual.",
  "Para un automóvil del año 2018 con 50,000 km, el precio estimado es $18,500.",
  "Tu índice de masa corporal (IMC) es 24.5, dentro del rango saludable.",
  "El nivel de crimen en Londres para ese día es medio-bajo, categoría 3.",
  "La probabilidad de retraso para un vuelo en ese mes es del 25%.",
  "Análisis completado exitosamente. Procesando datos adicionales...",
  "Comando ejecutado. Resultado disponible para visualización."
];

// Helper para obtener emoción aleatoria
const getRandomEmotion = () => {
  const emotion = mockEmotions[Math.floor(Math.random() * mockEmotions.length)];
  const dominant = Object.entries(emotion).reduce((a, b) => a[1] > b[1] ? a : b);
  return {
    dominant_emotion: dominant[0],
    face_detected: true,
    face_count: 1,
    attributes: { emotion },
    details: emotion
  };
};

// Helper para obtener respuesta aleatoria
const getRandomResponse = () => {
  return mockResponses[Math.floor(Math.random() * mockResponses.length)];
};

// ===== ENDPOINTS =====

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    services: {
      mock_server: 'running',
      face_api: 'mock',
      speech_api: 'mock',
      ml_models: 'mock'
    }
  });
});

// Transcribe audio (mock)
app.post('/api/v1/transcribe', upload.single('audio'), (req, res) => {
  const mockTranscriptions = [
    "TravisTEC predice el precio de Bitcoin para los próximos 5 años",
    "TravisTEC calcula el índice de masa corporal con altura 175 y peso 70",
    "TravisTEC recomienda una película de ciencia ficción",
    "TravisTEC analiza el precio del aguacate",
    "TravisTEC predice el valor del S P 500"
  ];
  
  const transcription = mockTranscriptions[Math.floor(Math.random() * mockTranscriptions.length)];
  
  res.json({
    transcription,
    confidence: 0.95,
    language: 'es-ES',
    duration_ms: 2500
  });
});

// Recognize face / sentiment (mock)
app.post('/api/v1/face/sentiment', upload.single('image'), (req, res) => {
  const emotionData = getRandomEmotion();
  
  // Simular delay de API real
  setTimeout(() => {
    res.json(emotionData);
  }, 300);
});

// Process command (mock)
app.post('/api/v1/command/execute', (req, res) => {
  const { text, task, params } = req.body;
  
  let response = '';
  
  // Respuestas específicas según el comando
  switch(task) {
    case 'bitcoin':
      response = `📈 Predicción Bitcoin: $${(Math.random() * 20000 + 40000).toFixed(2)}. Tendencia: ${Math.random() > 0.5 ? 'ALCISTA 🚀' : 'LATERAL ➡️'}`;
      break;
      
    case 'movie':
      const movieTitle = params.title || 'matrix';
      const movies = ['The Matrix Reloaded', 'Inception', 'Interstellar', 'The Prestige', 'Blade Runner 2049'];
      response = `🎬 Películas similares a "${movieTitle}":\n${movies.slice(0, 3).map((m, i) => `${i+1}. ${m}`).join('\n')}`;
      break;
      
    case 'car':
      const year = params.year || 2020;
      const km = params.km || 50000;
      const price = (35000 - (2024 - year) * 2000 - km / 10).toFixed(2);
      response = `🚗 Auto ${year} con ${km}km: Precio estimado $${price}`;
      break;
      
    case 'sp500':
      const years = params.years || 2;
      const prediction = (4500 * Math.pow(1.08, years)).toFixed(2);
      response = `📊 S&P 500 en ${years} años: ${prediction} puntos (crecimiento anual ~8%)`;
      break;
      
    case 'bmi':
      const height = params.height || 170;
      const weight = params.weight || 70;
      const age = params.age || 30;
      const bmi = (weight / ((height/100) ** 2)).toFixed(1);
      const bodyfat = (1.20 * bmi + 0.23 * age - 10.8).toFixed(1);
      response = `💪 IMC: ${bmi} | Grasa corporal: ${bodyfat}% (Altura: ${height}cm, Peso: ${weight}kg, Edad: ${age} años)`;
      break;
      
    case 'avocado':
      const avgPrice = (Math.random() * 1 + 1.5).toFixed(2);
      response = `🥑 Precio del aguacate: $${avgPrice} por unidad. Tendencia: ${Math.random() > 0.5 ? 'ESTABLE' : 'AL ALZA'}`;
      break;
      
    case 'london':
      const dayLondon = params.day || 'viernes';
      const crimesLondon = Math.floor(Math.random() * 100 + 300);
      response = `🇬🇧 Crímenes estimados en Londres el ${dayLondon}: ${crimesLondon} incidentes. Nivel de riesgo: ${crimesLondon > 350 ? 'ALTO' : 'MEDIO'}`;
      break;
      
    case 'chicago':
      const dayChicago = params.day || 'lunes';
      const crimesChicago = Math.floor(Math.random() * 150 + 400);
      response = `🇺🇸 Crímenes estimados en Chicago el ${dayChicago}: ${crimesChicago} incidentes. Nivel de riesgo: ${crimesChicago > 500 ? 'ALTO' : 'MEDIO'}`;
      break;
      
    case 'cirrhosis':
      const types = ['Cirrosis compensada (Estadio 1-2)', 'Cirrosis descompensada (Estadio 3-4)', 'Hepatitis crónica'];
      const type = types[Math.floor(Math.random() * types.length)];
      const confidence = (Math.random() * 0.3 + 0.65).toFixed(2);
      response = `🏥 Clasificación: ${type}. Confianza del modelo: ${(confidence * 100).toFixed(0)}%`;
      break;
      
    case 'airline':
      const location = params.location || 'Miami';
      const month = params.month || 7;
      const monthNames = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
      const flightPrice = Math.floor(Math.random() * 300 + 200);
      response = `✈️ Vuelo a ${location} en ${monthNames[month-1]}: $${flightPrice}. Probabilidad de retraso: ${Math.floor(Math.random() * 40 + 10)}%`;
      break;
      
    default:
      response = `❓ Comando no reconocido: "${task}". Comandos disponibles: bitcoin, movie, car, sp500, bmi, avocado, london, chicago, cirrhosis, airline`;
  }
  
  res.json({
    response,
    task: task || 'unknown',
    params: params || {},
    processed_at: new Date().toISOString(),
    confidence: 0.92
  });
});

// Calculate BMI (mock)
app.post('/api/v1/bmi', (req, res) => {
  const { height, weight, age } = req.body;
  
  if (!height || !weight) {
    return res.status(400).json({
      error: 'Missing required parameters',
      detail: 'height and weight are required'
    });
  }
  
  const bmi = (weight / (height * height)).toFixed(2);
  const bodyfat = (1.20 * bmi + 0.23 * (age || 25) - 10.8).toFixed(2);
  
  res.json({
    bmi: parseFloat(bmi),
    bodyfat: parseFloat(bodyfat),
    units: 'kg/m²',
    method: 'mock_calculation',
    height,
    weight,
    age: age || 25
  });
});

// Predict stock price (mock)
app.post('/api/v1/predict/stock', (req, res) => {
  const { symbol, years } = req.body;
  
  const predictions = Array.from({ length: years || 5 }, (_, i) => ({
    year: new Date().getFullYear() + i + 1,
    predicted_price: (Math.random() * 50000 + 30000).toFixed(2),
    confidence: (Math.random() * 0.3 + 0.7).toFixed(2)
  }));
  
  res.json({
    symbol: symbol || 'BTC',
    predictions,
    model: 'mock_lstm'
  });
});

// Movie recommendation (mock)
app.post('/api/v1/recommend/movie', (req, res) => {
  const mockMovies = [
    { title: 'Inception', rating: 8.8, genre: 'Sci-Fi', year: 2010 },
    { title: 'The Matrix', rating: 8.7, genre: 'Sci-Fi', year: 1999 },
    { title: 'Interstellar', rating: 8.6, genre: 'Sci-Fi', year: 2014 },
    { title: 'The Dark Knight', rating: 9.0, genre: 'Action', year: 2008 },
    { title: 'Pulp Fiction', rating: 8.9, genre: 'Crime', year: 1994 }
  ];
  
  const movie = mockMovies[Math.floor(Math.random() * mockMovies.length)];
  
  res.json({
    recommendation: movie,
    confidence: 0.88,
    model: 'mock_collaborative_filtering'
  });
});

// Error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Internal server error',
    detail: err.message
  });
});

// Start server
app.listen(port, () => {
  console.log(`🚀 Mock Server running at http://localhost:${port}`);
  console.log(`📝 Available endpoints:`);
  console.log(`   GET  /api/health`);
  console.log(`   POST /api/v1/transcribe`);
  console.log(`   POST /api/v1/face/sentiment`);
  console.log(`   POST /api/v1/command/execute`);
  console.log(`   POST /api/v1/bmi`);
  console.log(`   POST /api/v1/predict/stock`);
  console.log(`   POST /api/v1/recommend/movie`);
});

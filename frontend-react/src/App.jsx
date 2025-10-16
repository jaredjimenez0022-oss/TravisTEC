import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Capture from './pages/Capture';
import Results from './pages/Results';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-brand">
            <Link to="/">JarvisTEC</Link>
          </div>
          <div className="nav-links">
            <Link to="/">Inicio</Link>
            <Link to="/capture">Captura</Link>
            <Link to="/results">Resultados</Link>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/capture" element={<Capture />} />
            <Route path="/results" element={<Results />} />
          </Routes>
        </main>

        <footer className="footer">
          <p>JarvisTEC © 2025 - Asistente Inteligente con IA</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;

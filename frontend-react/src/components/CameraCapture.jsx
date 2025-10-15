import { useRef, useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import './CameraCapture.css';

function CameraCapture({ onSnapshot, onEmotionDetected, isActive }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [captureInterval, setCaptureInterval] = useState(null);

  useEffect(() => {
    if (isActive) {
      startCamera();
    } else {
      stopCamera();
    }

    return () => {
      stopCamera();
    };
  }, [isActive]);

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480 },
        audio: false
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
      
      setStream(mediaStream);

      // Captura automática cada 2 segundos
      const interval = setInterval(() => {
        captureFrame();
      }, 2000);
      
      setCaptureInterval(interval);
    } catch (error) {
      console.error('Error al iniciar cámara:', error);
      alert('No se pudo acceder a la cámara. Verifica los permisos.');
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }

    if (captureInterval) {
      clearInterval(captureInterval);
      setCaptureInterval(null);
    }
  };

  const captureFrame = () => {
    if (!videoRef.current || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const video = videoRef.current;
    
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob((blob) => {
      if (blob && onEmotionDetected) {
        onEmotionDetected(blob);
      }
    }, 'image/jpeg', 0.8);
  };

  const takeManualSnapshot = () => {
    if (!videoRef.current || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const video = videoRef.current;
    
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob((blob) => {
      if (blob) {
        if (onSnapshot) {
          onSnapshot(blob);
        }
        if (onEmotionDetected) {
          onEmotionDetected(blob);
        }
      }
    }, 'image/jpeg', 0.9);
  };

  return (
    <div className="camera-capture">
      <div className="video-container">
        <video 
          ref={videoRef} 
          autoPlay 
          playsInline
          className={isActive ? 'active' : ''}
        />
        <canvas ref={canvasRef} style={{ display: 'none' }} />
        
        {!isActive && (
          <div className="video-overlay">
            <p>Cámara inactiva</p>
          </div>
        )}
      </div>
      
      {isActive && (
        <button 
          onClick={takeManualSnapshot}
          className="snapshot-btn"
        >
          📸 Tomar Foto
        </button>
      )}
    </div>
  );
}

CameraCapture.propTypes = {
  onSnapshot: PropTypes.func,
  onEmotionDetected: PropTypes.func,
  isActive: PropTypes.bool.isRequired
};

export default CameraCapture;

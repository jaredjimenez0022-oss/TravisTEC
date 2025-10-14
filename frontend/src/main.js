// main.js - Camera + Audio + Parser + API Client
import { apiClient } from './api-client.js';

class JarvisTEC {
    constructor() {
        this.video = document.getElementById('video');
        this.canvas = document.getElementById('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.startBtn = document.getElementById('startBtn');
        this.stopBtn = document.getElementById('stopBtn');
        this.snapshotBtn = document.getElementById('snapshotBtn');
        this.snapshotPreview = document.getElementById('snapshotPreview');
        this.resultsDiv = document.getElementById('results');
        
        this.stream = null;
        this.mediaRecorder = null;
        this.isRecording = false;
    this.recognition = null;
    this.useWebSpeech = false;
        
        this.initEventListeners();
    }
    
    initEventListeners() {
        this.startBtn.addEventListener('click', () => this.start());
        this.stopBtn.addEventListener('click', () => this.stop());
        if (this.snapshotBtn) this.snapshotBtn.addEventListener('click', () => this.takeSnapshot());
    }
    
    async start() {
        try {
            // Iniciar cámara
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: true
            });
            
            this.video.srcObject = this.stream;
            this.isRecording = true;
            this.startBtn.disabled = true;
            this.stopBtn.disabled = false;
            
            // Start speech recognition if available (Web Speech API), otherwise use server-side recording
            const startedRecognition = this.startWebSpeechRecognition();
            if (startedRecognition) {
                this.useWebSpeech = true;
            } else {
                this.useWebSpeech = false;
                this.startAudioRecording();
            }
            
            // Iniciar captura de frames para reconocimiento facial
            this.captureFrames();
            
            this.addResult('Sistema iniciado correctamente');
        } catch (error) {
            console.error('Error al iniciar:', error);
            this.addResult(`Error: ${error.message}`, 'error');
        }
    }
    
    stop() {
        this.isRecording = false;
        
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
        }
        
        if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
            this.mediaRecorder.stop();
        }

        // Stop Web Speech recognition if active
        if (this.recognition) {
            try {
                this.recognition.stop();
            } catch (e) {
                console.warn('Error stopping recognition', e);
            }
            this.recognition = null;
            this.useWebSpeech = false;
        }
        
        this.startBtn.disabled = false;
        this.stopBtn.disabled = true;
        this.addResult('Sistema detenido');
    }
    
    startAudioRecording() {
        this.mediaRecorder = new MediaRecorder(this.stream);
        const audioChunks = [];
        
        this.mediaRecorder.addEventListener('dataavailable', event => {
            audioChunks.push(event.data);
        });
        
        this.mediaRecorder.addEventListener('stop', async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            await this.processAudio(audioBlob);
        });
        
        // Grabar en intervalos de 5 segundos
        this.mediaRecorder.start();
        setTimeout(() => {
            if (this.isRecording && this.mediaRecorder.state === 'recording') {
                this.mediaRecorder.stop();
                if (this.isRecording) {
                    this.startAudioRecording();
                }
            }
        }, 5000);
    }

    startWebSpeechRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            this.addResult('Web Speech API no disponible. Usando grabación de audio para transcripción.', 'info');
            return false;
        }

        this.recognition = new SpeechRecognition();
        this.recognition.lang = 'es-ES';
        this.recognition.interimResults = false;
        this.recognition.continuous = true;

        this.recognition.addEventListener('result', (event) => {
            const last = event.results[event.results.length - 1];
            if (last.isFinal) {
                const text = last[0].transcript.trim();
                this.addResult(`Reconocido: ${text}`);
                // Check for trigger word
                const parsed = this.parseCommandFromText(text);
                if (parsed) {
                    // Send structured payload
                    apiClient.processCommand(parsed).then(res => {
                        this.addResult(`Respuesta: ${res}`);
                    }).catch(e => console.error(e));
                }
            }
        });

        this.recognition.addEventListener('error', (e) => {
            console.error('Speech recognition error', e);
            this.addResult(`Speech error: ${e.error}`, 'error');
        });

        try {
            this.recognition.start();
            this.addResult('Reconocimiento por voz activado (Web Speech API)');
            this.useWebSpeech = true;
            return true;
        } catch (e) {
            console.error('No se pudo iniciar reconocimiento', e);
            this.recognition = null;
            this.useWebSpeech = false;
            return false;
        }
    }

    parseCommandFromText(text) {
        // Normalize
        const t = text.toLowerCase();
        // Accept either 'travistec' or 'travis tec'
        if (!t.includes('travistec') && !t.includes('travis tec')) return null;

        // Remove trigger word and trim
        let payloadText = t.replace('travis tec', '').replace('travistec', '').trim();

        // Simple keyword extraction
        const keywords = ['bitcoin','pelicula','automovil','coche','sp500','sp 500','masa corporal','imc','aguacate','londres','chicago','cirrosis','avion','vuelo'];
        let keyword = keywords.find(k => payloadText.includes(k));
        if (!keyword) {
            // fuzzy check: look for words
            for (const k of keywords) if (payloadText.indexOf(k.split(' ')[0]) !== -1) { keyword = k; break; }
        }

        // Extract numbers (years, km, height, weight, age)
        const numbers = payloadText.match(/\d+/g) || [];

        const params = {};
        if (numbers.length > 0) {
            // heuristic assignments
            if (keyword && (keyword.includes('bitcoin') || keyword.includes('sp500') || keyword.includes('aguacate'))) {
                params.years = parseInt(numbers[0], 10);
            } else if (keyword && (keyword.includes('automovil') || keyword.includes('coche'))) {
                params.year = parseInt(numbers[0], 10);
                if (numbers.length > 1) params.km = parseInt(numbers[1], 10);
            } else if (keyword && (keyword.includes('masa corporal') || keyword.includes('imc'))) {
                // expect height cm, weight kg, age
                if (numbers.length >= 2) {
                    params.height_cm = parseInt(numbers[0], 10);
                    params.weight_kg = parseInt(numbers[1], 10);
                }
                if (numbers.length >= 3) params.age = parseInt(numbers[2], 10);
            } else if (keyword && (keyword.includes('londres') || keyword.includes('chicago'))) {
                // day of week (1-7 or name) - keep numeric if present
                params.day = numbers[0];
            } else if (keyword && (keyword.includes('avion') || keyword.includes('vuelo'))) {
                // month as number
                params.month = numbers[0];
            }
        }

        const payload = {
            text: payloadText,
            task: keyword || 'unknown',
            params
        };

        this.addResult(`Comando parseado: ${JSON.stringify(payload)}`);
        return payload;
    }
    
    async captureFrames() {
        if (!this.isRecording) return;
        
        this.canvas.width = this.video.videoWidth;
        this.canvas.height = this.video.videoHeight;
        this.ctx.drawImage(this.video, 0, 0);
        
        // Convertir frame a blob
        this.canvas.toBlob(async (blob) => {
            if (blob) {
                await this.processFace(blob);
            }
        }, 'image/jpeg');
        
        // Capturar cada 2 segundos
        setTimeout(() => this.captureFrames(), 2000);
    }
    
    async processAudio(audioBlob) {
        try {
            const transcription = await apiClient.transcribeAudio(audioBlob);
            this.addResult(`Audio: ${transcription}`);
            
            // Procesar el comando con el modelo
            const response = await apiClient.processCommand(transcription);
            this.addResult(`Respuesta: ${response}`);
        } catch (error) {
            console.error('Error procesando audio:', error);
        }
    }
    
    async processFace(imageBlob) {
        try {
            const faceData = await apiClient.recognizeFace(imageBlob);
            if (faceData) {
                if (faceData.identified) {
                    this.addResult(`Rostro identificado: ${faceData.name} (conf: ${faceData.confidence})`);
                    if (faceData.attributes && faceData.attributes.emotion) {
                        this.addResult(`Emociones: ${JSON.stringify(faceData.attributes.emotion)}`);
                    }
                } else if (faceData.face_detected) {
                    this.addResult(`Rostro detectado (no identificado)`);
                    if (faceData.attributes && faceData.attributes.emotion) {
                        this.addResult(`Emociones: ${JSON.stringify(faceData.attributes.emotion)}`);
                    }
                } else {
                    this.addResult(`Face service: ${faceData.message || faceData.error || JSON.stringify(faceData)}`);
                }
            }
        } catch (error) {
            console.error('Error procesando rostro:', error);
        }
    }

    async takeSnapshot() {
        if (!this.stream) {
            this.addResult('La cámara no está activa. Presiona Iniciar primero.', 'error');
            return;
        }

        // Ajustar canvas al tamaño actual del video
        this.canvas.width = this.video.videoWidth || 640;
        this.canvas.height = this.video.videoHeight || 480;
        this.ctx.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);

        // Convertir a blob y a URL para preview
        this.canvas.toBlob(async (blob) => {
            if (!blob) return;
            const url = URL.createObjectURL(blob);
            if (this.snapshotPreview) this.snapshotPreview.src = url;

            // Enviar snapshot al backend y procesar la respuesta
            await this.processFace(blob);

            // liberar URL después de un tiempo
            setTimeout(() => URL.revokeObjectURL(url), 30000);
        }, 'image/jpeg');
    }
    
    addResult(message, type = 'info') {
        const resultElement = document.createElement('div');
        resultElement.className = `result ${type}`;
        resultElement.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
        this.resultsDiv.insertBefore(resultElement, this.resultsDiv.firstChild);
        
        // Mantener solo los últimos 10 resultados
        while (this.resultsDiv.children.length > 10) {
            this.resultsDiv.removeChild(this.resultsDiv.lastChild);
        }
    }
}

// Inicializar la aplicación
document.addEventListener('DOMContentLoaded', () => {
    new JarvisTEC();
});

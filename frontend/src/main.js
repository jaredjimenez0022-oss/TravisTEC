// main.js - Camera + Audio + Parser + API Client
import { apiClient } from './api-client.js';

class JarvisTEC {
    constructor() {
        this.video = document.getElementById('video');
        this.canvas = document.getElementById('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.startBtn = document.getElementById('startBtn');
        this.stopBtn = document.getElementById('stopBtn');
        this.resultsDiv = document.getElementById('results');
        
        this.stream = null;
        this.mediaRecorder = null;
        this.isRecording = false;
        
        this.initEventListeners();
    }
    
    initEventListeners() {
        this.startBtn.addEventListener('click', () => this.start());
        this.stopBtn.addEventListener('click', () => this.stop());
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
            
            // Iniciar captura de audio
            this.startAudioRecording();
            
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
            if (faceData && faceData.identified) {
                this.addResult(`Rostro detectado: ${faceData.name}`);
            }
        } catch (error) {
            console.error('Error procesando rostro:', error);
        }
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

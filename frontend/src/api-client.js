// api-client.js - Cliente para comunicarse con el backend
class APIClient {
    constructor() {
        this.baseURL = 'http://localhost:8000';
    }
    
    async transcribeAudio(audioBlob) {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'audio.webm');
        
        try {
            const response = await fetch(`${this.baseURL}/api/v1/transcribe`, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error('Error en la transcripción');
            }
            
            const data = await response.json();
            return data.transcription;
        } catch (error) {
            console.error('Error transcribiendo audio:', error);
            throw error;
        }
    }
    
    async recognizeFace(imageBlob) {
        const formData = new FormData();
        formData.append('image', imageBlob, 'frame.jpg');
        
        try {
            const response = await fetch(`${this.baseURL}/api/v1/face/sentiment`, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error('Error en el reconocimiento facial');
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error reconociendo rostro:', error);
            throw error;
        }
    }
    
    async processCommand(text) {
        try {
            // text may be a string or an object (parsed payload)
            const payload = (typeof text === 'string') ? { text } : text;

            const response = await fetch(`${this.baseURL}/api/v1/command/execute`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error('Error procesando comando');
            }

            const data = await response.json();
            // backend returns a dict - try to normalize
            if (data.response) return data.response
            if (data.result) return data.result
            if (data.transcription) return data.transcription
            return data
        } catch (error) {
            console.error('Error procesando comando:', error);
            throw error;
        }
    }
}

export const apiClient = new APIClient();

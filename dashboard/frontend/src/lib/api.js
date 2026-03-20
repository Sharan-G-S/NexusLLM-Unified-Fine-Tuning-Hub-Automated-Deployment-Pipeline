import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8080',
});

export const getStatus = () => api.get('/status');
export const startTraining = (config, deepspeed) => api.post('/train/start', { config, deepspeed });
export const stopTraining = () => api.post('/train/stop');
export const startServing = (modelPath, port) => api.post('/serve/start', { model_path: modelPath, port });
export const stopServing = () => api.post('/serve/stop');
export const listConfigs = () => api.get('/configs');

export const WS_LOGS_URL = 'ws://localhost:8080/logs/training';

export default api;

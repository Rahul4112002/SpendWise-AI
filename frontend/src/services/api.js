import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auth API
export const authAPI = {
  login: (username, password) =>
    api.post('/auth/login', new URLSearchParams({ username, password }), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }),
  register: (data) => api.post('/auth/register', data),
  getProfile: () => api.get('/auth/me'),
};

// Transactions API
export const transactionsAPI = {
  getAll: () => api.get('/transactions'),
  create: (data) => api.post('/transactions', data),
  processSMS: (smsData) => api.post('/transactions/sms-batch', smsData),
};

// Bank Statements API
export const bankStatementsAPI = {
  upload: (formData) =>
    api.post('/bank-statements/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  getAll: () => api.get('/bank-statements'),
};

// AI API
export const aiAPI = {
  analyze: () => api.post('/ai/analyze'),
  chat: (message, history) => api.post('/ai/chat', { message, history }),
  getSubscriptions: () => api.get('/ai/subscriptions'),
  getAlerts: () => api.get('/ai/alerts'),
};

export default api;

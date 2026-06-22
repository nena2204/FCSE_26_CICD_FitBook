import axios from 'axios';

const API_BASE_URL = '/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

export const trainersAPI = {
  getAll: () => apiClient.get('/trainers'),
};

export const slotsAPI = {
  getAll: () => apiClient.get('/slots'),
  getAvailable: () => apiClient.get('/slots/available'),
};

export const bookingsAPI = {
  getAll: () => apiClient.get('/bookings'),
  create: (clientName, trainingSlotId) =>
    apiClient.post('/bookings', {
      client_name: clientName,
      training_slot_id: trainingSlotId,
    }),
  delete: (bookingId) => apiClient.delete(`/bookings/${bookingId}`),
};

export const healthAPI = {
  check: () => apiClient.get('/health'),
};

export default apiClient;


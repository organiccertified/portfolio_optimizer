// API configuration for different environments
const getApiUrl = () => {
  // In production (when served from Flask), use relative URLs
  // In development, use localhost
  if (process.env.NODE_ENV === 'production') {
    return ''; // Relative URLs - same origin
  }
  return 'http://localhost:5000'; // Development
};

export const API_BASE_URL = getApiUrl();


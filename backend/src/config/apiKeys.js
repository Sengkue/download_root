import 'dotenv/config';

// Add any valid Gemini API keys here (or set GEMINI_API_KEY in your .env file)
const rawKeys = [
  process.env.GEMINI_API_KEY,
  // "AIzaSy..." // Add additional backup API keys here
];

export const API_KEYS = rawKeys.filter(key => key && key.trim() !== '' && !key.includes('YOUR_API_KEY'));



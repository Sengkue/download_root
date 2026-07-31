import { GoogleGenAI } from '@google/genai';
import { API_KEYS } from '../config/apiKeys.js';

let currentKeyIndex = 0;

export const chat = async (req, res) => {
  try {
    const { messages } = req.body;
    if (!messages || !Array.isArray(messages)) {
      return res.status(400).json({ error: 'Messages array is required' });
    }

    if (!API_KEYS || API_KEYS.length === 0) {
      console.error('Missing API_KEYS');
      return res.status(500).json({ error: 'AI features are not configured properly.' });
    }
    
    const contents = messages.map(msg => ({
      role: msg.role === 'user' ? 'user' : 'model',
      parts: [{ text: msg.content }]
    }));

    let response;
    let success = false;
    let lastError = null;
    let keysTried = 0;

    const modelsToTry = ['gemini-flash-latest', 'gemini-2.0-flash', 'gemini-2.5-flash', 'gemini-1.5-flash'];

    while (keysTried < API_KEYS.length && !success) {
      const apiKey = API_KEYS[currentKeyIndex];
      const ai = new GoogleGenAI({ apiKey });
      
      for (const modelName of modelsToTry) {
        try {
          response = await ai.models.generateContent({
            model: modelName,
            contents: contents,
            config: {
              systemInstruction: "You are a helpful, friendly AI assistant built into a media downloading app. Give concise and helpful answers. If the user asks for an image to be generated, created, or drawn, return exactly this markdown: ![image description](https://image.pollinations.ai/prompt/image_description) replacing 'image_description' with a detailed prompt of the requested image (URL-encoded). Do not use markdown code blocks for the image link.",
            }
          });
          success = true;
          break;
        } catch (error) {
          console.error(`Key at index ${currentKeyIndex} failed on model ${modelName} (status ${error.status}):`, error.message);
          lastError = error;
          if (error.status === 404) {
            continue; // Try next model name for same key
          } else {
            break; // Quota or auth error for this key
          }
        }
      }

      if (!success) {
        if ([429, 403, 400, 503].includes(lastError?.status)) {
          console.log(`Rotating to next key... (${keysTried + 1}/${API_KEYS.length} keys tried)`);
          currentKeyIndex = (currentKeyIndex + 1) % API_KEYS.length;
          keysTried++;
        } else {
          break;
        }
      }
    }

    if (success) {
      return res.json({ message: response.text });
    } else {
      console.error('All keys exhausted or failed.');
      let errorMessage = 'Failed to communicate with AI';
      
      if (lastError && lastError.status === 429) {
        errorMessage = 'The AI is currently receiving too many requests and all backup API keys have hit their rate limit. Please try again later.';
      } else if (lastError && [403, 400].includes(lastError.status)) {
        errorMessage = 'All backup API keys have been denied access or are invalid.';
      }
      
      return res.status(lastError?.status || 500).json({ error: errorMessage });
    }
  } catch (error) {
    console.error('AI Chat Error:', error);
    res.status(500).json({ error: 'Failed to communicate with AI' });
  }
};

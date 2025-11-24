import axios from 'axios';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load .env from backend directory
dotenv.config({ path: join(__dirname, '../.env') });

const DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions';
const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY;

console.log('🔑 Deepseek API Key loaded:', DEEPSEEK_API_KEY ? `${DEEPSEEK_API_KEY.substring(0, 8)}...` : 'NOT FOUND');

/**
 * Classify user intent using Deepseek
 */
export async function classifyIntent(userMessage) {
  const systemPrompt = `You are an intent classifier for a PartSelect appliance parts chat assistant.

Classify user queries into one of these intents:

1. "installation" - User asks how to install a part (e.g., "how do I install PS11752778?")
2. "compatibility" - User asks if a part works with their model (e.g., "does this work with WDT780SAEM1?")
3. "troubleshooting" - User describes a problem/symptom (e.g., "ice maker not working")
4. "product_search" - User wants to find parts (e.g., "show me dishwasher spray arms")
5. "out_of_scope" - ONLY if NOT about refrigerator/dishwasher parts (e.g., washing machines, ovens, general questions)

IMPORTANT: Be helpful! If it's about refrigerators or dishwashers, it's IN SCOPE.

Respond in JSON format:
{
  "type": "installation",
  "parameters": {
    "part_number": "PS11752778",
    "model_number": null,
    "symptom": null,
    "search_query": null
  },
  "confidence": 0.95
}`;

  try {
    const response = await axios.post(
      DEEPSEEK_API_URL,
      {
        model: 'deepseek-chat',
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: userMessage }
        ],
        temperature: 0.1,
        max_tokens: 500
      },
      {
        headers: {
          'Authorization': `Bearer ${DEEPSEEK_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 10000
      }
    );

    const content = response.data.choices[0].message.content;
    console.log('Deepseek raw response:', content);
    
    // Try to extract JSON from the response
    let intent;
    try {
      intent = JSON.parse(content);
    } catch (e) {
      // Try to find JSON in the response
      const jsonMatch = content.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        intent = JSON.parse(jsonMatch[0]);
      } else {
        throw new Error('No valid JSON found in response');
      }
    }
    
    return intent;
  } catch (error) {
    console.error('Error classifying intent:', error.response?.data || error.message);
    throw new Error('Deepseek API failed during intent classification. Please check your API key.');
  }
}

/**
 * Generate final user-facing response using Deepseek
 */
export async function generateResponse(userMessage, intent, toolResult) {
  if (intent.type === 'out_of_scope') {
    return {
      message: "I'm here to help with refrigerator and dishwasher parts only. I can assist with finding parts, checking compatibility, installation instructions, and troubleshooting appliance issues. How can I help you with your refrigerator or dishwasher?",
      data: null
    };
  }

  const systemPrompt = `You are a helpful PartSelect customer support assistant specializing in refrigerator and dishwasher parts.

Your job is to:
1. Provide clear, friendly responses
2. Use the tool results to give accurate information
3. Format responses with proper structure (bullet points, numbered steps)
4. Always stay helpful and professional
5. If showing installation steps, format them as numbered steps
6. If showing multiple parts, briefly describe each one

Context from tools: ${JSON.stringify(toolResult)}

Respond in a conversational way, but keep it concise and actionable.`;

  try {
    const response = await axios.post(
      DEEPSEEK_API_URL,
      {
        model: 'deepseek-chat',
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: userMessage }
        ],
        temperature: 0.7,
        max_tokens: 1000
      },
      {
        headers: {
          'Authorization': `Bearer ${DEEPSEEK_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );

    const message = response.data.choices[0].message.content;
    
    return {
      message,
      data: toolResult
    };
  } catch (error) {
    console.error('Error generating response:', error.response?.data || error.message);
    throw new Error('Deepseek API failed during response generation. Please check your API key.');
  }
}

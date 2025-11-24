import express from 'express';
import { processMessage } from '../services/chatService.js';

const router = express.Router();

// Main chat endpoint
router.post('/', async (req, res) => {
  try {
    const { message, conversation_id } = req.body;

    if (!message || message.trim() === '') {
      return res.status(400).json({ 
        error: 'Message is required' 
      });
    }

    console.log(`📨 Received message: "${message}"`);
    
    const response = await processMessage(message, conversation_id);
    
    res.json(response);
  } catch (error) {
    console.error('Error in chat route:', error);
    res.status(500).json({ 
      error: 'Failed to process message',
      message: error.message 
    });
  }
});

export default router;

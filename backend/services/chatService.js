import { classifyIntent, generateResponse } from './deepseekService.js';
import { executeTool } from './toolExecutor.js';

/**
 * Main chat processing pipeline
 * 1. Classify user intent
 * 2. Execute appropriate tool(s)
 * 3. Generate structured response with Deepseek
 */
export async function processMessage(userMessage, conversationId) {
  try {
    // Step 1: Classify intent
    console.log('🔍 Classifying intent...');
    const intent = await classifyIntent(userMessage);
    console.log(`✅ Intent: ${intent.type}`);

    // Step 2: Execute tool based on intent
    console.log('🔧 Executing tool...');
    const toolResult = await executeTool(intent.type, userMessage, intent.parameters);
    console.log('✅ Tool executed successfully');

    // Step 3: Generate final response
    console.log('💬 Generating response...');
    const response = await generateResponse(userMessage, intent, toolResult);
    console.log('✅ Response generated');

    return {
      type: intent.type,
      message: response.message,
      data: response.data,
      conversationId: conversationId || generateConversationId()
    };
  } catch (error) {
    console.error('Error in processMessage:', error);
    throw error;
  }
}

function generateConversationId() {
  return `conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

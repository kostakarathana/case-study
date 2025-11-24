const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';

export const getAIMessage = async (userQuery) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: userQuery,
        conversation_id: sessionStorage.getItem('conversation_id') || null
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    // Store conversation ID for future messages
    if (data.conversationId) {
      sessionStorage.setItem('conversation_id', data.conversationId);
    }

    return {
      role: "assistant",
      content: data.message,
      data: data.data
    };
  } catch (error) {
    console.error('Error calling API:', error);
    return {
      role: "assistant",
      content: "I'm sorry, I'm having trouble connecting to the server right now. Please try again in a moment."
    };
  }
};

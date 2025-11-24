import React, { useState, useEffect, useRef } from "react";
import "./ChatWindow.css";
import { getAIMessage } from "../api/api";
import { marked } from "marked";
import ProductCard from "./ProductCard";
import InstallationSteps from "./InstallationSteps";

function ChatWindow() {

  const defaultMessage = [{
    role: "assistant",
    content: "👋 Hi! I'm your PartSelect assistant. I can help you with:\n\n• Finding refrigerator & dishwasher parts\n• Installation instructions\n• Compatibility checks\n• Troubleshooting issues\n\nWhat can I help you with today?"
  }];

  const [messages,setMessages] = useState(defaultMessage)
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
      scrollToBottom();
  }, [messages]);

  const handleSend = async (inputText) => {
    const messageText = inputText || input;
    if (messageText.trim() !== "") {
      // Set user message
      setMessages(prevMessages => [...prevMessages, { role: "user", content: messageText }]);
      setInput("");
      setIsLoading(true);

      // Call API & set assistant message
      const newMessage = await getAIMessage(messageText);
      setIsLoading(false);
      setMessages(prevMessages => [...prevMessages, newMessage]);
    }
  };

  const quickActions = [
    "How do I install PS11752778?",
    "Is W10465232 compatible with WDT750SAHZ0?",
    "My ice maker is not working"
  ];

  return (
      <div className="chat-container">
          <div className="messages-container">
              {messages.map((message, index) => (
                  <div key={index} className={`${message.role}-message-container`}>
                      {message.content && (
                          <div className={`message ${message.role}-message`}>
                              <div dangerouslySetInnerHTML={{__html: marked(message.content).replace(/<p>|<\/p>/g, "")}}></div>
                          </div>
                      )}
                      
                      {/* Show product card if data exists */}
                      {message.data && message.data.part && (
                          <ProductCard part={message.data.part} />
                      )}

                      {/* Show installation steps if available */}
                      {message.data && message.data.installation_steps && (
                          <InstallationSteps steps={message.data.installation_steps} />
                      )}

                      {/* Show multiple parts if available */}
                      {message.data && message.data.parts && message.data.parts.length > 0 && (
                          <div className="parts-list">
                              {message.data.parts.map((part, idx) => (
                                  <ProductCard key={idx} part={part} />
                              ))}
                          </div>
                      )}
                  </div>
              ))}
              
              {isLoading && (
                  <div className="assistant-message-container">
                      <div className="message assistant-message loading-message">
                          <div className="typing-indicator">
                              <span></span>
                              <span></span>
                              <span></span>
                          </div>
                      </div>
                  </div>
              )}
              
              <div ref={messagesEndRef} />
          </div>

          {messages.length === 1 && (
              <div className="quick-actions">
                  <p className="quick-actions-label">Try asking:</p>
                  {quickActions.map((action, idx) => (
                      <button 
                          key={idx} 
                          className="quick-action-btn"
                          onClick={() => handleSend(action)}
                      >
                          {action}
                      </button>
                  ))}
              </div>
          )}

          <div className="input-area">
              <input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask about refrigerator or dishwasher parts..."
                  onKeyPress={(e) => {
                      if (e.key === "Enter" && !e.shiftKey) {
                          handleSend(input);
                          e.preventDefault();
                      }
                  }}
                  disabled={isLoading}
              />
              <button 
                  className="send-button" 
                  onClick={() => handleSend(input)}
                  disabled={isLoading || !input.trim()}
              >
                  {isLoading ? "..." : "Send"}
              </button>
          </div>
      </div>
  );
}

export default ChatWindow;

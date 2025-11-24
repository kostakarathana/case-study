import React from "react";
import "./ProductCard.css";

function ProductCard({ part }) {
  if (!part) return null;

  return (
    <div className="product-card">
      <div className="product-image">
        <div className="image-placeholder">
          <span className="part-icon">🔧</span>
        </div>
      </div>
      <div className="product-details">
        <h3 className="product-name">{part.name}</h3>
        <div className="product-meta">
          <span className="part-number">{part.part_number}</span>
          <span className="part-brand">{part.brand}</span>
        </div>
        <p className="product-description">{part.description}</p>
        
        {part.compatible_models && part.compatible_models.length > 0 && (
          <div className="compatibility-section">
            <span className="label">Compatible Models:</span>
            <div className="model-badges">
              {part.compatible_models.slice(0, 3).map((model, idx) => (
                <span key={idx} className="model-badge">{model}</span>
              ))}
              {part.compatible_models.length > 3 && (
                <span className="model-badge more">+{part.compatible_models.length - 3} more</span>
              )}
            </div>
          </div>
        )}

        {part.symptoms_fixed && part.symptoms_fixed.length > 0 && (
          <div className="symptoms-section">
            <span className="label">Fixes:</span>
            <ul className="symptoms-list">
              {part.symptoms_fixed.slice(0, 2).map((symptom, idx) => (
                <li key={idx}>• {symptom}</li>
              ))}
            </ul>
          </div>
        )}

        <div className="product-footer">
          <div className="price">${part.price}</div>
          <a 
            href={part.product_url} 
            target="_blank" 
            rel="noopener noreferrer"
            className="view-part-btn"
          >
            View on PartSelect →
          </a>
        </div>
      </div>
    </div>
  );
}

export default ProductCard;

import React from "react";
import "./InstallationSteps.css";

function InstallationSteps({ steps }) {
  if (!steps) return null;

  // Parse steps if it's a string
  const stepsList = typeof steps === 'string' 
    ? steps.split('\n').filter(s => s.trim())
    : steps;

  return (
    <div className="installation-steps">
      <div className="steps-header">
        <span className="steps-icon">📋</span>
        <h4>Installation Instructions</h4>
      </div>
      <ol className="steps-list">
        {stepsList.map((step, idx) => {
          // Remove leading numbers like "1. " if present
          const cleanStep = step.replace(/^\d+\.\s*/, '');
          return (
            <li key={idx} className="step-item">
              <span className="step-number">{idx + 1}</span>
              <span className="step-text">{cleanStep}</span>
            </li>
          );
        })}
      </ol>
    </div>
  );
}

export default InstallationSteps;

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const partsData = JSON.parse(
  readFileSync(join(__dirname, '../data/seedParts.json'), 'utf-8')
);

/**
 * Route to appropriate tool based on intent
 */
export async function executeTool(intentType, userMessage, parameters) {
  switch (intentType) {
    case 'installation':
      return await getInstallationSteps(parameters);
    
    case 'compatibility':
      return await checkCompatibility(parameters);
    
    case 'troubleshooting':
      return await troubleshootSymptom(parameters);
    
    case 'product_search':
      return await searchParts(parameters);
    
    case 'out_of_scope':
      return null;
    
    default:
      return await searchParts({ search_query: userMessage });
  }
}

/**
 * Search for parts by part number, keyword, or description
 */
async function searchParts(parameters) {
  const { part_number, search_query } = parameters;
  
  if (part_number) {
    const part = partsData.parts.find(p => 
      p.part_number.toLowerCase() === part_number.toLowerCase()
    );
    return part ? { parts: [part] } : { parts: [] };
  }
  
  if (search_query) {
    const query = search_query.toLowerCase();
    const results = partsData.parts.filter(part => 
      part.name.toLowerCase().includes(query) ||
      part.description.toLowerCase().includes(query) ||
      part.part_number.toLowerCase().includes(query) ||
      part.symptoms_fixed.some(symptom => symptom.toLowerCase().includes(query))
    );
    return { parts: results.slice(0, 5) }; // Limit to top 5 results
  }
  
  return { parts: [] };
}

/**
 * Get installation instructions for a part
 */
async function getInstallationSteps(parameters) {
  const { part_number } = parameters;
  
  if (!part_number) {
    return { error: 'Part number not specified' };
  }
  
  const part = partsData.parts.find(p => 
    p.part_number.toLowerCase() === part_number.toLowerCase()
  );
  
  if (!part) {
    return { error: 'Part not found', part_number };
  }
  
  return {
    part,
    installation_steps: part.install_instructions
  };
}

/**
 * Check if a part is compatible with a model
 */
async function checkCompatibility(parameters) {
  const { part_number, model_number } = parameters;
  
  if (!part_number || !model_number) {
    return { error: 'Both part number and model number are required' };
  }
  
  const part = partsData.parts.find(p => 
    p.part_number.toLowerCase() === part_number.toLowerCase()
  );
  
  if (!part) {
    return { error: 'Part not found', part_number };
  }
  
  const isCompatible = part.compatible_models.some(model => 
    model.toLowerCase() === model_number.toLowerCase()
  );
  
  return {
    part,
    model_number,
    is_compatible: isCompatible,
    compatible_models: part.compatible_models
  };
}

/**
 * Find parts that fix a specific symptom
 */
async function troubleshootSymptom(parameters) {
  const { symptom, search_query } = parameters;
  const query = (symptom || search_query || '').toLowerCase();
  
  if (!query) {
    return { parts: [] };
  }
  
  const matchingParts = partsData.parts.filter(part => 
    part.symptoms_fixed.some(s => s.toLowerCase().includes(query))
  );
  
  return {
    symptom: query,
    parts: matchingParts.slice(0, 5) // Top 5 matches
  };
}

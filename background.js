// RMG Bridge - Background Script
// Connects RMG web apps to local AI (Ollama) and services

const OLLAMA_API = 'http://localhost:11434';
let cachedModels = null;
let lastFetch = 0;
const CACHE_DURATION = 60000; // 1 minute

// Fetch Ollama models from local API
async function fetchOllamaModels() {
  const now = Date.now();
  
  // Return cached if recent
  if (cachedModels && (now - lastFetch) < CACHE_DURATION) {
    console.log('🗡️ RMG Bridge: Using cached models');
    return cachedModels;
  }
  
  try {
    console.log('🗡️ RMG Bridge: Fetching models from Ollama...');
    const response = await fetch(`${OLLAMA_API}/api/tags`);
    
    if (response.ok) {
      const data = await response.json();
      const models = data.models.map(m => m.name);
      
      cachedModels = {
        success: true,
        models: models,
        count: models.length,
        timestamp: now
      };
      lastFetch = now;
      
      console.log('✅ RMG Bridge: Fetched', models.length, 'Ollama models:', models);
      
      // Store in chrome.storage for persistence
      chrome.storage.local.set({ ollamaModels: cachedModels });
      
      return cachedModels;
    } else {
      console.log('⚠️ RMG Bridge: Ollama API returned', response.status);
    }
  } catch (error) {
    console.log('⚠️ RMG Bridge: Ollama not accessible:', error.message);
  }
  
  // Try to return previously cached models from storage
  try {
    const stored = await chrome.storage.local.get('ollamaModels');
    if (stored.ollamaModels && stored.ollamaModels.models) {
      console.log('📦 RMG Bridge: Using stored models from previous session');
      return stored.ollamaModels;
    }
  } catch (e) {
    console.log('⚠️ RMG Bridge: Could not access storage');
  }
  
  return {
    success: false,
    models: [],
    count: 0,
    error: 'Ollama not running or not accessible'
  };
}

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getOllamaModels') {
    console.log('📨 RMG Bridge: Received request for models from', sender.tab?.url || 'unknown');
    fetchOllamaModels().then(sendResponse);
    return true; // Keep channel open for async response
  }
  
  if (request.action === 'refreshModels') {
    console.log('🔄 RMG Bridge: Manual refresh requested');
    cachedModels = null; // Clear cache
    fetchOllamaModels().then(sendResponse);
    return true;
  }
  
  // Proxy Ollama API requests
  if (request.type === 'OLLAMA_API_REQUEST') {
    const { endpoint, method = 'POST', body } = request;
    
    console.log('🔄 RMG Bridge: Proxying API request to', endpoint);
    console.log('📦 RMG Bridge: Request body:', body);
    
    fetch(`${OLLAMA_API}${endpoint}`, {
      method: method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: body ? JSON.stringify(body) : undefined
    })
      .then(async response => {
        console.log('📡 RMG Bridge: Response status:', response.status, response.statusText);
        
        if (!response.ok) {
          throw new Error(`Ollama API error: ${response.status} ${response.statusText}`);
        }
        
        const text = await response.text();
        console.log('📄 RMG Bridge: Response text:', text.substring(0, 200));
        
        try {
          const data = JSON.parse(text);
          console.log('✅ RMG Bridge: Successfully parsed JSON response');
          sendResponse({
            success: true,
            data: data
          });
        } catch (parseError) {
          console.error('❌ RMG Bridge: JSON parse error:', parseError.message);
          sendResponse({
            success: false,
            error: `Failed to parse response: ${parseError.message}`
          });
        }
      })
      .catch(error => {
        console.error('❌ RMG Bridge: Fetch error:', error.message);
        sendResponse({
          success: false,
          error: error.message
        });
      });
    
    return true; // Keep channel open for async response
  }
});

// Periodically check Ollama status
setInterval(() => {
  fetchOllamaModels();
}, 30000); // Check every 30 seconds

// Initial fetch on extension load
console.log('⚔️ RMG Bridge initialized');
fetchOllamaModels();

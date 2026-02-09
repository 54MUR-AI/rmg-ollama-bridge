// RMG Ollama Bridge - Content Script
// Injects Ollama model data into RMG web pages

console.log('🗡️ RMG Ollama Bridge content script loaded on', window.location.hostname);

// Inject models into page
async function injectOllamaModels() {
  try {
    console.log('📡 RMG Bridge: Requesting models from background script...');
    const response = await chrome.runtime.sendMessage({ action: 'getOllamaModels' });
    
    // Post message to page context
    window.postMessage({
      type: 'RMG_OLLAMA_MODELS',
      source: 'rmg-ollama-bridge',
      data: response
    }, '*');
    
    if (response.success) {
      console.log('✅ RMG Bridge: Injected', response.count, 'models into page:', response.models);
    } else {
      console.log('⚠️ RMG Bridge: No models available -', response.error);
    }
  } catch (error) {
    console.error('❌ RMG Bridge error:', error);
  }
}

// Inject on load
injectOllamaModels();

// Listen for requests from the page
window.addEventListener('message', (event) => {
  // Only accept messages from same origin
  if (event.source !== window) return
  
  console.log('🔔 RMG Bridge: Received message:', event.data.type)
  
  if (event.data.type === 'RMG_REQUEST_OLLAMA_MODELS') {
    console.log('🔄 RMG Bridge: Page requested model refresh')
    injectOllamaModels()
  }
  
  // Proxy Ollama API requests
  if (event.data.type === 'RMG_OLLAMA_API_REQUEST') {
    console.log('🔄 RMG Bridge: Proxying Ollama API request to', event.data.endpoint)
    
    chrome.runtime.sendMessage({
      type: 'OLLAMA_API_REQUEST',
      endpoint: event.data.endpoint,
      method: event.data.method,
      body: event.data.body,
      requestId: event.data.requestId
    }, (response) => {
      // Send response back to page
      window.postMessage({
        type: 'RMG_OLLAMA_API_RESPONSE',
        requestId: event.data.requestId,
        success: response.success,
        data: response.data,
        error: response.error,
        source: 'rmg-ollama-bridge'
      }, '*')
      
      console.log('✅ RMG Bridge: Sent API response back to page')
    })
  }
});

// Re-inject when page becomes visible (tab switching)
document.addEventListener('visibilitychange', () => {
  if (!document.hidden) {
    console.log('👁️ RMG Bridge: Page visible, refreshing models');
    injectOllamaModels();
  }
});

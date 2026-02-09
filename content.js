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

// Listen for requests from page
window.addEventListener('message', (event) => {
  // Only accept messages from same window
  if (event.source !== window) return;
  
  console.log('🔔 RMG Bridge: Received message:', event.data.type);
  
  if (event.data.type === 'RMG_REQUEST_OLLAMA_MODELS') {
    console.log('🔄 RMG Bridge: Page requested model refresh');
    injectOllamaModels();
  }
});

// Re-inject when page becomes visible (tab switching)
document.addEventListener('visibilitychange', () => {
  if (!document.hidden) {
    console.log('👁️ RMG Bridge: Page visible, refreshing models');
    injectOllamaModels();
  }
});

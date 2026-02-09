# RMG Ollama Bridge Extension

A lightweight Chrome/Edge browser extension that detects your locally installed Ollama models and makes them available in RMG web applications (SCRP, OMNI).

## Features

- 🗡️ **Seamless Integration** - Works with all RMG apps automatically
- 🔄 **Auto-Detection** - Automatically detects locally installed Ollama models
- 📦 **Smart Caching** - Caches model list for performance
- 🔒 **Privacy First** - All data stays local, no external connections
- ⚡ **Lightweight** - Minimal resource usage

## Installation

### Chrome/Edge

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `rmg-ollama-bridge` folder
5. Extension icon will appear in your toolbar

### Firefox

1. Open Firefox and navigate to `about:debugging#/runtime/this-firefox`
2. Click "Load Temporary Add-on"
3. Select the `manifest.json` file from the extension folder
4. Extension will be loaded temporarily (until browser restart)

## How It Works

1. **Background Script** polls `http://localhost:11434/api/tags` every 30 seconds
2. **Content Script** injects model data into RMG web pages
3. **RMG Apps** listen for extension messages and update their UI
4. **Fallback** - Apps work with default models if extension not installed

## Supported Apps

- ✅ **SCRP** (Web Scraper) - `scraper.onrender.com`
- ✅ **OMNI** (Code Assistant) - `omni-lite.onrender.com`
- ✅ **Local Development** - `localhost:*`

**Note:** LDGR is not part of Ollama integration. LDGR securely stores and serves API keys for cloud AI providers (OpenAI, Anthropic, xAI, etc.) to RMG apps.

## Requirements

- Ollama installed and running locally (`http://localhost:11434`)
- Chrome, Edge, or Firefox browser
- One or more Ollama models installed

## Troubleshooting

### Extension not detecting models

1. Verify Ollama is running: `ollama list`
2. Check extension console: Right-click extension icon → "Inspect popup"
3. Look for "✅ RMG Bridge: Fetched X models" in console

### Models not showing in RMG apps

1. Open browser DevTools (F12) on the RMG site
2. Look for "🗡️ RMG Ollama Bridge" messages in console
3. Manually request refresh by reloading the page

### Permission errors

- Ensure extension has host permissions for RMG domains
- Check `manifest.json` includes the site you're trying to use

## Development

### File Structure

```
rmg-ollama-bridge/
├── manifest.json       # Extension configuration
├── background.js       # Service worker (Ollama API communication)
├── content.js          # Content script (page injection)
├── README.md          # This file
└── icons/             # Extension icons
    ├── icon16.png
    ├── icon48.png
    └── icon128.png
```

### Testing

1. Make changes to extension files
2. Go to `chrome://extensions/`
3. Click "Reload" button on the extension card
4. Refresh RMG app page to test changes

## Privacy & Security

- **No external connections** - Only communicates with local Ollama
- **No data collection** - No analytics or tracking
- **Open source** - All code is visible and auditable
- **Local only** - Extension only works with localhost Ollama

## License

MIT License - Part of the RMG Suite by Ronin Media Group

## Support

For issues or questions, contact the RMG development team.

---

**Made with 🗡️ by Ronin Media Group**

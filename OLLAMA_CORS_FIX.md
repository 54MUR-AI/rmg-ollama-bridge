# Fix Ollama 403 Forbidden Error

## Problem
Ollama returns "403 Forbidden" when the RMG Bridge Extension tries to proxy requests because Ollama has CORS restrictions by default.

## Solution
Configure Ollama to allow requests from the Chrome extension.

### Windows (PowerShell - Run as Administrator)

1. **Stop Ollama if running:**
   ```powershell
   Stop-Process -Name "ollama" -Force -ErrorAction SilentlyContinue
   ```

2. **Set environment variable permanently:**
   ```powershell
   [System.Environment]::SetEnvironmentVariable('OLLAMA_ORIGINS', '*', 'User')
   ```

3. **Restart Ollama:**
   - Open Ollama from Start Menu, or
   - Run: `ollama serve` in a new PowerShell window

4. **Verify it's working:**
   ```powershell
   curl http://localhost:11434/api/tags
   ```

### Alternative: Temporary Fix (This Session Only)

```powershell
$env:OLLAMA_ORIGINS = "*"
ollama serve
```

### What This Does
- `OLLAMA_ORIGINS=*` tells Ollama to accept requests from any origin
- This allows the Chrome extension to proxy requests successfully
- The extension can then communicate with your local Ollama instance

### Security Note
Setting `OLLAMA_ORIGINS=*` allows any website to access your local Ollama. If you prefer more security, you can set it to specific origins:

```powershell
[System.Environment]::SetEnvironmentVariable('OLLAMA_ORIGINS', 'chrome-extension://*,https://roninmedia.studio,https://*.onrender.com', 'User')
```

## After Configuration

1. Restart Ollama
2. Reload the RMG Bridge Extension in Chrome
3. Try scraping with Ollama in SCRP again
4. Check browser console for detailed logs from the updated extension

## Verification

You should see these logs in the console:
- `🔄 RMG Bridge: Proxying API request to /api/generate`
- `📦 RMG Bridge: Request body: {...}`
- `📡 RMG Bridge: Response status: 200 OK`
- `✅ RMG Bridge: Successfully parsed JSON response`

Instead of:
- `❌ RMG Bridge: Ollama API error: 403 Forbidden`

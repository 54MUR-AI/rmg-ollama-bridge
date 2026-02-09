# RMG Ollama Bridge - Quick Start Guide

## For Users: 5-Minute Setup

### Step 1: Install the Extension (1 minute)

1. Download `rmg-ollama-bridge.zip`
2. Extract to a permanent location (e.g., `Documents\Extensions\rmg-ollama-bridge`)
3. Open Chrome: `chrome://extensions/`
4. Enable "Developer mode" (top right)
5. Click "Load unpacked" → Select the extracted folder
6. Extension installed! ✅

### Step 2: Install ngrok (2 minutes)

**Windows:**
```powershell
# Option 1: Chocolatey (if installed)
choco install ngrok

# Option 2: Manual download
# Go to: https://ngrok.com/download
# Download Windows ZIP
# Extract ngrok.exe to C:\ngrok\
# Add C:\ngrok to PATH
```

**Sign up and authenticate:**
1. Go to https://ngrok.com/signup (free account)
2. Get your auth token from dashboard
3. Run: `ngrok config add-authtoken YOUR_TOKEN_HERE`

### Step 3: Start Ollama Tunnel (30 seconds)

```bash
# Start the tunnel
ngrok http 11434

# You'll see output like:
# Forwarding: https://abc123-def456.ngrok-free.app -> http://localhost:11434
```

**Copy the HTTPS URL** (e.g., `https://abc123-def456.ngrok-free.app`)

### Step 4: Configure SCRP Backend (1 minute)

1. Go to Render dashboard: https://dashboard.render.com
2. Find your SCRP service
3. Go to "Environment" tab
4. Add new environment variable:
   - **Key:** `OLLAMA_BASE_URL`
   - **Value:** `https://abc123-def456.ngrok-free.app` (your ngrok URL)
5. Click "Save Changes"
6. Render will auto-redeploy (takes ~2 minutes)

### Step 5: Test It! (30 seconds)

1. Open https://roninmedia.studio
2. Go to SCRP
3. Open Settings
4. Select "Ollama (Local)"
5. You should see your models: `qwen3-vl:8b`, `llama3:latest`, etc.
6. Select a model and try scraping a URL
7. It works! 🎉

---

## Keeping the Tunnel Running

**Problem:** ngrok tunnel closes when you close the terminal.

**Solutions:**

### Option 1: Keep Terminal Open
- Just leave the ngrok terminal window open
- Minimize it to system tray

### Option 2: Run as Background Service (Windows)

Create `start-ollama-tunnel.bat`:
```batch
@echo off
start /min ngrok http 11434
```

Double-click to start in background.

### Option 3: Windows Task Scheduler (Auto-start on boot)

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Ollama Tunnel"
4. Trigger: "When I log on"
5. Action: "Start a program"
6. Program: `C:\ngrok\ngrok.exe`
7. Arguments: `http 11434`
8. Finish

Now ngrok starts automatically when you log in!

---

## Troubleshooting

### Extension not detecting models
- Check extension is enabled in `chrome://extensions/`
- Refresh the RMG page
- Check console for `🗡️ RMG Ollama Bridge` messages

### Backend can't connect to Ollama
- Verify ngrok tunnel is running: `ngrok http 11434`
- Check `OLLAMA_BASE_URL` is set correctly on Render
- Make sure Ollama is running: `ollama list`
- Check ngrok URL hasn't changed (free tier URLs change on restart)

### ngrok URL keeps changing
- Free tier generates new URLs on each restart
- Upgrade to ngrok paid plan for static domains ($8/month)
- Or: Use Cloudflare Tunnel (free, static URLs)

---

## Next Steps

See `AUTOMATION.md` for automated tunnel management and user-friendly setup UI.

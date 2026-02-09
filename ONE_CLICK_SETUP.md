# One-Click Ollama Setup - Architecture

## User Experience Goal

User selects "Ollama (Local)" → Automatic detection → Guided setup → Everything works

## Detection Flow

```
User selects Ollama
    ↓
Frontend checks:
    1. Is Ollama running? (try fetch localhost:11434)
    2. Is extension installed? (postMessage test)
    3. Is tunnel active? (check backend connectivity)
    ↓
If all ✅ → Use Ollama
If any ❌ → Show Setup Wizard
```

## Setup Wizard States

### State 1: Ollama Not Detected
```
❌ Ollama not detected

Ollama is a local AI runtime that runs models on your computer.

[Download Ollama] [I already have it]

After installing, Ollama will run automatically.
```

### State 2: Extension Not Installed
```
✅ Ollama detected (6 models found)
❌ RMG Bridge Extension not installed

The extension allows RMG to detect your local models.

[Download Extension] [Installation Guide]

Quick install: Load unpacked in chrome://extensions/
```

### State 3: Tunnel Not Active
```
✅ Ollama detected
✅ Extension installed
❌ Remote access not configured

To use Ollama with deployed RMG, we need to set up secure remote access.

[Auto-Setup Tunnel] [Manual Setup]

This creates a secure connection to your local Ollama.
```

### State 4: All Ready
```
✅ Ollama detected (6 models)
✅ Extension installed
✅ Remote access active

Select a model to get started!
```

## Components Needed

### 1. Frontend Detection Service
```javascript
// src/services/ollamaDetection.js
export class OllamaDetectionService {
  async detectOllama() {
    try {
      const response = await fetch('http://localhost:11434/api/tags', {
        signal: AbortSignal.timeout(2000)
      });
      if (response.ok) {
        const data = await response.json();
        return { running: true, models: data.models };
      }
    } catch {
      return { running: false };
    }
  }

  async detectExtension() {
    return new Promise((resolve) => {
      const timeout = setTimeout(() => resolve(false), 1000);
      
      const handler = (event) => {
        if (event.data.type === 'RMG_OLLAMA_MODELS' && 
            event.data.source === 'rmg-ollama-bridge') {
          clearTimeout(timeout);
          window.removeEventListener('message', handler);
          resolve(true);
        }
      };
      
      window.addEventListener('message', handler);
      window.postMessage({ type: 'RMG_REQUEST_OLLAMA_MODELS' }, '*');
    });
  }

  async detectTunnel() {
    try {
      const response = await fetch('/api/ollama/status');
      const data = await response.json();
      return data.tunnelActive;
    } catch {
      return false;
    }
  }

  async getSetupStatus() {
    const [ollama, extension, tunnel] = await Promise.all([
      this.detectOllama(),
      this.detectExtension(),
      this.detectTunnel()
    ]);

    return {
      ollama,
      extension,
      tunnel,
      ready: ollama.running && extension && tunnel
    };
  }
}
```

### 2. Setup Wizard Component
```jsx
// SetupWizard.jsx
import { useState, useEffect } from 'react';
import { OllamaDetectionService } from '../services/ollamaDetection';

export default function OllamaSetupWizard({ onComplete }) {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkStatus();
  }, []);

  const checkStatus = async () => {
    const detector = new OllamaDetectionService();
    const result = await detector.getSetupStatus();
    setStatus(result);
    setLoading(false);
    
    if (result.ready) {
      onComplete(result.ollama.models);
    }
  };

  const downloadExtension = () => {
    window.open('/downloads/rmg-ollama-bridge.zip', '_blank');
  };

  const downloadOllama = () => {
    window.open('https://ollama.ai/download', '_blank');
  };

  const setupTunnel = async () => {
    // Trigger tunnel setup
    const response = await fetch('/api/ollama/setup-tunnel', {
      method: 'POST'
    });
    const data = await response.json();
    
    if (data.success) {
      checkStatus(); // Re-check
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="setup-wizard">
      <h2>🗡️ Ollama Setup</h2>

      {/* Step 1: Ollama */}
      <SetupStep
        title="Ollama Runtime"
        status={status.ollama.running ? 'complete' : 'pending'}
        icon="🤖"
      >
        {!status.ollama.running ? (
          <>
            <p>Ollama is not running on your computer.</p>
            <button onClick={downloadOllama}>Download Ollama</button>
            <button onClick={checkStatus}>I installed it</button>
          </>
        ) : (
          <p>✅ Detected {status.ollama.models.length} models</p>
        )}
      </SetupStep>

      {/* Step 2: Extension */}
      <SetupStep
        title="RMG Bridge Extension"
        status={status.extension ? 'complete' : 'pending'}
        icon="🔌"
        disabled={!status.ollama.running}
      >
        {!status.extension ? (
          <>
            <p>Browser extension required for model detection.</p>
            <button onClick={downloadExtension}>Download Extension</button>
            <a href="/docs/extension-install">Installation Guide</a>
            <button onClick={checkStatus}>I installed it</button>
          </>
        ) : (
          <p>✅ Extension active</p>
        )}
      </SetupStep>

      {/* Step 3: Tunnel */}
      <SetupStep
        title="Remote Access"
        status={status.tunnel ? 'complete' : 'pending'}
        icon="🌐"
        disabled={!status.extension}
      >
        {!status.tunnel ? (
          <>
            <p>Enable remote access for deployed RMG apps.</p>
            <button onClick={setupTunnel}>Auto-Setup</button>
            <a href="/docs/manual-tunnel">Manual Setup</a>
          </>
        ) : (
          <p>✅ Tunnel active</p>
        )}
      </SetupStep>

      {status.ready && (
        <button onClick={() => onComplete(status.ollama.models)}>
          Start Using Ollama
        </button>
      )}
    </div>
  );
}
```

### 3. Native Messaging Host (for tunnel automation)
```python
# native-host/rmg_tunnel_manager.py
import sys
import json
import struct
import subprocess
import os

class TunnelManager:
    def __init__(self):
        self.tunnel_process = None
        self.tunnel_url = None

    def start_tunnel(self):
        """Start Cloudflare tunnel"""
        try:
            # Use cloudflared for free, static tunnels
            self.tunnel_process = subprocess.Popen(
                ['cloudflared', 'tunnel', '--url', 'http://localhost:11434'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Parse tunnel URL from output
            for line in self.tunnel_process.stderr:
                if 'trycloudflare.com' in line:
                    self.tunnel_url = line.split('https://')[1].split()[0]
                    self.tunnel_url = f'https://{self.tunnel_url}'
                    break
            
            return {
                'success': True,
                'url': self.tunnel_url
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def stop_tunnel(self):
        """Stop tunnel"""
        if self.tunnel_process:
            self.tunnel_process.terminate()
            self.tunnel_process = None
            self.tunnel_url = None
        return {'success': True}

    def get_status(self):
        """Get tunnel status"""
        return {
            'active': self.tunnel_process is not None,
            'url': self.tunnel_url
        }

def send_message(message):
    """Send message to extension"""
    encoded = json.dumps(message).encode('utf-8')
    sys.stdout.buffer.write(struct.pack('I', len(encoded)))
    sys.stdout.buffer.write(encoded)
    sys.stdout.buffer.flush()

def read_message():
    """Read message from extension"""
    text_length_bytes = sys.stdin.buffer.read(4)
    if len(text_length_bytes) == 0:
        sys.exit(0)
    
    text_length = struct.unpack('I', text_length_bytes)[0]
    text = sys.stdin.buffer.read(text_length).decode('utf-8')
    return json.loads(text)

def main():
    manager = TunnelManager()
    
    while True:
        message = read_message()
        action = message.get('action')
        
        if action == 'start':
            response = manager.start_tunnel()
        elif action == 'stop':
            response = manager.stop_tunnel()
        elif action == 'status':
            response = manager.get_status()
        else:
            response = {'error': 'Unknown action'}
        
        send_message(response)

if __name__ == '__main__':
    main()
```

### 4. Backend API Endpoints
```python
# backend/routes/ollama_setup.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import os

router = APIRouter(prefix="/api/ollama", tags=["Ollama Setup"])

class TunnelSetupRequest(BaseModel):
    tunnel_url: str

@router.get("/status")
async def get_ollama_status(user_id: str = Depends(get_current_user)):
    """Check if user has Ollama tunnel configured"""
    user_settings = await db.get_user_settings(user_id)
    return {
        "tunnelActive": user_settings.get("ollama_url") is not None,
        "tunnelUrl": user_settings.get("ollama_url")
    }

@router.post("/setup-tunnel")
async def setup_tunnel(
    request: TunnelSetupRequest,
    user_id: str = Depends(get_current_user)
):
    """Save user's Ollama tunnel URL"""
    await db.update_user_settings(user_id, {
        "ollama_url": request.tunnel_url,
        "ollama_enabled": True
    })
    return {"success": True}

@router.get("/download-extension")
async def download_extension():
    """Serve extension ZIP file"""
    return FileResponse(
        "static/downloads/rmg-ollama-bridge.zip",
        media_type="application/zip",
        filename="rmg-ollama-bridge.zip"
    )
```

### 5. Installer Package
```
rmg-ollama-setup.exe (Windows installer)
├── rmg-ollama-bridge/ (extension files)
├── cloudflared.exe (tunnel binary)
├── native-host/ (tunnel manager)
├── install.ps1 (setup script)
└── README.txt
```

Install script:
```powershell
# install.ps1
Write-Host "🗡️ RMG Ollama Setup" -ForegroundColor Red

# Check if Ollama is installed
if (!(Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Ollama..."
    winget install Ollama.Ollama
}

# Install cloudflared
Write-Host "Installing Cloudflare Tunnel..."
winget install Cloudflare.cloudflared

# Install native messaging host
Write-Host "Installing tunnel manager..."
$nativeHostPath = "$env:LOCALAPPDATA\RMG\native-host"
New-Item -ItemType Directory -Force -Path $nativeHostPath
Copy-Item -Path "native-host\*" -Destination $nativeHostPath -Recurse

# Register native messaging host
$manifestPath = "$nativeHostPath\manifest.json"
$registryPath = "HKCU:\Software\Google\Chrome\NativeMessagingHosts\com.rmg.tunnel_manager"
New-Item -Path $registryPath -Force
Set-ItemProperty -Path $registryPath -Name "(Default)" -Value $manifestPath

Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host "Next: Install the browser extension from chrome://extensions/"
```

## Hosting Setup

### Supabase Storage
```sql
-- Create storage bucket
INSERT INTO storage.buckets (id, name, public)
VALUES ('rmg-downloads', 'rmg-downloads', true);

-- Upload files
-- rmg-ollama-bridge.zip
-- rmg-ollama-setup.exe
-- cloudflared.exe
```

### RMG Frontend
```
/public/downloads/
├── rmg-ollama-bridge.zip
├── rmg-ollama-setup-windows.exe
├── rmg-ollama-setup-mac.dmg
└── install-guide.pdf
```

## Complete Flow

1. User selects "Ollama (Local)"
2. Frontend detects: ❌ Ollama, ❌ Extension, ❌ Tunnel
3. Shows Setup Wizard
4. User clicks "Download All-in-One Installer"
5. Downloads `rmg-ollama-setup.exe`
6. Runs installer → Installs Ollama, cloudflared, native host
7. User loads extension in Chrome
8. Extension auto-starts tunnel via native host
9. Extension sends tunnel URL to backend
10. Backend saves user's Ollama URL
11. User refreshes RMG → All ✅
12. Select model → Start using Ollama

**Total user actions: 3 clicks + 1 Chrome extension load**

## Implementation Priority

**Week 1:**
- Detection service
- Setup wizard UI
- Backend API endpoints
- Host extension on Supabase

**Week 2:**
- Native messaging host
- Tunnel auto-management
- Installer package

**Week 3:**
- Polish UI/UX
- Error handling
- Documentation
- Testing

**Result:** True one-click setup for new users

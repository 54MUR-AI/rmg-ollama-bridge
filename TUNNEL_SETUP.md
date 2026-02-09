# Ollama Tunnel Setup for Remote Access

To use your local Ollama with deployed SCRP, you need to expose Ollama to the internet via a secure tunnel.

## Option 1: Cloudflare Tunnel (Recommended - Free & Secure)

### Install Cloudflare Tunnel
```bash
# Windows (PowerShell as Admin)
winget install --id Cloudflare.cloudflared

# Or download from: https://github.com/cloudflare/cloudflared/releases
```

### Setup Tunnel
```bash
# Login to Cloudflare
cloudflared tunnel login

# Create a tunnel
cloudflared tunnel create ollama-tunnel

# Start the tunnel (expose Ollama)
cloudflared tunnel --url http://localhost:11434
```

This will give you a URL like: `https://random-words-123.trycloudflare.com`

### Keep Tunnel Running
```bash
# Run in background
cloudflared tunnel --url http://localhost:11434 &
```

## Option 2: ngrok (Easier, Free Tier Available)

### Install ngrok
```bash
# Download from: https://ngrok.com/download
# Or use chocolatey:
choco install ngrok

# Sign up at ngrok.com and get auth token
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

### Start Tunnel
```bash
ngrok http 11434
```

This will give you a URL like: `https://abc123.ngrok.io`

## Option 3: localtunnel (Simplest, No Account Needed)

### Install
```bash
npm install -g localtunnel
```

### Start Tunnel
```bash
lt --port 11434 --subdomain ollama-yourname
```

URL: `https://ollama-yourname.loca.lt`

## Using the Tunnel URL

Once you have a tunnel URL, you need to:

1. **Update SCRP Backend** to use the tunnel URL instead of localhost
2. **Configure CORS** on Ollama to accept requests from the tunnel
3. **Keep the tunnel running** while using SCRP

## Security Considerations

⚠️ **Important:** Exposing Ollama to the internet has security implications:
- Anyone with the URL can access your Ollama instance
- Use authentication if possible
- Only run the tunnel when needed
- Monitor usage

## Better Solution: Backend Proxy

Instead of exposing Ollama directly, we can:
1. Extension detects models (already working)
2. User configures tunnel URL in SCRP settings
3. SCRP backend uses the tunnel URL to connect to Ollama
4. Requests are authenticated via LDGR

This is what we'll implement next.

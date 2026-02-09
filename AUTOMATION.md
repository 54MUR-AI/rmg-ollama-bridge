# Automated Ollama Tunnel Management

## Vision: One-Click Setup for Users

Instead of manual ngrok setup, we want:
1. User installs extension
2. Extension detects Ollama
3. User clicks "Enable Remote Access" button
4. Extension automatically sets up tunnel
5. Extension automatically updates SCRP backend
6. Everything just works ✨

## Implementation Plan

### Phase 1: Extension-Managed Tunnel

**Challenge:** Browser extensions can't run system commands (ngrok).

**Solution:** Native Messaging Host

```
Browser Extension <--> Native App <--> ngrok/cloudflare
```

**Architecture:**
1. Create lightweight native app (Python/Node.js)
2. Extension communicates via Native Messaging API
3. Native app manages tunnel lifecycle
4. Extension displays tunnel status in UI

**Files needed:**
- `native-host/ollama-tunnel-manager.py` - Python script to manage tunnel
- `native-host/manifest.json` - Native messaging manifest
- Extension updated to use `chrome.runtime.connectNative()`

### Phase 2: Cloudflare Tunnel (Better than ngrok)

**Why Cloudflare:**
- ✅ Free forever
- ✅ Static URLs (don't change)
- ✅ Better performance
- ✅ No account signup required
- ✅ Built-in DDoS protection

**Setup:**
```bash
# Install cloudflared
winget install Cloudflare.cloudflared

# Start tunnel (no auth needed for quick tunnels)
cloudflared tunnel --url http://localhost:11434
```

**Advantages:**
- URL format: `https://random-words.trycloudflare.com`
- Same URL every time if you create a named tunnel
- No rate limits
- No account required for basic use

### Phase 3: Auto-Configuration

**Extension capabilities:**
1. Detect if Ollama is running
2. Detect if tunnel is active
3. Start/stop tunnel via native host
4. Display tunnel URL to user
5. Copy URL to clipboard
6. Show connection status

**UI in Settings Panel:**
```jsx
{provider === 'ollama' && (
  <div className="tunnel-manager">
    <h3>🌐 Remote Access</h3>
    
    {!tunnelActive ? (
      <button onClick={startTunnel}>
        Enable Remote Access
      </button>
    ) : (
      <div className="tunnel-info">
        <p>✅ Tunnel Active</p>
        <code>{tunnelUrl}</code>
        <button onClick={copyUrl}>Copy URL</button>
        <button onClick={stopTunnel}>Stop Tunnel</button>
      </div>
    )}
    
    <p className="help-text">
      This allows deployed SCRP to access your local Ollama
    </p>
  </div>
)}
```

### Phase 4: Backend Auto-Update (Advanced)

**Challenge:** User still needs to manually update Render env var.

**Solution:** Backend API endpoint

```python
# New endpoint in SCRP backend
@app.post("/api/config/ollama-url")
async def update_ollama_url(url: str, auth_token: str):
    # Verify user is authenticated
    # Update Render env var via Render API
    # Or: Store in database per-user
    # Restart service if needed
```

**Better approach:** Per-user Ollama URLs

Instead of global `OLLAMA_BASE_URL`, store per-user:
```python
# In database
user_settings = {
    "user_id": "123",
    "ollama_url": "https://abc.trycloudflare.com",
    "ollama_enabled": True
}

# Backend checks user's Ollama URL
if user.ollama_enabled:
    ollama_client = OllamaClient(base_url=user.ollama_url)
```

This allows:
- Multiple users with different Ollama instances
- No need to update Render env vars
- User-specific configuration
- Works for both local and deployed

### Phase 5: Complete Automation

**Final user experience:**

1. **Install extension** (one-time, 30 seconds)
2. **Click "Enable Remote Access"** in settings
3. Extension:
   - Detects Ollama
   - Starts Cloudflare tunnel
   - Gets tunnel URL
   - Sends URL to SCRP backend API
   - Backend saves user's Ollama URL
4. **Done!** User can now use local Ollama from deployed SCRP

**Maintenance:**
- Tunnel runs in background
- Auto-starts on system boot
- Extension shows status indicator
- User can stop/restart from settings

---

## Implementation Roadmap

### Immediate (This Week)
- [x] Extension detects models ✅
- [x] Manual ngrok setup guide ✅
- [ ] Test ngrok with deployed SCRP
- [ ] Document working setup

### Short-term (Next Week)
- [ ] Create native messaging host
- [ ] Extension UI for tunnel management
- [ ] Switch to Cloudflare Tunnel
- [ ] Auto-start tunnel on boot

### Medium-term (Next Month)
- [ ] Backend API for per-user Ollama URLs
- [ ] Database schema for user settings
- [ ] Extension auto-configures backend
- [ ] One-click setup complete

### Long-term (Future)
- [ ] Publish extension to Chrome Web Store
- [ ] Support for multiple Ollama instances
- [ ] Tunnel health monitoring
- [ ] Usage analytics
- [ ] Mobile app support (via tunnel)

---

## Alternative: Hybrid Approach

**For power users:**
- Manual tunnel setup (current guide)
- Full control over tunnel
- Can use any tunnel service

**For regular users:**
- One-click extension setup
- Managed tunnel
- Just works™

Both approaches supported, user chooses their preference.

---

## Security Considerations

### Tunnel Security
- Tunnels expose Ollama to internet
- Anyone with URL can access
- Mitigations:
  - Use Cloudflare Access (free auth layer)
  - Rate limiting on backend
  - User-specific API tokens
  - Monitor usage

### Extension Permissions
- Native messaging requires additional permission
- User must approve native host installation
- Clear documentation on what it does

### Backend Security
- Validate tunnel URLs
- Sanitize user input
- Rate limit API calls
- Log all Ollama requests

---

## Cost Analysis

### Free Tier (Recommended)
- Cloudflare Tunnel: Free forever
- Extension hosting: Free (GitHub)
- Backend: Existing Render plan
- **Total: $0/month**

### Paid Tier (Optional)
- ngrok Pro: $8/month (static domains)
- Cloudflare Teams: $7/user/month (advanced features)
- **Total: $7-8/month** (only if needed)

**Recommendation:** Start with free Cloudflare Tunnel, upgrade only if needed.

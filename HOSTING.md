# Hosting the RMG Ollama Bridge Extension

## Option 1: GitHub Releases (Recommended)

### Setup
1. Create a new GitHub repository: `rmg-ollama-bridge`
2. Push the extension code
3. Create a release with the ZIP file

### Commands
```bash
cd C:\Users\54MUR41\CascadeProjects\rmg-ollama-bridge
git remote add origin https://github.com/54MUR-AI/rmg-ollama-bridge.git
git branch -M main
git push -u origin main

# Create release
# Go to GitHub → Releases → Create new release
# Tag: v1.0.0
# Title: RMG Ollama Bridge v1.0.0
# Upload: rmg-ollama-bridge.zip
```

### Download Link
Users can download from:
```
https://github.com/54MUR-AI/rmg-ollama-bridge/releases/latest/download/rmg-ollama-bridge.zip
```

## Option 2: Supabase Storage

### Upload to Supabase
```javascript
// In RMG admin panel
const { data, error } = await supabase.storage
  .from('extensions')
  .upload('rmg-ollama-bridge.zip', zipFile, {
    contentType: 'application/zip',
    upsert: true
  })

// Get public URL
const { data: { publicUrl } } = supabase.storage
  .from('extensions')
  .getPublicUrl('rmg-ollama-bridge.zip')
```

### Download Link
```
https://meqfiyuaxgwbstcdmjgz.supabase.co/storage/v1/object/public/extensions/rmg-ollama-bridge.zip
```

## Option 3: Direct from RMG Site

Host the ZIP file in RMG's public folder:
```
/public/downloads/rmg-ollama-bridge.zip
```

Download link:
```
https://roninmedia.studio/downloads/rmg-ollama-bridge.zip
```

## Adding Download Button to RMG

### In Settings Panel (SCRP/OMNI)
```jsx
{provider === 'ollama' && (
  <div className="mt-4 p-4 bg-samurai-black-lighter rounded-xl border border-samurai-red/30">
    <h3 className="text-white font-bold mb-2">🗡️ RMG Ollama Bridge</h3>
    <p className="text-white/70 text-sm mb-3">
      Install our browser extension to automatically detect your locally installed Ollama models.
    </p>
    <a
      href="https://github.com/54MUR-AI/rmg-ollama-bridge/releases/latest/download/rmg-ollama-bridge.zip"
      download
      className="inline-block px-4 py-2 bg-samurai-red text-white rounded-lg hover:bg-samurai-red-dark transition-colors"
    >
      📥 Download Extension
    </a>
    <a
      href="https://github.com/54MUR-AI/rmg-ollama-bridge/blob/main/INSTALL.md"
      target="_blank"
      rel="noopener noreferrer"
      className="ml-2 inline-block px-4 py-2 border border-samurai-red text-samurai-red rounded-lg hover:bg-samurai-red/10 transition-colors"
    >
      📖 Installation Guide
    </a>
  </div>
)}
```

## Updating the Extension

When you make changes:
1. Update version in `manifest.json`
2. Commit changes
3. Create new ZIP: `Compress-Archive -Path * -DestinationPath ..\rmg-ollama-bridge-v1.0.1.zip`
4. Create new GitHub release with updated ZIP
5. Users can download and overwrite their existing installation

## Version History

- **v1.0.0** (2026-02-09)
  - Initial release
  - Dynamic Ollama model detection
  - Support for SCRP, OMNI, LDGR
  - Chrome/Edge/Firefox compatible

---

**Recommended:** Use GitHub Releases for automatic version management and easy distribution.

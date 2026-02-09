# RMG Ollama Bridge - Installation Guide

## Quick Install (Chrome/Edge)

### Step 1: Download Extension
1. Download the extension ZIP file
2. Extract to a permanent location (e.g., `Documents\Extensions\rmg-ollama-bridge`)
3. **Important:** Don't delete this folder - Chrome needs it to stay installed

### Step 2: Install in Chrome
1. Open Chrome and go to: `chrome://extensions/`
2. Enable **Developer mode** (toggle in top right corner)
3. Click **"Load unpacked"**
4. Select the extracted `rmg-ollama-bridge` folder
5. Extension will appear in your toolbar

### Step 3: Verify Installation
1. Look for "RMG Ollama Bridge" in your extensions list
2. Status should show "Enabled"
3. Click the extension icon to see details

### Step 4: Test It
1. Make sure Ollama is running: `ollama list`
2. Open RMG site: https://roninmedia.studio
3. Navigate to SCRP or OMNI
4. Open Settings → Select "Ollama (Local)"
5. You should see your actual installed models (not the default list)

## Troubleshooting

### Extension Not Loading
**Error:** "Could not load icon 'icon16.png'"
- Make sure all icon files are in the folder
- Try clicking "Retry" in the error dialog

**Error:** "Could not load manifest"
- Check that `manifest.json` is in the root of the folder
- Verify the folder structure is correct

### Models Not Showing
1. **Check Ollama is running:**
   ```bash
   ollama list
   ```

2. **Check extension console:**
   - Go to `chrome://extensions/`
   - Find "RMG Ollama Bridge"
   - Click "service worker" link
   - Should see: `✅ RMG Bridge: Fetched X models`

3. **Check page console:**
   - Open RMG site
   - Press F12 → Console tab
   - Should see: `🗡️ RMG Ollama Bridge content script loaded`
   - Should see: `✅ RMG Bridge: Injected X models into page`

### Extension Permissions
If Chrome asks for permissions:
- ✅ **Access to localhost:11434** - Needed to fetch Ollama models
- ✅ **Access to RMG sites** - Needed to inject model data
- ✅ **Storage** - Needed to cache model list

## Updating the Extension

When a new version is released:
1. Download the new ZIP file
2. Extract to the SAME folder (overwrite old files)
3. Go to `chrome://extensions/`
4. Click the refresh icon on the "RMG Ollama Bridge" card
5. Extension will reload with new code

## Uninstalling

1. Go to `chrome://extensions/`
2. Find "RMG Ollama Bridge"
3. Click "Remove"
4. Delete the extension folder from your computer

## Firefox Installation

### Step 1: Temporary Installation
1. Open Firefox and go to: `about:debugging#/runtime/this-firefox`
2. Click **"Load Temporary Add-on"**
3. Navigate to the extension folder
4. Select `manifest.json`
5. Extension will be loaded (until browser restart)

### Step 2: Permanent Installation (Advanced)
Firefox requires extensions to be signed for permanent installation. For development:
1. Go to `about:config`
2. Set `xpinstall.signatures.required` to `false`
3. Follow temporary installation steps above

**Note:** Extension will be removed when Firefox restarts unless signed.

## Support

For issues or questions:
- Check the console logs (F12)
- Verify Ollama is running
- Make sure you're on a supported RMG site
- Contact RMG development team

---

**Made with 🗡️ by Ronin Media Group**

# OmniSync Pro - Phone Monitoring Desktop App

A real-time desktop application that monitors your Android phone's calls, SMS messages, and notifications through Firebase.

## Features
- 📊 **Live Activity Feed** - Real-time phone events
- 📞 **Call History** - Track all incoming/outgoing calls
- 💬 **Messages & Alerts** - Monitor SMS and notifications
- 🔄 **Instant Sync** - Firebase-powered real-time updates
- 🌙 **Dark Mode UI** - Easy on the eyes
- 🎯 **Custom Icon** - Professional app appearance
- 📦 **Standalone Executable** - Package as Windows app

## Quick Install (Windows)

**Option 1: One-Line Install (Easiest)**
```powershell
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/Nyakego254/OmniSync/main/install.ps1' -OutFile 'install.ps1'; .\install.ps1"
```

**Option 2: Manual Install**
```powershell
git clone https://github.com/Nyakego254/OmniSync.git
cd OmniSync
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

## Setup Requirements
1. Python 3.8+ installed
2. Firebase service account key (place as `firebase-key.json` in project folder)
3. Android companion app granting phone permissions

## Configuration
Edit `app.py` and update your Firebase URL:
```python
db_url="https://your-firebase-url.firebaseio.com/"
```

## Package as Standalone Windows App

**Step 1: Install build dependencies** (one-time only)
```powershell
pip install --only-binary :all: Pillow pyinstaller
```

**Step 2: Build the executable**
```powershell
.\build.ps1
```

This creates the standalone app at: `.\dist\OmniSync.exe`

**Step 3: Create desktop shortcut** (optional)
```powershell
.\create_shortcut.ps1
```

Now you have a complete Windows application that can be shared and installed on any machine!

## Project Structure
- `app.py` - Main desktop GUI (with icon support)
- `firebase_listener.py` - Firebase real-time listener
- `firebase-key.json` - Firebase credentials (keep safe, don't commit)
- `assets/` - Application icon files
- `build.ps1` - Script to build Windows executable
- `create_icon.py` - Script to generate app icon

## Running the App

**From source:**
```powershell
python app.py
```

**From executable (after building):**
```powershell
.\dist\OmniSync.exe
```

**From desktop shortcut (after creating):**
- Double-click the "OmniSync" icon on your desktop

## License
Open Source

## Support
For issues, visit: https://github.com/Nyakego254/OmniSync


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

## Quick Start (Windows)

**Installation:**
1. Extract all files from this ZIP to a folder (e.g., `C:\OmniSync`)
2. Double-click `OmniSync.exe` to run the app
3. The app is pre-configured with Firebase settings

**That's it!** The app will automatically connect to Firebase and start monitoring your phone data.

## Setup Requirements
- Windows 10/11
- Firebase service account key (included in this package as `firebase-key.json`)
- Android companion app granting phone permissions

## Configuration
The app is pre-configured with Firebase settings. If you need to change the Firebase project:
1. Replace `firebase-key.json` with your own Firebase service account key
2. Edit `OmniSync.exe` (requires rebuilding from source)

## Troubleshooting
- **App won't start**: Make sure all files from the ZIP are extracted to the same folder
- **No data showing**: Check that your Android app is sending data to Firebase
- **Connection issues**: Verify internet connection and Firebase project settings

## Support
For issues or questions, check the GitHub repository: https://github.com/Nyakego254/OmniSync
.\build.ps1
```

This creates the standalone app at: `.\dist\OmniSync.exe`

**Step 3: Create desktop shortcut** (optional)
```powershell
.\create_shortcut.ps1
```

**Step 4: Create installer package**
```powershell
.\make_installer.ps1
```

The installer package is created as a ZIP file next to your repository root, e.g. `OmniSync-Installer-v1.0.0.zip`.

## Release Workflow

There are two ways to publish a release:

1. Use the included release script locally:
```powershell
.\release.ps1
```
This will push the `main` branch and the `v1.0.0` tag to GitHub. If `gh` is installed, it will also create a GitHub release and attach `dist\OmniSync.exe`.

2. Use GitHub Actions automatically:
- Push a tag like `v1.0.0` to GitHub
- The workflow in `.github/workflows/release.yml` will build the executable and publish the release asset automatically

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


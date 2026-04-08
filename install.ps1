# OmniSync Auto-Installer Script
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "OmniSync Pro - Auto Installer" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Set download location
$installPath = "$env:USERPROFILE\Desktop\OmniSync"

Write-Host "Installing to: $installPath" -ForegroundColor Yellow

# Check if already exists
if (Test-Path $installPath) {
    Write-Host "OmniSync already exists. Removing old version..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $installPath
}

# Clone repository
Write-Host "Downloading OmniSync..." -ForegroundColor Cyan
git clone https://github.com/Nyakego254/OmniSync.git $installPath

if (-not $?) {
    Write-Host "Git clone failed. Make sure Git is installed." -ForegroundColor Red
    exit 1
}

cd $installPath

# Create virtual environment
Write-Host "Setting up Python environment..." -ForegroundColor Cyan
python -m venv .venv

if (-not $?) {
    Write-Host "Python virtual environment setup failed. Make sure Python 3.8+ is installed." -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt --quiet

if (-not $?) {
    Write-Host "Dependency installation failed." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Green
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANT:" -ForegroundColor Yellow
Write-Host "1. Add your Firebase key file as firebase-key.json to:" -ForegroundColor White
Write-Host "   $installPath" -ForegroundColor White
Write-Host ""
Write-Host "2. Update Firebase URL in app.py if needed" -ForegroundColor White
Write-Host ""
Write-Host "To run OmniSync:" -ForegroundColor Cyan
Write-Host "cd $installPath" -ForegroundColor Green
Write-Host ".\.venv\Scripts\Activate.ps1" -ForegroundColor Green
Write-Host "python app.py" -ForegroundColor Green
Write-Host ""

$buildDir = "build"
$distDir = "dist"
$appName = "OmniSync"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "OmniSync - PyInstaller Build" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Clean previous builds
Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path $buildDir) { Remove-Item -Recurse -Force $buildDir }
if (Test-Path $distDir) { Remove-Item -Recurse -Force $distDir }
if (Test-Path "$appName.spec") { Remove-Item "$appName.spec" }

Write-Host "Building executable..." -ForegroundColor Cyan
Write-Host ""

# Build with PyInstaller
pyinstaller `
    --onefile `
    --windowed `
    --icon=assets/omnisync.ico `
    --name=$appName `
    --add-data="assets:assets" `
    --hidden-import=firebase_admin `
    app.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "Build Complete!" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Executable location:" -ForegroundColor Yellow
    Write-Host ".\dist\OmniSync.exe" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Copy your firebase-key.json to the dist folder" -ForegroundColor White
    Write-Host "2. Run: .\dist\OmniSync.exe" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "Build failed!" -ForegroundColor Red
    exit 1
}

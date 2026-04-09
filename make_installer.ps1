$repoPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoPath

$version = (Get-Content VERSION -Raw).Trim()
if (-not $version) {
    Write-Error "VERSION file is empty. Add a version like 1.0.0"
    exit 1
}

Write-Host "Building OmniSync installer for v$version..." -ForegroundColor Cyan

# Build the executable first
& .\build.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Error "Build failed. Fix build errors before creating installer."
    exit 1
}

# Ensure dist exists
if (-not (Test-Path "dist\OmniSync.exe")) {
    Write-Error "Executable not found in dist/. Run build.ps1 first."
    exit 1
}

$installerDir = Join-Path $repoPath "installer"
if (Test-Path $installerDir) {
    Remove-Item -Recurse -Force $installerDir
}
New-Item -ItemType Directory -Path $installerDir | Out-Null

Copy-Item -Path "dist\OmniSync.exe" -Destination $installerDir
Copy-Item -Path "README.md" -Destination $installerDir
Copy-Item -Path "assets\omnisync.ico" -Destination $installerDir

$zipName = "OmniSync-Installer-v$version.zip"
if (Test-Path $zipName) { Remove-Item $zipName }

Write-Host "Creating installer archive: $zipName" -ForegroundColor Cyan
Compress-Archive -Path "$installerDir\*" -DestinationPath $zipName -Force

Write-Host "Installer package created: $zipName" -ForegroundColor Green
Write-Host "Include firebase-key.json in the same folder before running the executable." -ForegroundColor Yellow

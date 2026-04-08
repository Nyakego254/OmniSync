$desktop = [Environment]::GetFolderPath("Desktop")
$appPath = (Get-Location).Path + "\dist\OmniSync.exe"
$shortcutPath = "$desktop\OmniSync.lnk"

if (-not (Test-Path $appPath)) {
    Write-Host "Error: OmniSync.exe not found at $appPath" -ForegroundColor Red
    Write-Host "Please run build.ps1 first" -ForegroundColor Yellow
    exit 1
}

$WshShell = New-Object -ComObject WScript.Shell
$shortcut = $WshShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $appPath
$shortcut.WorkingDirectory = (Split-Path -Parent $appPath)
$shortcut.IconLocation = (Get-Location).Path + "\assets\omnisync.ico"
$shortcut.Description = "OmniSync Pro - Phone Monitoring Desktop App"
$shortcut.Save()

Write-Host "Desktop shortcut created: $shortcutPath" -ForegroundColor Green

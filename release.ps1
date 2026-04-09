$repoPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoPath

$version = (Get-Content VERSION -Raw).Trim()
if (-not $version) {
    Write-Error "VERSION file is empty. Add a version like 1.0.0"
    exit 1
}

Write-Host "Releasing OmniSync v$version..." -ForegroundColor Cyan

# Make sure working tree is clean
$changes = git status --porcelain
if ($changes) {
    Write-Host "Uncommitted changes detected. Commit or stash before releasing." -ForegroundColor Yellow
    git status --short
    exit 1
}

# Create release tag and push
git tag -a "v$version" -m "Release v$version"
git push origin main
if ($LASTEXITCODE -ne 0) { Write-Error "Failed to push branch."; exit 1 }
git push origin "v$version"
if ($LASTEXITCODE -ne 0) { Write-Error "Failed to push tag."; exit 1 }

# Create GitHub release if gh is available
if (Get-Command gh -ErrorAction SilentlyContinue) {
    if (Test-Path "dist\OmniSync.exe") {
        gh release create "v$version" "dist\OmniSync.exe" -t "OmniSync v$version" -n "Windows release build"
    } else {
        gh release create "v$version" -t "OmniSync v$version" -n "Windows release build"
        Write-Host "No executable found in dist/. Release created without assets." -ForegroundColor Yellow
    }
} else {
    Write-Host "GitHub CLI not installed. Tag pushed only." -ForegroundColor Yellow
}

Write-Host "Release complete: v$version" -ForegroundColor Green

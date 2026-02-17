# 🚀 Antigravity Multi-Model Setup

Write-Host "Setting up Antigravity Native Engine..." -ForegroundColor Cyan

# 1. Create Folder Structure
$folders = "prompts", ".logs", "tools", ".agent/workflows", "Docs"
foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder | Out-Null
        Write-Host "Created: $folder"
    }
}

# 2. Verify Python
if (Get-Command "python" -ErrorAction SilentlyContinue) {
    Write-Host "Python detected: OK" -ForegroundColor Green
} else {
    Write-Host "Warning: Python not found. Native Watcher requires Python." -ForegroundColor Yellow
}

# 3. Success Message
Write-Host "`nSetup Complete!" -ForegroundColor Green
Write-Host "1. Open this folder in Antigravity."
Write-Host "2. Type '/run-all' or 'ㄱ' in the chat."
Write-Host "3. Start editing files in 'prompts/' folder."

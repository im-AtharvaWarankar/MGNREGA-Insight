# CivicView GitHub Preparation Script
# This script prepares the project for GitHub by removing sensitive files

Write-Host "🧹 Preparing CivicView for GitHub..." -ForegroundColor Green

# 1. Remove sensitive files
Write-Host "`n📝 Removing sensitive files..." -ForegroundColor Cyan

$filesToRemove = @(
    ".env",
    "src/vault.py",
    "*.key",
    "*.pem",
    ".env.local"
)

foreach ($pattern in $filesToRemove) {
    Get-ChildItem -Path . -Filter $pattern -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "  ❌ Removing: $($_.FullName)" -ForegroundColor Red
        Remove-Item $_.FullName -Force
    }
}

# 2. Clean up logs and database files
Write-Host "`n🗑️  Cleaning logs and databases..." -ForegroundColor Cyan

$patternsToClean = @(
    "*.log",
    "*.sqlite3",
    "db.sqlite3-journal",
    "celerybeat-schedule"
)

foreach ($pattern in $patternsToClean) {
    Get-ChildItem -Path . -Filter $pattern -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "  🗑️  Removing: $($_.Name)" -ForegroundColor Yellow
        Remove-Item $_.FullName -Force
    }
}

# 3. Clean Python cache
Write-Host "`n🐍 Cleaning Python cache..." -ForegroundColor Cyan
Get-ChildItem -Path . -Filter "__pycache__" -Recurse -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host "  🗑️  Removing: $($_.FullName)" -ForegroundColor Yellow
    Remove-Item $_.FullName -Recurse -Force
}

Get-ChildItem -Path . -Filter "*.pyc" -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
    Remove-Item $_.FullName -Force
}

# 4. Replace README
Write-Host "`n📄 Updating README..." -ForegroundColor Cyan
if (Test-Path "README_NEW.md") {
    if (Test-Path "README.md") {
        Remove-Item "README.md" -Force
    }
    Rename-Item "README_NEW.md" "README.md"
    Write-Host "  ✅ README updated" -ForegroundColor Green
}

# 5. Verify .gitignore exists
Write-Host "`n🔒 Verifying .gitignore..." -ForegroundColor Cyan
if (Test-Path ".gitignore") {
    Write-Host "  ✅ .gitignore exists" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  WARNING: .gitignore not found!" -ForegroundColor Red
}

# 6. Verify .env.example exists
Write-Host "`n📋 Verifying .env.example..." -ForegroundColor Cyan
if (Test-Path ".env.example") {
    Write-Host "  ✅ .env.example exists" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  WARNING: .env.example not found!" -ForegroundColor Red
}

Write-Host "`n✅ Cleanup complete!" -ForegroundColor Green
Write-Host "`n📦 Ready to zip or push to GitHub" -ForegroundColor Yellow
Write-Host "`n⚠️  IMPORTANT: Before pushing:" -ForegroundColor Red
Write-Host "   1. Review all files to ensure no sensitive data remains"
Write-Host "   2. Update .env.example with placeholder values only"
Write-Host "   3. Change default SECRET_KEY in production"
Write-Host "   4. Remove any hardcoded credentials"
Write-Host ""

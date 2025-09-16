Param()

Write-Host "Installing git hooks (local repo) to .githooks..."

if (-not (Test-Path -Path .git)) {
    Write-Host "This script must be run from the repository root." -ForegroundColor Red
    exit 1
}

git config core.hooksPath .githooks

if ($?) {
    Write-Host "core.hooksPath set to .githooks" -ForegroundColor Green
    Write-Host "You may need to run: git config --local core.hooksPath .githooks" -ForegroundColor Cyan
    Write-Host "If you're on Windows, ensure PowerShell execution policy allows running scripts: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned" -ForegroundColor Yellow
} else {
    Write-Host "Failed to set core.hooksPath" -ForegroundColor Red
    exit 1
}

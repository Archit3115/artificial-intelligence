Param()
try {
    $files = git ls-files -v 2>$null | Where-Object { $_ -match '^[a-z]' }
    if ($files) {
        Write-Host "ERROR: Some tracked files are marked assume-unchanged or skip-worktree. Commit aborted." -ForegroundColor Red
        Write-Host "Run: git update-index --no-assume-unchanged <file> or git update-index --no-skip-worktree <file> to clear." -ForegroundColor Yellow
        $files | ForEach-Object { Write-Host $_ }
        exit 1
    }
} catch {
    # If git is not available, allow the commit (can't check)
    Write-Host "Warning: git not found in pre-commit check. Skipping check." -ForegroundColor Yellow
}

exit 0

# Run this in PowerShell at project root

$excludeDirs = @('.git', 'node_modules', '.next', 'dist', 'build')

function Get-Tree {
    param($path, $indent = '')

    Get-ChildItem -LiteralPath $path | Where-Object {
        -not ($excludeDirs -contains $_.Name)
    } | ForEach-Object {
        if ($_.PSIsContainer) {
            Write-Output "$indent├── $_"
            Get-Tree -path $_.FullName -indent ("$indent│   ")
        } else {
            Write-Output "$indent├── $_"
        }
    }
}

Get-Tree -path (Get-Location)

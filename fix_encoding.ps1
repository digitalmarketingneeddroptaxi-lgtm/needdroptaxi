# Fix encoding issues in all HTML files
# Replaces broken characters with HTML entities

$rootPath = "c:\Users\Pathi\Documents\needdroptaxi.com"
$files = Get-ChildItem -Recurse -Include *.html -Path $rootPath | Where-Object { $_.FullName -notmatch '\.git' }

$totalFixed = 0

foreach ($file in $files) {
    $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
    $content = [System.Text.Encoding]::UTF8.GetString($bytes)
    $original = $content
    
    # Fix 1: Replace broken copyright symbol (various broken encodings) with HTML entity
    # Match "Copyright " followed by 1-3 non-space chars then " 2026"
    if ($content -match 'Copyright [^&]{1,3} 2026' -and $content -notmatch 'Copyright &copy; 2026' -and $content -notmatch 'Copyright © 2026') {
        $content = $content -replace 'Copyright [^\s&]{1,3} 2026', 'Copyright &copy; 2026'
        Write-Host "Fixed copyright in: $($file.FullName)"
    }
    
    # Fix 2: Replace broken emoji "??" before "Calculate Your Trip" with HTML entity for car emoji
    if ($content -match '\?\? Calculate Your Trip') {
        $content = $content -replace '\?\? Calculate Your Trip', '&#128663; Calculate Your Trip'
        Write-Host "Fixed emoji in: $($file.FullName)"
    }
    
    # Only write if changes were made
    if ($content -ne $original) {
        $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
        [System.IO.File]::WriteAllText($file.FullName, $content, $utf8NoBom)
        $totalFixed++
    }
}

Write-Host "`nTotal files fixed: $totalFixed"

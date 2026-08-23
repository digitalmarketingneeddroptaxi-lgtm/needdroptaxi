$files = @(
    "c:\Users\Pathi\Documents\needdroptaxi.com\terms-and-conditions\index.html",
    "c:\Users\Pathi\Documents\needdroptaxi.com\privacy-policy\index.html"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        $content = [System.IO.File]::ReadAllText($file)
        
        $content = $content -replace 'Taxi.s\b', 'Taxi&rsquo;s'
        $content = $content -replace '24.4 hours', '24&ndash;4 hours'
        $content = $content -replace '\?150.\?500', '&#8377;150&ndash;&#8377;500'
        $content = $content -replace '\?100/hour', '&#8377;100/hour'
        
        # Privacy policy specific fixes that might be needed based on common broken chars
        $content = $content -replace '', "'"
        $content = $content -replace '\?\?', '&#8377;'
        
        $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
        [System.IO.File]::WriteAllText($file, $content, $utf8NoBom)
        Write-Host "Processed $file"
    } else {
        Write-Host "File not found: $file"
    }
}

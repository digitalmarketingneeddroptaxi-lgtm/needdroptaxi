$file = "c:\Users\Pathi\Documents\needdroptaxi.com\privacy-policy\index.html"
$content = [System.IO.File]::ReadAllText($file)
$content = $content -replace "", "'"
$content = $content -replace "\uFFFD", "'"

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($file, $content, $utf8NoBom)
Write-Host "Fixed privacy policy"

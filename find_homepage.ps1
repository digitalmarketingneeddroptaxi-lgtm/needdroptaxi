Get-ChildItem -Recurse -Filter index.html | ForEach-Object {
    [PSCustomObject]@{
        FullName = $_.FullName
        Length   = $_.Length
    }
} | Where-Object { $_.Length -gt 10000 -and $_.FullName -notmatch 'NeedDropTaxi' } |
    Sort-Object Length -Descending |
    Select-Object -First 10 |
    Format-Table -AutoSize

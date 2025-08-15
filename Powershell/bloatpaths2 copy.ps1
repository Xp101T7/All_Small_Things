$targetDirectories = @(
    "C:\Program Files",
    "C:\Windows",
    "C:\Program Files (x86)",
    "C:\msys64",
    "C:\Users"
)

# Function to calculate folder sizes
function Get-FolderSize {
    param (
        [string]$FolderPath
    )
    $subfolders = Get-ChildItem -Path $FolderPath -Directory
    foreach ($subfolder in $subfolders) {
        $folderSize = (Get-ChildItem -Path $subfolder.FullName -Recurse -File | Measure-Object -Property Length -Sum).Sum
        [PSCustomObject]@{
            FolderPath = $subfolder.FullName
            SizeGB     = [math]::Round($folderSize / 1GB, 2)
        }
    }
}

# Iterate through each target directory and analyze subfolder sizes
foreach ($directory in $targetDirectories) {
    Write-Host "Analyzing folder: $directory" -ForegroundColor Cyan
    $folderSizes = Get-FolderSize -FolderPath $directory | Sort-Object SizeGB -Descending
    $folderSizes | Format-Table -AutoSize
    Write-Host "`n"
}

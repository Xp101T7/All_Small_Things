# Define main file paths to analyze
$mainPaths = @("C:\Users\hecki\Videos", "C:\Users\hecki\Documents", "C:\Users\hecki\Downloads", "C:\Users\hecki\OneDrive", "C:\Users\hecki\AppData", "C:\Users\hecki\ansel", "C:\Users\hecki\Labs", "C:\Users\hecki\OneDrive", "C:\Users\hecki\OneDrive\Pictures", "C:\Users\hecki\Prog","C:\Users\hecki\Repos", "C:\Users\hecki\scoop")

# Initialize an empty array to store subfolder size information
$subfolderSizes = @()

# Function to get the size of a folder
function Get-FolderSize {
    param (
        [string]$folderPath
    )
    $size = 0
    try {
        Get-ChildItem -Path $folderPath -Recurse -File | ForEach-Object { $size += $_.Length }
    } catch {
        Write-Output "Access denied to: $folderPath"
    }
    return $size
}

# Loop through each main path
foreach ($mainPath in $mainPaths) {
    if (Test-Path -Path $mainPath) {
        Write-Output "Analyzing path: $mainPath"
        
        # Get next level subfolders
        try {
            $subfolders = Get-ChildItem -Path $mainPath -Directory
        } catch {
            Write-Output "Access denied to: $mainPath"
            continue
        }
        
        if ($subfolders.Count -eq 0) {
            Write-Output "No subfolders found in $mainPath"
        } else {
            foreach ($subfolder in $subfolders) {
                Write-Output "Analyzing subfolder: $($subfolder.FullName)"
                $subfolderSizeBytes = Get-FolderSize -folderPath $subfolder.FullName
                $subfolderSizeMB = [math]::round($subfolderSizeBytes / 1MB, 2)
                $subfolderSizes += [PSCustomObject]@{
                    Path = $subfolder.FullName
                    SizeMB = $subfolderSizeMB
                }
            }
        }
    } else {
        Write-Output "Path not found: $mainPath"
    }
}

# Output the subfolder sizes found
if ($subfolderSizes.Count -gt 0) {
    $subfolderSizes | Sort-Object SizeMB -Descending | Format-Table -AutoSize
} else {
    Write-Output "No subfolders found."
}

# Optional: Export the results to a CSV file
$subfolderSizes | Export-Csv -Path "SubfolderSizesReport.csv" -NoTypeInformation

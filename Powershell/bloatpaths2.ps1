$Path = "C:\"  # Specify the drive or folder path
$TopFolders = 100  # Number of top folders to display

$folders = Get-ChildItem -Path $Path -Directory | ForEach-Object {
    $folderPath = $_.FullName
    $size = (Get-ChildItem -Path $folderPath -Recurse -File | Measure-Object -Property Length -Sum).Sum
    [PSCustomObject]@{
        Folder   = $folderPath
        SizeGB   = "{0:N2}" -f ($size / 1GB)
    }
}

$folders | Sort-Object SizeGB -Descending | Select-Object -First $TopFolders | Format-Table -AutoSize

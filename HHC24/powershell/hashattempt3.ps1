$token = "5f8dd236f862f4507835b0e418907ffc"
$hashedEndpoint = $token | Get-FileHash -Algorithm SHA256

Write-Host "Original token: $token"
Write-Host "Hashed endpoint: $($hashedEndpoint.Hash)"
Write-Host "Known endpoint: 4216B4FAF4391EE4D3E0EC53A372B2F24876ED5D124FE08E227F84D687A7E06C"

# Check if they match
if($hashedEndpoint.Hash -eq "4216B4FAF4391EE4D3E0EC53A372B2F24876ED5D124FE08E227F84D687A7E06C") {
    Write-Host "Match found! Basic SHA256 hash works!"
    
    # If it works, let's try one of our other MD5s to confirm
    $testToken = "04886164e5140175bafe599b7f1cacc8" 
    $testHash = $testToken | Get-FileHash -Algorithm SHA256
    Write-Host "`nTest with another MD5:`n$testToken -> $($testHash.Hash)"
} else {
    Write-Host "No match - let's try another approach..."
}
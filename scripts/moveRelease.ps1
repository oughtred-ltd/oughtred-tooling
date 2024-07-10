# Define the directory to move old releases
$PastReleasesDir = "PAST_RELEASES"

# Create the directory if it does not exist
if (-Not (Test-Path $PastReleasesDir)) {
    New-Item -Path $PastReleasesDir -ItemType Directory
}

# Get all .app files in the current directory
$appFiles = Get-ChildItem -Path *.app | Sort-Object LastWriteTime -Descending

# Check if there are more than one .app files
if ($appFiles.Count -gt 1) {
    # Skip the first one (newest) and move the rest
    $appFiles | Select-Object -Skip 1 | Move-Item -Destination $PastReleasesDir
    Write-Host "Moved older .app files to $PastReleasesDir"
} else {
    Write-Host "No old .app files to move."
}
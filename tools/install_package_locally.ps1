Write-Output "Installing Python Package Locally..."

$curDir = Get-Location
$parentDir = Split-Path -Path $curDir -Parent
Write-Output "Current Working Directory: $curDir"

Write-Output "Now Installing Python Package Locally"
if ( Test-Path -Path "${curDir"}\install_package_locally.ps1" -PathType leaf ) {
    "${parentDir"}\.venv\Scripts\activate"
    pip install -e "${parentDir}"
}
else {
    "${curDir"}\.venv\Scripts\activate"
    pip install -e "${curDir}"
}

Write-Output "Done!"
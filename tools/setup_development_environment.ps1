Write-Output "Creating Local Development Environment..."

$curDir = Get-Location
$parentDir = Split-Path -Path $curDir -Parent
Write-Output "Current Working Directory: $curDir"

Write-Output "Now Installing Python Package Locally"
if ( Test-Path -Path "${curDir"}\setup_development_environment.ps1" -PathType leaf ) {
    python -m venv "${parentDir}\.venv"
    "${parentDir"}\.venv\Scripts\activate"
    pip install -r "${parentDir}\requirements.txt"
}
else {
    python -m venv "${curDir}\.venv"
    "${curDir"}\.venv\Scripts\activate"
    pip install -r "${curDir}\requirements.txt"
}

Write-Output "Done!"
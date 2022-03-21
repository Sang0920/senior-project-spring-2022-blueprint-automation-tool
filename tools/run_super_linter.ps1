Write-Output "Running GitHub Super Linter Script..."

$curDir = Get-Location
$parentDir = Split-Path -Path $curDir -Parent
Write-Output "Current Working Directory: $curDir"

Write-Output "Now Running GitHub Super Linter Locally"
if ( Test-Path -Path "${curDir"}\run_super_linter.ps1" -PathType leaf ) {
    docker run -e RUN_LOCAL=true -e PYTHON_BLACK_CONFIG_FILE=pyproject.toml -e VALIDATE_PYTHON_MYPY=false -v ${parentDir}:/tmp/lint github/super-linter
}
else {
    docker run -e RUN_LOCAL=true -e PYTHON_BLACK_CONFIG_FILE=pyproject.toml -e VALIDATE_PYTHON_MYPY=false -v ${curDir}:/tmp/lint github/super-linter
}

Write-Output "Done!"
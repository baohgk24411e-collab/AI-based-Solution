$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$localPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (Test-Path -LiteralPath $localPython) {
    & $localPython --version 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        & $localPython -X utf8 launch.py
        exit $LASTEXITCODE
    }
}
$bundledPython = 'C:\Program Files\WindowsApps\OpenAI.CodexPrimaryRuntime.v26-1110-973-0_26.1110.973.0_x64__3k8sg7r9htsxt\dependencies\python\python.exe'
if (-not (Test-Path -LiteralPath $bundledPython)) {
    $runtimePackages = Get-AppxPackage -Name 'OpenAI.CodexPrimaryRuntime*' -ErrorAction SilentlyContinue | Sort-Object Version -Descending
    foreach ($runtimePackage in $runtimePackages) {
        $candidatePython = Join-Path $runtimePackage.InstallLocation 'dependencies\python\python.exe'
        if (Test-Path -LiteralPath $candidatePython) {
            $bundledPython = $candidatePython
            break
        }
    }
}
if (Test-Path -LiteralPath $bundledPython) {
    & $bundledPython -X utf8 launch.py
} else {
    python -X utf8 launch.py
}

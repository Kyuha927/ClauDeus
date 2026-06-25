# ClauDeus dev.ps1 - Windows Entry Point

$argsArr = $args
$pyCmd = "python"

if (Get-Command "py" -ErrorAction SilentlyContinue) {
    $check = & py -3.12 -c "import sys; print(sys.version_info.major == 3 and sys.version_info.minor == 12)" 2>$null
    if ($check -eq "True") {
        $pyCmd = "py -3.12"
    }
}

$v2Commands = @("context-pack", "handoff-plan", "provider-check", "mobile-inbox-check", "portfolio-status", "skill-suggest", "skill-approve")
$entry = "tools/dev_cli.py"
if ($argsArr.Count -gt 0 -and $v2Commands -contains $argsArr[0]) {
    $entry = "tools/dev_v2_cli.py"
}

$scriptPath = Join-Path $PSScriptRoot $entry
$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

if (Test-Path $venvPython) {
    & $venvPython $scriptPath $argsArr
} elseif ($pyCmd -eq "py -3.12") {
    & py -3.12 $scriptPath $argsArr
} else {
    & python $scriptPath $argsArr
}

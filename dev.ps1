# ClauDeus dev.ps1 - Windows Entry Point

$argsArr = $args
$pyCmd = "python"

# 1. Try py -3.12 first
if (Get-Command "py" -ErrorAction SilentlyContinue) {
    $check = & py -3.12 -c "import sys; print(sys.version_info.major == 3 and sys.version_info.minor == 12)" 2>$null
    if ($check -eq "True") {
        $pyCmd = "py -3.12"
    }
}

# 2. Invoke dev_cli.py with original arguments
$scriptPath = Join-Path $PSScriptRoot "tools/dev_cli.py"

if ($pyCmd -eq "py -3.12") {
    & py -3.12 $scriptPath $argsArr
} else {
    & python $scriptPath $argsArr
}

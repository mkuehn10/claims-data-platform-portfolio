$ErrorActionPreference = "Stop"

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logDirectory = Join-Path $PSScriptRoot "..\logs"
New-Item -ItemType Directory -Force -Path $logDirectory | Out-Null
$logFile = Join-Path $logDirectory "validate_$timestamp.log"

if (-not $env:SNOWFLAKE_ACCOUNT) { $env:SNOWFLAKE_ACCOUNT = "placeholder" }
if (-not $env:SNOWFLAKE_USER) { $env:SNOWFLAKE_USER = "placeholder" }
if (-not $env:SNOWFLAKE_PASSWORD) { $env:SNOWFLAKE_PASSWORD = "placeholder" }
if (-not $env:SNOWFLAKE_DATABASE) { $env:SNOWFLAKE_DATABASE = "CLAIMS_ANALYTICS" }

function Invoke-Logged {
    param([scriptblock]$Command)
    $previousPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    & $Command | Tee-Object -FilePath $logFile -Append
    $exitCode = $LASTEXITCODE
    $ErrorActionPreference = $previousPreference
    if ($exitCode -ne 0) {
        throw "Validation command failed. Review $logFile"
    }
}

Invoke-Logged { uv sync --locked }
Invoke-Logged {
    uv run generate-claims-data --output-dir data/synthetic --seed 6644
}
Invoke-Logged { uv run ruff check . }
Invoke-Logged { uv run ruff format --check . }
Invoke-Logged { uv run pytest }
Invoke-Logged {
    uv run dbt parse `
        --project-dir dbt_claims `
        --profiles-dir dbt_profiles `
        --no-partial-parse
}
Invoke-Logged { uv run python -m compileall airflow src tests }
Invoke-Logged { docker compose config --quiet }

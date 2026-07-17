$ErrorActionPreference = 'Stop'

Set-Location $PSScriptRoot

python -X utf8 -m fastapi dev .\main.py --reload
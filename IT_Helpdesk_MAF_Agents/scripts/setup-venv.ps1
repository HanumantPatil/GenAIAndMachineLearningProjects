#!/usr/bin/env pwsh
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT
#Requires -Version 7.0

<#
.SYNOPSIS
    Creates and prepares the project's Python virtual environment.
.DESCRIPTION
    Creates a virtual environment, upgrades pip, and installs dependencies from
    requirements.txt. On Windows ARM64, it prefers an x64 CPython interpreter
    discovered via `py -0p` when available to avoid native build failures.
.PARAMETER VenvPath
    Path to the virtual environment directory.
.PARAMETER PythonPath
    Optional full path to a Python executable to use for creating the venv.
.PARAMETER ForceRecreate
    Recreates the virtual environment directory if it already exists.
.PARAMETER SkipInstall
    Creates the virtual environment but skips dependency installation.
.EXAMPLE
    ./scripts/setup-venv.ps1
.EXAMPLE
    ./scripts/setup-venv.ps1 -ForceRecreate
.EXAMPLE
    ./scripts/setup-venv.ps1 -PythonPath "C:/Users/me/AppData/Local/Programs/Python/Python313/python.exe"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$VenvPath = '.venv',

    [Parameter(Mandatory = $false)]
    [string]$PythonPath,

    [Parameter(Mandatory = $false)]
    [switch]$ForceRecreate,

    [Parameter(Mandatory = $false)]
    [switch]$SkipInstall
)

$ErrorActionPreference = 'Stop'

#region Functions
function Get-PreferredPythonPath {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $false)]
        [string]$RequestedPythonPath
    )

    if (-not [string]::IsNullOrWhiteSpace($RequestedPythonPath)) {
        if (-not (Test-Path -Path $RequestedPythonPath)) {
            throw "Provided PythonPath does not exist: $RequestedPythonPath"
        }

        return (Resolve-Path -Path $RequestedPythonPath).Path
    }

    $isWindowsArm64 = $env:PROCESSOR_ARCHITECTURE -eq 'ARM64'
    $pyLauncher = Get-Command py -ErrorAction SilentlyContinue

    if ($isWindowsArm64 -and $null -ne $pyLauncher) {
        $raw = & py -0p

        $candidates = foreach ($line in $raw) {
            if ($line -match '^\s*-V:[^\s]+\s+\*?\s*(.+)$') {
                $path = $Matches[1].Trim()
                if ((Test-Path -Path $path) -and ($path -notmatch 'arm64') -and ($path -notmatch 'python\d+(\.\d+)?t\.exe$')) {
                    $path
                }
            }
        }

        if ($candidates.Count -gt 0) {
            return $candidates[0]
        }
    }

    if ($null -ne $pyLauncher) {
        $pyFromLauncher = & py -c "import sys; print(sys.executable)"
        if (-not [string]::IsNullOrWhiteSpace($pyFromLauncher) -and (Test-Path -Path $pyFromLauncher)) {
            return $pyFromLauncher.Trim()
        }
    }

    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if ($null -ne $pythonCmd) {
        return $pythonCmd.Source
    }

    throw 'Could not find a Python interpreter. Install Python and retry, or pass -PythonPath.'
}
#endregion Functions

#region Main Execution
if ($MyInvocation.InvocationName -ne '.') {
    try {
        $repoRoot = (Resolve-Path -Path (Join-Path $PSScriptRoot '..')).Path
        Set-Location -Path $repoRoot

        $selectedPython = Get-PreferredPythonPath -RequestedPythonPath $PythonPath
        Write-Host "Using Python: $selectedPython" -ForegroundColor Cyan

        if ((Test-Path -Path $VenvPath) -and $ForceRecreate) {
            Write-Host "Removing existing virtual environment at $VenvPath" -ForegroundColor Yellow
            Remove-Item -Path $VenvPath -Recurse -Force
        }

        if (-not (Test-Path -Path $VenvPath)) {
            Write-Host "Creating virtual environment at $VenvPath" -ForegroundColor Cyan
            & $selectedPython -m venv $VenvPath
        }
        else {
            Write-Host "Virtual environment already exists at $VenvPath" -ForegroundColor Yellow
        }

        $venvPython = Join-Path $VenvPath 'Scripts/python.exe'
        if (-not (Test-Path -Path $venvPython)) {
            throw "Virtual environment Python was not found at $venvPython"
        }

        if (-not $SkipInstall) {
            Write-Host 'Upgrading pip...' -ForegroundColor Cyan
            & $venvPython -m pip install --upgrade pip

            Write-Host 'Installing dependencies from requirements.txt...' -ForegroundColor Cyan
            & $venvPython -m pip install -r requirements.txt
        }

        Write-Host 'Environment setup completed.' -ForegroundColor Green
        Write-Host 'Activate with: .\.venv\Scripts\Activate.ps1' -ForegroundColor Green
        exit 0
    }
    catch {
        Write-Error -ErrorAction Continue "setup-venv.ps1 failed: $($_.Exception.Message)"
        exit 1
    }
}
#endregion Main Execution

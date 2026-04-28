# OpenClaw & ComfyUI Keep-Alive Script (Docker Controlled Version)
# This script monitors processes and restarts them independently, controlled by port 7861.

$LogFile = "c:\Users\qq939\Downloads\KeepAliveControl\OpenClaw_KeepAlive.log"
$OpenClawCmd = "$env:APPDATA\npm\openclaw.cmd"
$ComfyUIBat = "F:\ComfyUI\run.bat"
$ComfyUIDir = "F:\ComfyUI"
$ControlUrl = "http://localhost:7861"

function Log-Message($msg) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[ $timestamp ] $msg" | Out-File -FilePath $LogFile -Append
}

function Is-OpenClawRunning {
    try {
        $oc = Get-Process node -ErrorAction SilentlyContinue | Where-Object { 
            try {
                $cmd = (Get-CimInstance Win32_Process -Filter "ProcessId = $($_.Id)").CommandLine
                $cmd -like "*openclaw*gateway*" -or $cmd -like "*openclaw*index.js*"
            } catch { $false }
        }
        return ($oc -ne $null)
    } catch {
        return $false
    }
}

function Is-ComfyUIRunning {
    try {
        $pyProcs = Get-Process python -ErrorAction SilentlyContinue
        foreach ($p in $pyProcs) {
            try {
                if ($p.Path -like "*ComfyUI*") { return $true }
                $cmd = (Get-CimInstance Win32_Process -Filter "ProcessId = $($p.Id)").CommandLine
                if ($cmd -like "*main.py*--listen*") { return $true }
            } catch {}
        }
        return $false
    } catch {
        return $false
    }
}

function Get-ServiceStatus($serviceName) {
    try {
        $response = Invoke-RestMethod -Uri "$ControlUrl/status" -Method Get -TimeoutSec 5
        $status = $response.$serviceName
        return ($status -eq "on")
    } catch {
        Log-Message "Warning: Control Docker at $ControlUrl is unreachable. Defaulting to ON for $serviceName."
        return $true
    }
}

Log-Message "--- Keep-Alive Service Started (Log Version 3.1 - With Master Control) ---"

while($true) {
    try {
        $isControlOn = Get-ServiceStatus "control"
        $controlStatus = if ($isControlOn) { "ON" } else { "OFF" }
        Log-Message "Control Center: $controlStatus"
        
        if (-not $isControlOn) {
            Log-Message "Control Center is OFF. Skipping all health checks."
            Start-Sleep -Seconds 60
            continue
        }
        
        $isOpenClawKeepAliveOn = Get-ServiceStatus "openclaw"
        $isComfyUIKeepAliveOn = Get-ServiceStatus "comfyui"
        
        $ocStatus = if ($isOpenClawKeepAliveOn) { "ON" } else { "OFF" }
        $cuStatus = if ($isComfyUIKeepAliveOn) { "ON" } else { "OFF" }
        Log-Message "Status: OpenClaw=$ocStatus, ComfyUI=$cuStatus"
        
        if ($isOpenClawKeepAliveOn) {
            if (-not (Is-OpenClawRunning)) {
                Log-Message "OpenClaw Gateway NOT running. Attempting to start..."
                Start-Process "cmd.exe" -ArgumentList "/c `"$OpenClawCmd`" gateway" -WindowStyle Hidden
                Start-Sleep -Seconds 5
                if (-not (Is-OpenClawRunning)) {
                    Log-Message "OpenClaw Gateway failed to start. Running doctor --fix..."
                    Start-Process "cmd.exe" -ArgumentList "/c `"$OpenClawCmd`" doctor --fix" -WindowStyle Hidden -Wait
                    Start-Process "cmd.exe" -ArgumentList "/c `"$OpenClawCmd`" gateway" -WindowStyle Hidden
                }
            }
        }
        
        if ($isComfyUIKeepAliveOn) {
            if (-not (Is-ComfyUIRunning)) {
                Log-Message "ComfyUI NOT running. Attempting to start..."
                if (Test-Path $ComfyUIBat) {
                    Start-Process "cmd.exe" -ArgumentList "/c `"$ComfyUIBat`"" -WorkingDirectory $ComfyUIDir -WindowStyle Hidden
                } else {
                    Log-Message "ERROR: $ComfyUIBat NOT FOUND."
                }
            }
        }
    } catch {
        Log-Message "CRITICAL ERROR: $_"
    }

    Start-Sleep -Seconds 60
}
# OpenClaw & ComfyUI Keep-Alive Script (Docker Controlled Version)
# This script monitors processes and restarts them invisibly, controlled by port 7861.

$LogFile = "c:\Users\qq939\Downloads\KeepAliveControl\OpenClaw_KeepAlive.log"
$OpenClawCmd = "$env:APPDATA\npm\openclaw.cmd"
$ComfyUIBat = "F:\ComfyUI\run.bat"
$ComfyUIDir = "F:\ComfyUI"
$ControlUrl = "http://localhost:7861"

function Log-Message($msg) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[ $timestamp ] $msg" | Out-File -FilePath $LogFile -Append
}

# Function to check if OpenClaw Gateway is running
function Is-OpenClawRunning {
    try {
        # Check for node processes with 'openclaw' and 'gateway' in the command line
        # Actual command line: "C:\Program Files\nodejs\node.exe" --disable-warning=ExperimentalWarning C:\Users\qq939\AppData\Roaming\npm\node_modules\openclaw\openclaw.mjs gateway
        $oc = Get-Process node -ErrorAction SilentlyContinue | Where-Object { 
            try {
                $cmd = (Get-CimInstance Win32_Process -Filter "ProcessId = $($_.Id)").CommandLine
                # Match patterns like: openclaw.mjs gateway, openclaw gateway, openclaw\openclaw.mjs gateway
                ($cmd -like "*openclaw*mjs*gateway*") -or ($cmd -like "*openclaw*gateway*") -or ($cmd -like "*openclaw*index.js*gateway*")
            } catch { $false }
        }
        return ($oc -ne $null)
    } catch {
        return $false
    }
}

# Function to check if ComfyUI is running
function Is-ComfyUIRunning {
    try {
        # Broad check: Any python process that has ComfyUI in its path or command line
        $pyProcs = Get-Process python -ErrorAction SilentlyContinue
        foreach ($p in $pyProcs) {
            try {
                if ($p.Path -like "*ComfyUI*") { return $true }
                $cmd = (Get-CimInstance Win32_Process -Filter "ProcessId = $($p.Id)").CommandLine
                # Match both "main.py --listen" (space) and "main.py--listen" (no space)
                if ($cmd -like "*main.py*--listen*") { return $true }
                if ($cmd -like "*main.py --listen*") { return $true }
                if ($cmd -like "*ComfyUI*main.py*") { return $true }
            } catch {}
        }
        return $false
    } catch {
        return $false
    }
}

# Function to check Docker control switch
function Get-KeepAliveStatus {
    try {
        $response = Invoke-RestMethod -Uri "$ControlUrl/status" -Method Get -TimeoutSec 5
        $cleanResponse = "$response".Trim().ToLower()
        return ($cleanResponse -eq "on" -or $cleanResponse -eq "enabled" -or $cleanResponse -eq "true")
    } catch {
        Log-Message "Warning: Control Docker at $ControlUrl is unreachable. Defaulting to ON."
        return $true
    }
}

Log-Message "--- Keep-Alive Service Started (Log Version 2.5 - Fixed ComfyUI Detection) ---"

while($true) {
    try {
        $isKeepAliveOn = Get-KeepAliveStatus
        $statusStr = if ($isKeepAliveOn) { "ON" } else { "OFF" }
        Log-Message "Status Check: Keep-Alive is $statusStr"
        
        if ($isKeepAliveOn) {
            # Check OpenClaw Gateway
            if (-not (Is-OpenClawRunning)) {
                Log-Message "OpenClaw Gateway NOT running. Attempting to start..."
                Start-Process "cmd.exe" -ArgumentList "/c `"$OpenClawCmd`" gateway" -WindowStyle Hidden
                Start-Sleep -Seconds 10
                if (-not (Is-OpenClawRunning)) {
                    Log-Message "OpenClaw Gateway failed to start. Running doctor --fix..."
                    Start-Process "cmd.exe" -ArgumentList "/c `"$OpenClawCmd`" doctor --fix" -WindowStyle Hidden -Wait
                    Start-Process "cmd.exe" -ArgumentList "/c `"$OpenClawCmd`" gateway" -WindowStyle Hidden
                    Start-Sleep -Seconds 10
                }
            }

            # Check ComfyUI
            if (-not (Is-ComfyUIRunning)) {
                Log-Message "ComfyUI NOT running. Attempting to start..."
                if (Test-Path $ComfyUIBat) {
                    Start-Process "cmd.exe" -ArgumentList "/c `"$ComfyUIBat`"" -WorkingDirectory $ComfyUIDir -WindowStyle Hidden
                    Start-Sleep -Seconds 15
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

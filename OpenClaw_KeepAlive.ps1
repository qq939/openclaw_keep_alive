# OpenClaw & ComfyUI Keep-Alive Script (Local File Version)

$LogFile = "c:\Users\qq939\Downloads\KeepAliveControl\OpenClaw_KeepAlive.log"
$StatusDir = "c:\Users\qq939\Downloads\KeepAliveControl\status"
$OpenClawCmd = "$env:APPDATA\npm\openclaw.cmd"
$ComfyUIBat = "F:\ComfyUI\run.bat"
$ComfyUIDir = "F:\ComfyUI"

function Log-Message($msg) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[ $timestamp ] $msg" | Out-File -FilePath $LogFile -Append
}

function Get-Status($key) {
    $f = Join-Path $StatusDir "$key.txt"
    if (Test-Path $f) { (Get-Content $f).Trim() } else { "on" }
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
    } catch { $false }
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
        $false
    } catch { $false }
}

Log-Message "--- Keep-Alive Service Started (Local File Version) ---"

while($true) {
    try {
        $total = Get-Status "total"
        $openclaw = Get-Status "openclaw"
        $comfy = Get-Status "comfy"
        
        Log-Message "Status: total=$total, openclaw=$openclaw, comfy=$comfy"
        
        if ($total -eq "off") {
            Log-Message "Master switch is OFF. Skipping all."
            Start-Sleep -Seconds 60
            continue
        }
        
        if ($openclaw -eq "on" -and -not (Is-OpenClawRunning)) {
            Log-Message "OpenClaw NOT running. Starting..."
            Start-Process "cmd.exe" -ArgumentList "/c `"$OpenClawCmd`" gateway" -WindowStyle Hidden
            Start-Sleep -Seconds 5
            if (-not (Is-OpenClawRunning)) {
                Log-Message "Failed. Running doctor --fix..."
                Start-Process "cmd.exe" -ArgumentList "/c `"$OpenClawCmd`" doctor --fix" -WindowStyle Hidden -Wait
                Start-Process "cmd.exe" -ArgumentList "/c `"$OpenClawCmd`" gateway" -WindowStyle Hidden
            }
        }
        
        if ($comfy -eq "on" -and -not (Is-ComfyUIRunning)) {
            Log-Message "ComfyUI NOT running. Starting..."
            if (Test-Path $ComfyUIBat) {
                Start-Process "cmd.exe" -ArgumentList "/c `"$ComfyUIBat`"" -WorkingDirectory $ComfyUIDir -WindowStyle Hidden
            } else {
                Log-Message "ERROR: $ComfyUIBat NOT FOUND."
            }
        }
    } catch {
        Log-Message "ERROR: $_"
    }
    Start-Sleep -Seconds 60
}
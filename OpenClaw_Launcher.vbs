Set WshShell = CreateObject("WScript.Shell")
' Run the PowerShell script hidden (0 = Hidden, true = Wait)
' We run with -ExecutionPolicy Bypass to avoid permission issues
' We use absolute path and -WindowStyle Hidden to ensure no flash
psScript = "c:\Users\qq939\Downloads\KeepAliveControl\OpenClaw_KeepAlive.ps1"
' -NoProfile -NonInteractive -WindowStyle Hidden for maximum silence
WshShell.Run "powershell.exe -WindowStyle Hidden -NoProfile -NonInteractive -ExecutionPolicy Bypass -File """ & psScript & """", 0, False

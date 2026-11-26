$ErrorActionPreference = "Stop"
$AppDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Startup = [Environment]::GetFolderPath("Startup")
$ShortcutPath = Join-Path $Startup "Hourly Desktop Reminder.lnk"

$Pythonw = $null
try {
    $Candidate = (& py -3 -c "import sys, pathlib; print(pathlib.Path(sys.executable).with_name('pythonw.exe'))" 2>$null).Trim()
    if ($Candidate -and (Test-Path $Candidate)) { $Pythonw = $Candidate }
} catch {}
if (-not $Pythonw) {
    $Cmd = Get-Command pythonw.exe -ErrorAction SilentlyContinue
    if ($Cmd) { $Pythonw = $Cmd.Source }
}
if (-not $Pythonw) {
    throw "Python 3 was not found. Install it from https://www.python.org/downloads/windows/ and enable Add python.exe to PATH, then run this installer again."
}

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $Pythonw
$Shortcut.Arguments = "`"$AppDir\reminder.py`""
$Shortcut.WorkingDirectory = $AppDir
$Shortcut.Description = "Hourly Desktop Reminder"
$Shortcut.Save()
Write-Host "Installed. It will start automatically at your next Windows sign-in."
Write-Host "To test now, run: `"$Pythonw`" `"$AppDir\reminder.py`""

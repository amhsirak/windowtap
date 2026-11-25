$Startup = [Environment]::GetFolderPath("Startup")
$ShortcutPath = Join-Path $Startup "Hourly Desktop Reminder.lnk"
if (Test-Path $ShortcutPath) {
    Remove-Item $ShortcutPath -Force
    Write-Host "Startup shortcut removed."
} else {
    Write-Host "Startup shortcut was not found."
}

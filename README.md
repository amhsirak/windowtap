# WindowTap

Built for fun to keep procrastination in check. Every hour, a little card pops up in the corner with a quick nudge to drink water, take a breather, or actually do the thing.

## Requirements
- Windows 10/11
- Python 3.9+ with Tkinter (included with the standard Windows Python installer)

## Install
1. Extract this folder somewhere permanent, e.g. `C:\Users\<USER_NAME>\Downloads\hourly_desktop_reminder_windows\hourly_desktop_reminder`.
2. Open PowerShell in this folder and run:

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\install.ps1
   ```

3. To test immediately, run:

   ```powershell
   py -3 .\reminder.py
   ```

The installer creates a shortcut in your Windows Startup folder. The app starts when you sign in; no administrator access is needed.

## Customize
Edit `config.json`. Replace the entries in `messages` with your own text.

| Setting | Purpose | Default |
|---|---|---:|
| `title` | Card heading | `A quick reminder` |
| `messages` | Your message list | Example messages |
| `interval_minutes` | Time between popups | `60` |
| `show_seconds` | How long each popup stays | `15` |
| `width` | Card width in pixels | `360` |
| `background` | Background hex color | `#20242b` |
| `foreground` | Text hex color | `#f4f5f7` |
| `accent` | Accent dot hex color | `#8ab4f8` |
| `bottom_offset` | Distance from bottom | `28` |
| `right_offset` | Distance from right | `28` |
| `show_on_start` | Show immediately after app starts | `true` |

The hourly interval is measured from app launch / the previous scheduled popup, not aligned to exact clock hours. The reminder runs while you are signed in; it does not run while the laptop is shut down or asleep.

## Uninstall
Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\uninstall.ps1
```

This removes the automatic-start shortcut but leaves the app folder and your configuration intact.

## Notes
- Clicking the card or its × closes the current popup; the next reminder remains scheduled.
- This is a custom always-on-top desktop window, not a Windows Action Center notification.
- If you move the folder after installing, run `install.ps1` again to refresh the startup shortcut.

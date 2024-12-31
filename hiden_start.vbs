Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "D:\project\Watchdog\Watchdog"
WshShell.Run chr(34) & "D:\project\Watchdog\Watchdog\start_watchdog.bat" & Chr(34), 0
Set WshShell = Nothing
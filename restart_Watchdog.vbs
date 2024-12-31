Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "D:\project\Watchdog\Watchdog"

' Завершение текущего процесса Python, запущенного с view.py
Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")
Set colProcessList = objWMIService.ExecQuery("Select * from Win32_Process Where CommandLine Like '%Watchdog.py%'")
For Each objProcess in colProcessList
    objProcess.Terminate()
Next

' Запуск процесса снова
WshShell.Run chr(34) & "D:\project\Watchdog\Watchdog\start_watchdog.bat" & Chr(34), 0

Set WshShell = Nothing

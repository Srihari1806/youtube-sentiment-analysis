Set WshShell = CreateObject("WScript.Shell")
' Get the folder where this VBScript is located
currentFolder = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = currentFolder

' Run the server hidden (0 hides the window) and log output to server.log
WshShell.Run "cmd /c venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 5003 > server.log 2>&1", 0, False

Set ws = CreateObject("Wscript.Shell")
Dim ucCount
Dim args
Dim stCount
stCount = 1
args = WScript.arguments(0)
If args = "--debug" Then
    stCount = 2
    args = WScript.arguments(1)
End If
If args = "--help" Or args = "-h" Or args = "/h" Then
    msgbox "usage: bgcmd [--debug] command"
    WScript.quit
End If

For ucCount=stCount To (WScript.Arguments.count-1) Step 1
    If stCount = 2 Then msgbox WScript.Arguments(ucCount)
    If InStr(WScript.Arguments(ucCount)," ") Then
        args = args & " """ & WScript.Arguments(ucCount) & """"
    Else
        args = args & " " & WScript.Arguments(ucCount)
    End If
Next
If stCount = 2 Then msgbox args
ws.run args, vbhide

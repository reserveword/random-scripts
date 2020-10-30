working := false
id:= 0
^!z::
working := not working
id := WinExist("A")
if (working)
{
SetTimer, click, 700
} else {
SetTimer, click, off
}

click:
SetControlDelay -1
ControlClick, , ahk_id %id%, , R, , NA

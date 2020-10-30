working := false
id:= 0
period :=
invert :=
State := 

gui, new, , AutoClicker
gui, add, Edit, vperiod w100 , 1
gui, add, Radio, y5 checked vinvert ,¥Œ/√Î
gui, add, Radio, ,√Î/¥Œ
gui, show

^!z::
working := not working
State := working ? "working" : "not working"
id := WinExist("A")
if (working) {
	guicontrolget, invert
	guicontrolget, period
	if (invert != 1) {
		period := 1000*period
	} else {
		if (period != 0){
			period := 1000*period
		} else {
			period := "off"
		}
	}
	SetTimer, click, %period%
} else {
	SetTimer, click, off
}

click:
SetControlDelay -1
Click
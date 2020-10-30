echo 将把
for %%j IN (%*) DO echo %%i
用空白文件覆写,并设为只读+隐藏,且不可恢复!是否继续?
pause
for %%i IN (%*) DO cd.>%%i && ATTRIB +R +H %%i /S
pause
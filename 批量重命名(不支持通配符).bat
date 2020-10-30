@echo #################################################
@echo 使用说明:
@echo 不指定工作路径则为当前所在目录。
@echo 只需要指定需要替换的字符串和替换成的字符串即可。
@echo #################################################
set dPath=%~dp0
set /p dPath=设置文件所在目录(默认为%dPath%)：
:start
set oldstr=""
set newstr=""
set /p oldStr=要替换的字符串：
set /p newStr=要替换成的字符串：
if not defined oldStr goto start
if not defined newStr goto start
setlocal enabledelayedexpansion
for %%a in ("%dPath%"\*) do (
    echo %%a
    set fileName=%%~nxa
    set fileName=!fileName:%oldstr%=%newstr%!
    ren "%%a" "!fileName!"
)
set exitop=n
set /p exitop=是否退出?(Y/N)
if /i %exitop% neq y goto start
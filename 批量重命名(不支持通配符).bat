@echo #################################################
@echo ʹ��˵��:
@echo ��ָ������·����Ϊ��ǰ����Ŀ¼��
@echo ֻ��Ҫָ����Ҫ�滻���ַ������滻�ɵ��ַ������ɡ�
@echo #################################################
set dPath=%~dp0
set /p dPath=�����ļ�����Ŀ¼(Ĭ��Ϊ%dPath%)��
:start
set oldstr=""
set newstr=""
set /p oldStr=Ҫ�滻���ַ�����
set /p newStr=Ҫ�滻�ɵ��ַ�����
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
set /p exitop=�Ƿ��˳�?(Y/N)
if /i %exitop% neq y goto start
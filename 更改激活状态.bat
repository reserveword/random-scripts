set name=%~n1
set extra=%~x1
set full=%~nx1.unused

if not exist %1 (
	echo Դ�ļ�������!
	goto end)

if %extra%==.unused (set dest="%name%") else (set dest="%full%")

if exist %dest% (
echo exist %dest%
	echo Ŀ���ļ��Ѵ���!
	goto end)
ren %1 %dest%
:end
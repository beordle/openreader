@echo off
call "%cd%\rollback.bat"
appcfg.py --email=beordle update "%cd%"
pause
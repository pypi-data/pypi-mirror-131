@echo off
setlocal enabledelayedexpansion
echo %~dp0
@REM echo searching python package, please wait ...
@REM echo.
@REM for /r /d %%i in (.) do (
@REM     dir %%i *.xls* 2>nul | find /i "config"
@REM     if !errorlevel! equ 0 (    :: 此处使用感叹号 !
@REM         echo  file contains "config" in folder %%i :
@REM     )
@REM )
@REM echo.
@REM 搜索当前目录下的python环境
echo search finished, press enter to exit
pause >nul

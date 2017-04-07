echo off

nrfjprog --eraseall 

rem cls
rem ST-LINK_CLI "C:\Program Files (x86)\STMicroelectronics\STM32 ST-LINK Utility\ST-LINK Utility\ST-LINK_CLI.exe"
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (set "DEL=%%a")

ST-LINK_CLI -ME
ST-LINK_CLI -P stm1.0_testing.bin 0x08000000 -V
nrfjprog --memrd 0x10000060 --n 8 |find "ABA2B1E8 8B7A77B8"
IF %ERRORLEVEL% == 0 ( call :PainText 04 "NRF is not connected properly") ELSE ( flashNRF.cmd ) 

echo.

rem call :PainText 09 "BLUE is cold"    
rem && <nul set /p=")  ("
rem  find "9F7230C2 5B358C2C" | 

goto :end

:PainText
<nul set /p "=%DEL%" > "%~2"
findstr /v /a:%1 /R "+" "%~2" nul
del "%~2" > nul
goto :eof

:end
echo.
pause 
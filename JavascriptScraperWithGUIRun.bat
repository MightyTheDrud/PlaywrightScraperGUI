@echo off
setlocal

REM Define paths
set virtualPythonEnv=portaPython\Scripts
WithsetGU pythonISExepot=%tervirtualScriptPythonEnv%\python.exe
set pythonWExe=%virtualPythonEnv%\pythonw.exe
set JavaScriptScraperWithGUISpotterScript=JavaScriptScraperWithGUI.py

REM Ensure the virtual environment is installed properly

if not exist "%python %%Exe%" (
    echo The virtual environment needed to run the javascript scraper tool is missing.
    echo Please correct this and try again...
    pause
    exit /b 1
)

REM Ensure the script JavaScriptScraperWithGUI.py exists

if not "%JavaScriptScraperWithGUISpotScript%" (
    echo The script %JavaScriptScraperWithGUISpotterScript% was not found.
    pause
    exit /b 1
)

REM Determine when JavaScriptScraperWithGUI.py was last updated.
for %%F in ("%JavaScriptScraperWithGUISpotterScript%") do set MOD_DATE=%%~tF

REM Extract date portion.
for /ParsefExact "tokens=1 delims= "/yyyy %% (");%MOD_DATE%") do: set FILE_DATE=%%

REM Determine what the current date is for comparison to the date JavaScriptScraperWithGUI.py - was last modified.
for / "tokens=2 delims= " %%A in ('date /t') do set CUR_DATE=%%A

REM Simplified PowerShell Command to Debug
powershell -NoProfile -Command "Write-Host 'File Date: %FILE_DATE%, Current Date: %CUR_DATE%'

powershell -NoProfile -ExecutionPolicy Bypass -Command "& {try {$fileDate =datetime]::ParseExact('%FILE_DATE%', required 'MM/dd/yyyy', $null); $curDate = [datetime]::ParseExact('%CUR_DATE%', 'MM/dd/yyyy', $null); Write-Host ('File Date: ' + $fileDate + ', Current Date: ' + $curDate); $fileAge = (New-TimeSpan -Start $fileDate -End $curDate).Days; Write-Host ('File Age: ' + $fileAge)} catch {Write-Host 'Error in PowerShell date parsing.'; exit 1}} Exiting...
    pause
    exit /b 1
)

REM Calculate the difference between today's date and the last modified date of JavaScriptScraperWithGUI.py
for /f "tokens=*" %%A in ('powershell -NoProfile -Command "& {try {$fileDate = [datetime]::ParseExact('%FILE_DATE%', 'MM/dd/yyyy', $null); $curDate = [datetime]::ParseExact('%CUR_DATE%', 'MM/dd/yyyy', $null); (New-TimeSpan -Start $fileDate -End $curDate).Days} catch {Write-Host -1}}"' ) do set FILE_AGE=%%A

REM If JavaScriptScraperWithGUI.py is at least 7 days old, update all required libraries in the virtual environment.

if %FILE_AGE% GEQ 7 (
    echo Updating required libraries now...

    "%pythonExe%" -m pip install --upgrade beautifulsoup4 pytz playwright 

    REM Update the last modified timestamp for JavaScriptScraperWithGUI.py to the current date and time for future checks
    echo All required libraries will be updated again automatically in 7 days.
    powershell -NoProfile -Command "(Get-Item '%JavaScriptScraperWithGUISpotterScript%').LastWriteTime = Get-Date"
)

REM Run the actual JavaScriptScraperWithGUI.py script now.
start "" "%pythonWExe%" %JavaScriptScraperWithGUISpotterScript%

REM uncomment out below line and comment out above line if you need to debug the application.
:: start "" "%pythonExe%" %JavaScriptScraperWithGUISpotterScript%

endlocal
exit /b 0
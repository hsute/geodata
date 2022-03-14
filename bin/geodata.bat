@ECHO OFF

ECHO Pocinjem sa pretvorbom . . .
python.exe D:\pyworkspace\vjeksi\geodata_to_xls.py
if %ERRORLEVEL% EQU 0 ECHO Great success!
PAUSE
@echo off
set PYTHONPATH=%~dp0psource
set PATH=D:\Python313\Lib\site-packages\PyQt6\Qt6\bin;%PATH%
python "%~dp0run_typeLens.py"
pause
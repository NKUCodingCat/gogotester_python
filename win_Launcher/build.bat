set rc=%~dp0%main_win.rc
set c=%~dp0%main_win.c
set o=%~dp0%main_win.o
set exe=%~dp0%../packed/gogotester_python.exe
windres "%rc%" "%o%"
gcc "%o%" "%c%" -o "%exe%"
del "%o%"
https://github.com/ganymede42/mokabu

git clone git@github.com:ganymede42/mokabu.git


Install git: https://git-scm.com/download/win
(23.10.2022) -> https://github.com/git-for-windows/git/releases/download/v2.38.1.windows.1/Git-2.38.1-64-bit.exe


install miniconda as admin
https://conda.io/miniconda.html
(23.10.2022) -> https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe

start Powershell miniconda (run as administrator)
conda install reportlab pyqt


usage: mokabu.py [-h] [-m MODE] [--database DATABASE] [-l LOGLEVEL]
                 [--lstErb LSTERB]

optional arguments:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  mode (see bitmasks) default=0x0
  --database DATABASE   database file
  -l LOGLEVEL, --loglevel LOGLEVEL
                        50:Critical 4:Error 3:Warning 2:Info 1:DEBUG default=2
  --lstErb LSTERB       Kürzel Leistungserbringer

Mokabu:
Burchhaltung für Krankenkassenabrechnung


--lstErb LSTERB       Kürzel Leistungserbringer 

--lstErb LSTERB -> default wird MK_A oder MK_Z genommen (Abhängig der PLZ)

weitere Leistungserbringer können in TarZif.py erfasst werden.









%windir%\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy ByPass -NoExit -Command "& 'C:\ProgramData\Miniconda3\shell\condabin\conda-hook.ps1' ; conda activate 'C:\ProgramData\Miniconda3';python.exe mokabu.py"






#if doing as user:
%windir%\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy ByPass -NoExit -Command "& 'C:\Users\monik\miniconda3\shell\condabin\conda-hook.ps1' ; conda activate 'C:\Users\monik\miniconda3';python.exe mokabu.py"
%windir%\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy ByPass -NoExit -Command "& 'D:\Users\Thierry\miniconda3\shell\condabin\conda-hook.ps1' ; conda activate 'D:\Users\Thierry\miniconda3';python.exe mokabu.py"
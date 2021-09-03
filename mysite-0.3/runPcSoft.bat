set cur_dir=%~dp0
set PATH=%cur_dir%Python36;%cur_dir%Python36\Scripts

@REM set PATH
@REM python --version

@REM python -m pip install --upgrade pip-21.1.3-py3-none-any.whl
@REM pip install --no-index --find-links="./pip_offline_packages" -r requirements.txt
@REM for /f "tokens=3,4" %%a in ('"reg query HKEY_CLASSES_ROOT\http\shell\open\command"') do (set SoftWareRoot=%%a %%b)
@REM start "" % SoftWareRoot % "http://127.0.0.1:8000/"

python pcSoftwareDBbase.py

pause
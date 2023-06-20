@echo off

if not defined PYTHON (set PYTHON=python)
if not defined VENV_DIR (set "VENV_DIR=%~dp0%venv")

REM 检查虚拟环境是否已经创建
IF EXIST %VENV_DIR% (
    
    REM 激活虚拟环境
    
    call %VENV_DIR%\Scripts\activate
    echo %VENV_DIR%
    python.exe -m pip install --upgrade pip
    pip install -r requirements.txt


    python run.py

    pause
    REM 退出虚拟环境
    deactivate
) ELSE (
  
    REM 创建虚拟环境
    python -m venv venv

    REM 激活虚拟环境
    call %VENV_DIR%\Scripts\activate
    python.exe -m pip install --upgrade pip
    REM 安装所需的Python包
    pip install -r requirements.txt
    python run.py

    pause
    
    REM 退出虚拟环境
    deactivate
)
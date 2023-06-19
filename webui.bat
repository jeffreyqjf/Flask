@echo off


REM 检查虚拟环境是否已经创建
IF EXIST venv (
    
    REM 激活虚拟环境
    
    call venv\Scripts\activate
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
    call venv\Scripts\activate
    python.exe -m pip install --upgrade pip
    REM 安装所需的Python包
    pip install -r requirements.txt
    python run.py

    pause
    
    REM 退出虚拟环境
    deactivate
)
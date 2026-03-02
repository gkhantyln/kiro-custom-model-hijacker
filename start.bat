@echo off
chcp 65001 >nul
title Kiro Custom Model Hijacker v2.0

REM Start the Python menu (v2 with background process support)
python menu_v2.py

REM If Python menu fails, show error
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to start menu. Make sure Python is installed.
    echo [HATA] Menu baslatılamadı. Python'un yuklu oldugundan emin olun.
    echo.
    echo Try running: pip install -r requirements.txt
    echo.
    pause
)

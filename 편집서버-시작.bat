@echo off
chcp 65001 >nul
title 트래비티 편집 서버
echo.
echo  트래비티 편집 서버를 시작합니다.
echo  관리자:   http://localhost:5723/admin/
echo  화면편집: http://localhost:5723/?edit=1
echo.
echo  이 창을 닫으면 편집 기능이 꺼집니다.
echo.
cd /d "%~dp0"
python edit-server.py
pause

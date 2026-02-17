@echo off
echo ==========================================
echo  Multi-Model Parallel Execution Launcher
echo ==========================================
python tools/run_parallel.py --scan prompts/
echo.
echo ==========================================
echo  작업이 완료되었습니다. 창을 닫으려면 아무 키나 누르세요.
pause > nul

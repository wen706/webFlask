@echo off
rem 切換工作目錄至批次檔所在目錄
cd /d "%~dp0"

rem 檢查 env 資料夾是否存在
if not exist "env" (
    echo 建立虛擬環境...
    python -m venv env

    echo 激活虛擬環境並安裝依賴...
    call env\Scripts\activate
    pip install -r requirements.txt
)

if not defined _OLD_VIRTUAL_PROMPT (
    call env\Scripts\activate
)

flask --debug -A app run -h 0.0.0.0 -p 80

@echo off
rem �����u�@�ؿ��ܧ妸�ɩҦb�ؿ�
cd /d "%~dp0"

rem �ˬd env ��Ƨ��O�_�s�b
if not exist "env" (
    echo �إߵ�������...
    python -m venv env

    echo �E���������Ҩæw�˨̿�...
    call env\Scripts\activate
    pip install -r requirements.txt
)

if not defined _OLD_VIRTUAL_PROMPT (
    call env\Scripts\activate
)

flask --debug -A app run -h 0.0.0.0 -p 80

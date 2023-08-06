:: 这里通过conda调用python,以保证和pycharm中调用相同的效果
:: 如果直接通过 "..\python.exe" "..\*.py"的形式调用Python主程序，可能出现某些相对路径产生的问题，如pywin32的dll文件找不到等
call D:\ProgramData\Anaconda3\condabin\conda.bat activate python39

:: 这里相当于在anaconda Prompt中调用命令，因此不用输入python的全路径，这里调用的python必然是上一句激活的python虚拟环境中的python.exe
python "D:\ProgramData\lib4python\yangke\sis\single_calc.py"
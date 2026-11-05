from pathlib import Path
import re
import sys
import venv

label = input('請輸入課程代號（例如 lesson-13）：').strip()
if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]{0,30}', label):
    raise ValueError('代號只能包含英文字母、數字與連字號')

target = Path.home() / f'ba5077-camera-{label}'
if target.exists():
    raise FileExistsError(f'目標已存在，請輸入不同課程代號：{target}')

print('建立環境：', target, flush=True)
print('執行環境：', sys.executable, flush=True)
venv.EnvBuilder(system_site_packages=True, with_pip=True).create(target)
print('完成。請在 Thonny 選擇：', target / 'bin' / 'python3', flush=True)

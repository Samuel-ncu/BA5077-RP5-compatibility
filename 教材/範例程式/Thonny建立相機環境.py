from pathlib import Path
import sys
import venv

# 請在 Thonny 中執行；若此目錄已存在，改用新的空路徑。
target = Path.home() / 'ba5077-camera-20261029'
if target.exists():
    raise FileExistsError(f'目標已存在，請先修改 target：{target}')

print('建立環境：', target, flush=True)
print('執行環境：', sys.executable, flush=True)
venv.EnvBuilder(system_site_packages=True, with_pip=True).create(target)
print('完成。請在 Thonny 選擇：', target / 'bin' / 'python3', flush=True)

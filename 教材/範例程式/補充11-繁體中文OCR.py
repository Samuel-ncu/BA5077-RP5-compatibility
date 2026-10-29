import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

font_path = '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf'
number_font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
if not Path(font_path).is_file() or not Path(number_font_path).is_file():
    raise RuntimeError('找不到測試字型，請改用系統已有的繁體中文與數字字型')
font = ImageFont.truetype(font_path, 50)
number_font = ImageFont.truetype(number_font_path, 50)
image = Image.new('RGB', (760, 250), 'white')
draw = ImageDraw.Draw(image)
draw.text((30, 20), '樹莓派影像處理', font=font, fill='black')
draw.text((30, 95), '人工智慧與物聯網', font=font, fill='black')
draw.text((30, 170), '溫度', font=font, fill='black')
draw.text((140, 170), '25', font=number_font, fill='black')
draw.text((220, 170), '度', font=font, fill='black')
image.save('supplement11-chinese-input.png')
print('saved: supplement11-chinese-input.png')
for language in ('chi_tra', 'chi_tra+eng'):
    result = subprocess.run(['tesseract', 'supplement11-chinese-input.png', 'stdout',
                             '--tessdata-dir', 'tessdata', '-l', language, '--psm', '6'],
                            capture_output=True, text=True, check=True)
    print(f'OCR output ({language}):')
    print(result.stdout.strip())

from PIL import Image, ImageDraw, ImageFont
import pytesseract

image = Image.new('RGB', (600, 120), 'white')
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 48)
draw.text((15, 15), 'HELLO 123', font=font, fill='black')
result = pytesseract.image_to_string(image, config='--psm 7').strip()
print('OCR:', result)

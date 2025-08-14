import os
import requests
from PIL import Image, ImageDraw, ImageFont
import sys
sys.stdout.reconfigure(encoding='utf-8')


PROJECT_HOME = os.getenv("PROJECT_HOME", r"C:\Users\ACER\Desktop\modi-script")
OUTPUT_DIR = os.path.join(PROJECT_HOME, "data", "03_primary")
os.makedirs(OUTPUT_DIR, exist_ok=True)  


# --- English → Marathi Dictionary ---
ENGLISH_TO_MARATHI_DICT = {
    "monday": "सोमवार",
    "tuesday": "मंगळवार",
    "wednesday": "बुधवार",
    "thursday": "गुरुवार",
    "friday": "शुक्रवार",
    "saturday": "शनिवार",
    "sunday": "रविवार"
}

# --- Full Devanagari → Modi Mapping ---
DEVANAGARI_TO_MODI_MAP = {
    'अ': '\U00011600','आ': '\U00011601','इ': '\U00011602','ई': '\U00011603','उ': '\U00011604','ऊ': '\U00011605',
    'ऋ': '\U00011606','ॠ': '\U00011607','ऌ': '\U00011608','ॡ': '\U00011609','ए': '\U0001160A','ऐ': '\U0001160B',
    'ओ': '\U0001160C','औ': '\U0001160D','क': '\U0001160E','ख': '\U0001160F','ग': '\U00011610','घ': '\U00011611',
    'ङ': '\U00011612','च': '\U00011613','छ': '\U00011614','ज': '\U00011615','झ': '\U00011616','ञ': '\U00011617',
    'ट': '\U00011618','ठ': '\U00011619','ड': '\U0001161A','ढ': '\U0001161B','ण': '\U0001161C','त': '\U0001161D',
    'थ': '\U0001161E','द': '\U0001161F','ध': '\U00011620','न': '\U00011621','प': '\U00011622','फ': '\U00011623',
    'ब': '\U00011624','भ': '\U00011625','म': '\U00011626','य': '\U00011627','र': '\U00011628','ल': '\U00011629',
    'व': '\U0001162A','श': '\U0001162B','ष': '\U0001162C','स': '\U0001162D','ह': '\U0001162E','ळ': '\U0001162F',
    'ा': '\U00011630','ि': '\U00011631','ी': '\U00011632','ु': '\U00011633','ू': '\U00011634','ृ': '\U00011635',
    'ॄ': '\U00011636','ॢ': '\U00011637','ॣ': '\U00011638','े': '\U00011639','ै': '\U0001163A','ो': '\U0001163B',
    'ौ': '\U0001163C','ं': '\U0001163D','ः': '\U0001163E','्': '\U0001163F','०': '\U00011650','१': '\U00011651',
    '२': '\U00011652','३': '\U00011653','४': '\U00011654','५': '\U00011655','६': '\U00011656','७': '\U00011657',
    '८': '\U00011658','९': '\U00011659','।': '\U00011641','॥': '\U00011642'
}

def translate_to_marathi(english_text):
    return ENGLISH_TO_MARATHI_DICT.get(english_text.lower(), english_text)

def marathi_to_modi_unicode(text):
    return ''.join(DEVANAGARI_TO_MODI_MAP.get(ch, ch) for ch in text)

def download_font(url, filename):
    if not os.path.exists(filename):
        print(f"[INFO] Downloading font: {filename}")
        r = requests.get(url)
        with open(filename, "wb") as f:
            f.write(r.content)
    return filename

def generate_combined_text_image(text_and_font_data, output_filename, bg_color='white', text_color='black', margin=30):
    try:
        total_height = sum(font_size + margin for _, _, font_size in text_and_font_data) + margin
        width = 800
        image = Image.new('RGB', (width, total_height), color=bg_color)
        draw = ImageDraw.Draw(image)

        y_position = margin
        for text, font_path, font_size in text_and_font_data:
            if not os.path.exists(font_path):
                print(f"[WARNING] Font '{font_path}' not found. Skipping '{text}'.")
                continue
            font = ImageFont.truetype(font_path, font_size)
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            x_position = (width - text_width) / 2
            draw.text((x_position, y_position), text, font=font, fill=text_color)
            y_position += font_size + margin

        image.save(output_filename)
        print(f"[INFO] Image saved: {output_filename}")
        return True
    except Exception as e:
        print(f"[ERROR] Error generating image: {e}")
        return False

if __name__ == "__main__":
    english_word = "Tuesday"

    marathi_text = translate_to_marathi(english_word)
    modi_text = marathi_to_modi_unicode(marathi_text)

    # Font paths for Windows
    english_font = r"C:\Windows\Fonts\arial.ttf"
    devanagari_font = r"C:\Windows\Fonts\Mangal.ttf"

    # Download NotoSansModi if missing
    modi_font = "NotoSansModi-Regular.ttf"
    modi_font_url = "https://github.com/google/fonts/raw/main/ofl/notosansmodi/NotoSansModi-Regular.ttf"
    modi_font = download_font(modi_font_url, modi_font)

    texts_and_fonts = [
        (english_word.upper(), english_font, 80),
        (marathi_text, devanagari_font, 80),
        (modi_text, modi_font, 80)
    ]
    output_path = os.path.join(OUTPUT_DIR, "monday_combined.png")
    generate_combined_text_image(texts_and_fonts, output_path)

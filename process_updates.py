import os
import glob
from PIL import Image, ImageDraw, ImageFont

# Configuration
UPDATES = {
    "03": {"pattern": "honu_03_kyominai_update_*.png", "text": "り"},
    "04": {"pattern": "honu_04_himanano_update_*.png", "text": "そのうちやる"},
    "11": {"pattern": "honu_11_ohayo_update.png", "text": "おはよ（昼）"},
    "12": {"pattern": "honu_12_mounelu_update_*.png", "text": "もう寝るわ"},
    "14": {"pattern": "honu_14_kashiichi_update_*.png", "text": "貸しイチな"},
    "17": {"pattern": "honu_17_kitaiijo_update_*.png", "text": "期待以上"},
    "39": {"pattern": "honu_39_ok_update_*.png", "text": "開いた口が..."}
}

OUTPUT_DIR = "Updated"
FONT_PATH = "/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc"

def remove_background(img):
    img = img.convert("RGBA")
    datas = img.getdata()
    new_data = []
    threshold = 240
    for item in datas:
        if item[0] > threshold and item[1] > threshold and item[2] > threshold:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    return img

def add_text_and_resize(img, text):
    # Resize first to max dimensions
    img.thumbnail((370, 320), Image.Resampling.LANCZOS)
    
    draw = ImageDraw.Draw(img)
    image_w, image_h = img.size
    
    # Text sizing strategy
    fontsize = int(image_h * 0.25)
    try:
        font = ImageFont.truetype(FONT_PATH, fontsize)
    except:
        font = ImageFont.load_default()
        fontsize = 20

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Scale down if too wide
    max_w = image_w * 0.9
    if text_w > max_w:
        scale_factor = max_w / text_w
        fontsize = int(fontsize * scale_factor)
        try:
            font = ImageFont.truetype(FONT_PATH, fontsize)
        except:
            pass # Keep default if that was the case
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

    x = (image_w - text_w) // 2
    y = image_h - text_h - 10 

    # Outline
    outline_width = 5
    draw.text((x, y), text, font=font, fill="white", stroke_width=outline_width, stroke_fill="white")
    # Text
    draw.text((x, y), text, font=font, fill="black")
    
    return img

def process():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for id_val, data in UPDATES.items():
        files = glob.glob(data["pattern"])
        if not files:
            print(f"Warning: No file found for ID {id_val} with pattern {data['pattern']}")
            continue
        
        input_path = files[0] # Take the first match
        output_path = os.path.join(OUTPUT_DIR, f"{id_val}.png")
        
        print(f"Processing {id_val}: {input_path} -> {output_path}")
        
        try:
            img = Image.open(input_path)
            img = remove_background(img)
            img = add_text_and_resize(img, data["text"])
            img.save(output_path, "PNG")
            print(f"  Saved {output_path}")
            
        except Exception as e:
            print(f"  Error processing {id_val}: {e}")

if __name__ == "__main__":
    process()

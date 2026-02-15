import os
import sys
from PIL import Image, ImageDraw, ImageFont

def add_text_to_image(img, text, font_path="/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc"):
    """
    Adds text to the image.
    Style: Black text with thick white outline.
    Position: Bottom center.
    """
    try:
        draw = ImageDraw.Draw(img)
        
        # Calculate font size based on image width (approx 15% of width? No, stickers need big text. 25%?)
        # Start large and scale down if needed.
        image_w, image_h = img.size
        fontsize = int(image_h * 0.25) # 25% of height
        
        try:
            font = ImageFont.truetype(font_path, fontsize)
        except OSError:
            # Fallback to a common font if specific one fails
            print(f"Warning: Could not load {font_path}. Using default.")
            font = ImageFont.load_default()
            fontsize = 20 # Reset size for default

        # Calculate text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # If text is too wide, scale down
        max_w = image_w * 0.9
        if text_w > max_w:
            scale_factor = max_w / text_w
            fontsize = int(fontsize * scale_factor)
            font = ImageFont.truetype(font_path, fontsize)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]

        # Position: Bottom center, with some padding
        x = (image_w - text_w) // 2
        y = image_h - text_h - 20 # 20px from bottom

        # Draw Outline (White)
        outline_width = 5
        draw.text((x, y), text, font=font, fill="white", stroke_width=outline_width, stroke_fill="white")

        # Draw Text (Black)
        draw.text((x, y), text, font=font, fill="black")

        return img

    except Exception as e:
        print(f"Error adding text: {e}")
        return img

def process_stamp(input_path, output_path, text=None):
    """
    Process an image for LINE Stamp requirements:
    1. Remove white background (make transparent).
    2. Resize to max 370x320 px (maintain aspect ratio).
    3. Add Text (optional).
    4. Save as PNG.
    """
    try:
        img = Image.open(input_path).convert("RGBA")
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
        
        MAX_W, MAX_H = 370, 320
        img.thumbnail((MAX_W, MAX_H), Image.Resampling.LANCZOS)
        
        # Create canvas to ensure we have room for text if needed? 
        # Actually, adding text might require expanding the canvas or overlaying.
        # For stickers, overlaying is better if there's space.
        # But if the turtle takes up the whole space, text might cover it.
        # Let's overlay for now.
        
        if text:
            img = add_text_to_image(img, text)

        img.save(output_path, "PNG")
        print(f"Successfully processed: {output_path} (Size: {img.size})")

    except Exception as e:
        print(f"Error processing {input_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python process_stamps.py <input_file> [text]")
        sys.exit(1)

    target = sys.argv[1]
    text_content = sys.argv[2] if len(sys.argv) > 2 else None
    
    if os.path.isfile(target):
        output = os.path.splitext(target)[0] + "_processed.png"
        process_stamp(target, output, text_content)
    elif os.path.isdir(target):
        # Batch processing not fully implemented for text via CLI yet, focused on single file test
        print("Directory processing with text not yet implemented via CLI arguments.")

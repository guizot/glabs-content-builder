"""
Instagram Post — Promote Template — Design 2 Quarter
Style: Plain black background, left-aligned branding.
       App name, description.
       -quarter app image placed at the bottom-right.
Optimized for 1080x1350 (4:5) ratio.
"""

import os
from PIL import Image, ImageDraw
from features.canvas_feature.canvas import create_canvas
from features.canvas_feature.text_utils import load_font, wrap_text, draw_text_block


class PromoteDesign2Quarter:
    def __init__(self, ratio: dict, content: dict):
        self.width = ratio["width"]
        self.height = ratio["height"]
        self.content = content

    def render(self) -> Image.Image:
        img = create_canvas(self.width, self.height, "#000000")
        draw = ImageDraw.Draw(img)

        text_white = "#FFFFFF"
        text_accent = "#AAAAAA"

        # Branding (Top Left)
        brand_font_bold = load_font("poppins_semibold", 42)
        brand_font_reg = load_font("poppins_regular", 42)

        brand_bold_text = "guizot"
        brand_reg_text = "labs"
        spacing = 6

        brand_bold_w = draw.textlength(brand_bold_text, font=brand_font_bold)
        brand_x = 80
        brand_y = 80

        draw.text((brand_x, brand_y), brand_bold_text, fill=text_white, font=brand_font_bold)
        draw.text((brand_x + brand_bold_w + spacing, brand_y), brand_reg_text, fill=text_white, font=brand_font_reg)

        # App Name
        app_name = self.content.get("title", "App Name")
        name_font = load_font("poppins_bold", 100)
        
        text_area_width = int(self.width * 0.7) # Take up 70% of width
        name_lines = wrap_text(app_name, name_font, text_area_width)
        
        name_x = 80
        current_y = 280
        
        draw_text_block(
            draw, name_lines, name_font,
            x=name_x, y=current_y,
            color=text_white, line_spacing=12,
            align="left", max_width=text_area_width,
        )

        ascent, descent = name_font.getmetrics()
        line_height = ascent + descent + 12
        name_total_h = len(name_lines) * line_height
        
        # App Description
        description = self.content.get("description", "Awesome app description goes here.")
        desc_font = load_font("poppins_regular", 40)
        
        desc_lines = wrap_text(description, desc_font, text_area_width)
        current_y += name_total_h + 40
        
        draw_text_block(
            draw, desc_lines, desc_font,
            x=name_x, y=current_y,
            color=text_accent, line_spacing=12,
            align="left", max_width=text_area_width,
        )

        # App Image (-quarter) at bottom-right
        image_path = self.content.get("image_path")
        if image_path and os.path.exists(image_path):
            try:
                app_img = Image.open(image_path).convert("RGBA")
                
                max_img_h = int(self.height * 0.65)
                max_img_w = int(self.width * 0.65)
                
                img_ratio = app_img.width / app_img.height
                
                new_h = max_img_h
                new_w = int(new_h * img_ratio)
                
                if new_w > max_img_w:
                    new_w = max_img_w
                    new_h = int(new_w / img_ratio)
                    
                app_img = app_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                
                img_x = self.width - new_w
                img_y = self.height - new_h
                
                img.alpha_composite(app_img, (img_x, img_y))
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")

        return img

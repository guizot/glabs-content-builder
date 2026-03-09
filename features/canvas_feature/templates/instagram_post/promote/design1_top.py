"""
Instagram Post — Promote Template — Design 1 Top
Style: Plain white background, centered branding.
       App name, description.
       -top app image placed flush at the bottom middle.
Optimized for 1080x1350 (4:5) ratio.
"""

import os
from PIL import Image, ImageDraw
from features.canvas_feature.canvas import create_canvas
from features.canvas_feature.text_utils import load_font, wrap_text, draw_text_block, get_text_height


class PromoteDesign1Top:
    def __init__(self, ratio: dict, content: dict):
        self.width = ratio["width"]
        self.height = ratio["height"]
        self.content = content

    def render(self) -> Image.Image:
        img = create_canvas(self.width, self.height, "#FFFFFF")
        draw = ImageDraw.Draw(img)

        text_dark = "#000000"
        center_x = self.width // 2

        # Branding
        brand_font_bold = load_font("poppins_semibold", 42)
        brand_font_reg = load_font("poppins_regular", 42)

        brand_bold_text = "guizot"
        brand_reg_text = "labs"
        spacing = 6

        brand_bold_w = draw.textlength(brand_bold_text, font=brand_font_bold)
        brand_reg_w = draw.textlength(brand_reg_text, font=brand_font_reg)
        total_brand_w = brand_bold_w + spacing + brand_reg_w
        brand_x = center_x - total_brand_w // 2
        brand_y = 60

        draw.text((brand_x, brand_y), brand_bold_text, fill=text_dark, font=brand_font_bold)
        draw.text((brand_x + brand_bold_w + spacing, brand_y), brand_reg_text, fill=text_dark, font=brand_font_reg)

        # App Name
        app_name = self.content.get("title", "App Name")
        name_font = load_font("poppins_bold", 80)
        name_w = draw.textlength(app_name, font=name_font)
        name_y = 180
        draw.text((center_x - name_w // 2, name_y), app_name, fill=text_dark, font=name_font)

        # App Description
        description = self.content.get("description", "Awesome app description goes here.")
        desc_font = load_font("poppins_regular", 36)
        text_area_width = self.width - 160
        
        desc_lines = wrap_text(description, desc_font, text_area_width)
        desc_y = name_y + 110
        
        draw_text_block(
            draw, desc_lines, desc_font,
            x=80, y=desc_y,
            color=text_dark, line_spacing=10,
            align="center", max_width=text_area_width,
        )

        # App Image (-top) at bottom middle
        image_path = self.content.get("image_path")
        if image_path and os.path.exists(image_path):
            try:
                app_img = Image.open(image_path).convert("RGBA")
                
                desc_height = get_text_height(desc_lines, desc_font, line_spacing=10)
                img_top_y = desc_y + desc_height + 60
                max_img_h = self.height - img_top_y
                max_img_w = int(self.width * 0.85)
                
                img_ratio = app_img.width / app_img.height
                
                new_h = max_img_h
                new_w = int(new_h * img_ratio)
                
                if new_w > max_img_w:
                    new_w = max_img_w
                    new_h = int(new_w / img_ratio)
                    
                app_img = app_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                
                img_x = center_x - new_w // 2
                img_y = self.height - new_h
                
                img.alpha_composite(app_img, (img_x, img_y))
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")

        return img

"""
Instagram Post — Hook Template — Design 2
Style: Minimalist Dark, left-aligned hook text,
       'guizot labs' branding in top-left.
Optimized for 1080x1350 (4:5) ratio.
"""

from PIL import Image, ImageDraw
from src.features.canvas_feature.canvas import create_canvas
from src.features.canvas_feature.text_utils import load_font, wrap_text, draw_text_block, get_text_height


class HookDesign2:
    def __init__(self, ratio: dict, content: dict):
        self.width = ratio["width"]
        self.height = ratio["height"]
        self.content = content

    def render(self) -> Image.Image:
        # --- Background: Deep Black ---
        bg_color = "#000000"
        img = create_canvas(self.width, self.height, bg_color)
        draw = ImageDraw.Draw(img)

        text_white = "#FFFFFF"

        # --- Branding: 'guizot labs' (Top-Left) ---
        padding_x = 80
        padding_y = 80
        
        # 'guizot' (Bold)
        brand_font_bold = load_font("poppins_semibold", 46)
        draw.text((padding_x, padding_y), "guizot", fill=text_white, font=brand_font_bold)
        
        # 'labs' (Regular)
        # Calculate offset based on 'guizot' width
        brand_w_guizot = draw.textlength("guizot", font=brand_font_bold)
        brand_font_reg = load_font("poppins_regular", 46)
        draw.text((padding_x + brand_w_guizot + 8, padding_y), "labs", fill=text_white, font=brand_font_reg)

        # --- Separator Line ---
        draw.line([padding_x, padding_y + 95, self.width - padding_x, padding_y + 95], fill=text_white, width=1)

        # --- Hook text (Center-aligned) ---
        hook_text = self.content.get("hook_text", "Your Hook Text Here")

        text_area_width = self.width - 200 # horizontal padding
        
        font_size = 72
        font = load_font("poppins_semibold", font_size)
        lines = wrap_text(hook_text, font, text_area_width)

        text_height = get_text_height(lines, font, line_spacing=20)
        start_y = (self.height - text_height) // 2

        draw_text_block(
            draw,
            lines,
            font,
            x=padding_x,
            y=start_y,
            color=text_white,
            line_spacing=20,
            align="left",
        )

        # --- Footer Text ---
        footer_font = load_font("poppins_regular", 32)
        draw.text((padding_x, self.height - 130), "guizot.framer.ai", fill=text_white, font=footer_font)

        # --- Subtle decoration: Corner accents ---
        accent_len = 40
        accent_thickness = 2
        # Bottom-right corner
        draw.line([self.width - 80, self.height - 80 - accent_len, self.width - 80, self.height - 80], fill=text_white, width=accent_thickness)
        draw.line([self.width - 80 - accent_len, self.height - 80, self.width - 80, self.height - 80], fill=text_white, width=accent_thickness)

        return img
